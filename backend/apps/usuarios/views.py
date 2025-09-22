from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.conf import settings
import os
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .models import Perfil, Plan
from .serializers import UserSerializer, PerfilSerializer, PlanSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener el usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """Actualizar el usuario actual"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Cambiar contraseña del usuario actual"""
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not all([current_password, new_password, confirm_password]):
            return Response(
                {'error': 'Todos los campos son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != confirm_password:
            return Response(
                {'error': 'Las contraseñas no coinciden'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 8:
            return Response(
                {'error': 'La nueva contraseña debe tener al menos 8 caracteres'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar contraseña actual
        if not request.user.check_password(current_password):
            return Response(
                {'current_password': ['Contraseña actual incorrecta']}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cambiar contraseña
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({'message': 'Contraseña cambiada exitosamente'})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def complete_onboarding(self, request):
        """Completa onboarding: setea rol, plan, datos de perfil y marca completado"""
        perfil = request.user.perfil
        es_prestador = request.data.get('es_prestador', None)
        plan = request.data.get('plan', None)
        perfil_data = request.data.get('perfil', {})

        if es_prestador is not None:
            perfil.es_prestador = bool(es_prestador)
        if plan:
            perfil.plan = plan
        
        # Actualizar datos del perfil si se proporcionan
        if perfil_data:
            # Validar campos permitidos por plan si es prestador
            if perfil.es_prestador and plan:
                from .models import Plan
                plan_obj = Plan.objects.filter(code=plan).first()
                if plan_obj and isinstance(plan_obj.fields_enabled, list):
                    allowed_fields = plan_obj.fields_enabled
                    # Filtrar solo campos permitidos
                    perfil_data = {k: v for k, v in perfil_data.items() 
                                 if k in allowed_fields or k in ['categoria', 'rubro']}
            
            # Aplicar cambios al perfil
            for field, value in perfil_data.items():
                if hasattr(perfil, field):
                    # Manejar campos ForeignKey especiales
                    if field == 'categoria' and value:
                        from apps.servicios.models import Categoria
                        try:
                            categoria_obj = Categoria.objects.get(id=value)
                            setattr(perfil, field, categoria_obj)
                        except Categoria.DoesNotExist:
                            pass  # Ignorar si no existe
                    elif field == 'rubro' and value:
                        from apps.servicios.models import Rubro
                        try:
                            rubro_obj = Rubro.objects.get(id=value)
                            setattr(perfil, field, rubro_obj)
                        except Rubro.DoesNotExist:
                            pass  # Ignorar si no existe
                    else:
                        setattr(perfil, field, value)
        
        perfil.onboarding_completed = True
        perfil.save()

        return Response(PerfilSerializer(perfil).data)


@api_view(['GET'])
def planes_view(request):
    """Lista de planes disponibles desde base de datos (requiere auth)."""
    queryset = Plan.objects.filter(is_active=True).order_by('order', 'id')
    serializer = PlanSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def google_login_view(request):
    """Vista independiente para login con Google - sin restricciones de autenticación"""
    credential = request.data.get('credential') or request.data.get('token_id')
    if not credential:
        return Response({"detail": "Falta credential de Google"}, status=400)

    client_id = os.environ.get('GOOGLE_CLIENT_ID') or getattr(settings, 'GOOGLE_CLIENT_ID', None)
    if not client_id:
        return Response({"detail": "GOOGLE_CLIENT_ID no configurado"}, status=500)

    try:
        # Verificar token de Google
        idinfo = id_token.verify_oauth2_token(credential, google_requests.Request(), client_id)
        # idinfo contiene: sub, email, name, picture, etc.
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        if not email:
            return Response({"detail": "Token de Google inválido"}, status=400)

        # Obtener o crear usuario local
        user, created = User.objects.get_or_create(username=email, defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        })
        
        # Obtener o crear perfil y actualizar información social
        perfil, perfil_created = Perfil.objects.get_or_create(
            usuario=user,
            defaults={
                'social_id': idinfo.get('sub'),  # Google user ID
                'social_provider': 'google',
            }
        )
        
        # Si el perfil ya existía, actualizar información social
        if not perfil_created:
            perfil.social_id = idinfo.get('sub')  # Google user ID
            perfil.social_provider = 'google'
            perfil.save()

        # Emitir JWT usando SimpleJWT
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    except Exception as e:
        return Response({"detail": "No se pudo verificar el token de Google", "error": str(e)}, status=400)
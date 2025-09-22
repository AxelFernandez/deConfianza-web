from rest_framework import viewsets, filters, status, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Categoria, Rubro, Servicio, Prestador, MediaPrestador, Resena, VisualizacionPerfil
from .serializers import (
    CategoriaSerializer, 
    RubroSerializer, 
    ServicioSerializer,
    PrestadorListSerializer,
    PrestadorDetailSerializer,
    MediaPrestadorSerializer,
    ResenaSerializer
)
from apps.usuarios.models import Plan

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    @action(detail=True, methods=['get'])
    def rubros(self, request, pk=None):
        """Obtener todos los rubros de una categoría"""
        categoria = self.get_object()
        rubros = categoria.rubros.all()
        serializer = RubroSerializer(rubros, many=True)
        return Response(serializer.data)

class RubroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rubro.objects.all()
    serializer_class = RubroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria']
    
    @action(detail=True, methods=['get'])
    def servicios(self, request, pk=None):
        """Obtener todos los servicios de un rubro"""
        rubro = self.get_object()
        servicios = rubro.servicios.all()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['rubro', 'categoria', 'activo']
    search_fields = ['nombre', 'descripcion']
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Servicio.objects.filter(prestador=self.request.user)
        return Servicio.objects.filter(activo=True)
    
    def perform_create(self, serializer):
        user = self.request.user
        
        # Verificar que el usuario sea prestador
        if not hasattr(user, 'perfil') or not user.perfil.es_prestador:
            raise serializers.ValidationError("Solo los prestadores pueden crear servicios")
        
        # Verificar permisos del plan
        plan = user.perfil.plan
        if not plan or not plan.puede_crear_servicios:
            raise serializers.ValidationError("Tu plan actual no permite crear servicios")
        
        # Verificar límite de servicios
        servicios_actuales = Servicio.objects.filter(prestador=user).count()
        if servicios_actuales >= plan.max_servicios:
            raise serializers.ValidationError(
                f"Has alcanzado el límite de {plan.max_servicios} servicios para tu plan actual"
            )
        
        serializer.save(prestador=user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_servicios(self, request):
        """Obtener servicios del usuario autenticado con información de límites"""
        user = request.user
        
        if not hasattr(user, 'perfil') or not user.perfil.es_prestador:
            return Response({'error': 'Usuario no es prestador'}, status=status.HTTP_403_FORBIDDEN)
        
        servicios = Servicio.objects.filter(prestador=user)
        serializer = self.get_serializer(servicios, many=True)
        
        # Información de límites
        plan = user.perfil.plan
        servicios_count = servicios.count()
        servicios_activos = servicios.filter(activo=True).count()
        
        limitaciones = {
            'servicios_creados': servicios_count,
            'servicios_activos': servicios_activos,
            'max_servicios': plan.max_servicios if plan else 1,
            'puede_crear_servicios': plan.puede_crear_servicios if plan else False,
            'puede_crear_mas': (plan.puede_crear_servicios if plan else False) and 
                              servicios_count < (plan.max_servicios if plan else 1)
        }
        
        return Response({
            'servicios': serializer.data,
            'limitaciones': limitaciones
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_resenas(self, request):
        """Obtener reseñas del prestador autenticado"""
        user = request.user
        
        if not hasattr(user, 'perfil') or not user.perfil.es_prestador:
            return Response({'error': 'Usuario no es prestador'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Obtener o crear el perfil de prestador
            prestador, created = Prestador.objects.get_or_create(
                usuario=user,
                defaults={
                    'nombre_comercial': user.get_full_name() or user.username,
                    'direccion': user.perfil.direccion or '',
                    'ciudad': user.perfil.ciudad or '',
                    'provincia': user.perfil.provincia or '',
                    'telefono': user.perfil.telefono or '',
                }
            )
            
            # Obtener reseñas
            resenas = Resena.objects.filter(prestador=prestador).order_by('-fecha')
            
            # Estadísticas
            total_resenas = resenas.count()
            promedio_calificacion = resenas.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
            
            # Distribución de calificaciones
            distribucion = {}
            for i in range(1, 6):
                distribucion[i] = resenas.filter(calificacion=i).count()
            
            # Serializar reseñas
            resenas_data = []
            for resena in resenas:
                resenas_data.append({
                    'id': resena.id,
                    'nombre': resena.nombre,
                    'email': resena.email,
                    'calificacion': resena.calificacion,
                    'comentario': resena.comentario,
                    'fecha': resena.fecha.strftime('%Y-%m-%d %H:%M')
                })
            
            return Response({
                'resenas': resenas_data,
                'estadisticas': {
                    'total_resenas': total_resenas,
                    'promedio_calificacion': round(promedio_calificacion, 1),
                    'distribucion': distribucion
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo reseñas: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PrestadorViewSet(viewsets.ModelViewSet):
    queryset = Prestador.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ciudad', 'provincia']
    search_fields = ['nombre_comercial', 'descripcion']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PrestadorListSerializer
        return PrestadorDetailSerializer
    
    def get_queryset(self):
        queryset = Prestador.objects.all()
        
        # Filtrado por ubicación
        ciudad = self.request.query_params.get('ciudad', None)
        if ciudad:
            queryset = queryset.filter(ciudad__icontains=ciudad)
            
        provincia = self.request.query_params.get('provincia', None)
        if provincia:
            queryset = queryset.filter(provincia__icontains=provincia)
            
        # Filtrado por servicio, rubro o categoría
        servicio_id = self.request.query_params.get('servicio', None)
        if servicio_id:
            queryset = queryset.filter(usuario__servicios_creados__id=servicio_id)
            
        rubro_id = self.request.query_params.get('rubro', None)
        if rubro_id:
            queryset = queryset.filter(usuario__servicios_creados__rubro__id=rubro_id)
            
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id:
            queryset = queryset.filter(usuario__servicios_creados__categoria__id=categoria_id)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def resenas(self, request, pk=None):
        prestador = self.get_object()
        resenas = prestador.resenas.all()
        serializer = ResenaSerializer(resenas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def media(self, request, pk=None):
        prestador = self.get_object()
        media = prestador.media.all()
        serializer = MediaPrestadorSerializer(media, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Obtener detalles del prestador y registrar visualización"""
        response = super().retrieve(request, *args, **kwargs)
        
        # Registrar visualización
        prestador = self.get_object()
        self._registrar_visualizacion(prestador, request)
        
        return response
    
    def _registrar_visualizacion(self, prestador, request):
        """Registrar una visualización del perfil del prestador"""
        try:
            # Obtener IP del cliente
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Obtener User-Agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Crear registro de visualización
            VisualizacionPerfil.objects.create(
                prestador=prestador,
                ip_address=ip,
                user_agent=user_agent
            )
        except Exception as e:
            # No fallar la respuesta principal si hay error en el tracking
            print(f"Error registrando visualización: {e}")

class MediaPrestadorViewSet(viewsets.ModelViewSet):
    queryset = MediaPrestador.objects.all()
    serializer_class = MediaPrestadorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prestador', 'tipo']

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prestador', 'calificacion']




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_prestador(request):
    """Endpoint para obtener datos del dashboard del prestador"""
    user = request.user
    
    # Verificar que el usuario sea prestador
    if not hasattr(user, 'perfil') or not user.perfil.es_prestador:
        return Response({'error': 'Usuario no es prestador'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Obtener o crear el perfil de prestador
        prestador, created = Prestador.objects.get_or_create(
            usuario=user,
            defaults={
                'nombre_comercial': user.get_full_name() or user.username,
                'direccion': user.perfil.direccion or '',
                'ciudad': user.perfil.ciudad or '',
                'provincia': user.perfil.provincia or '',
                'telefono': user.perfil.telefono or '',
            }
        )
        
        # Obtener el plan del usuario
        plan_obj = user.perfil.plan
        
        # Estadísticas básicas
        total_visualizaciones = VisualizacionPerfil.objects.filter(prestador=prestador).count()
        visualizaciones_mes = VisualizacionPerfil.objects.filter(
            prestador=prestador,
            fecha__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Reseñas
        resenas_qs = Resena.objects.filter(prestador=prestador)
        total_resenas = resenas_qs.count()
        promedio_calificacion = resenas_qs.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
        ultimas_resenas = resenas_qs.order_by('-fecha')[:5]
        
        # Servicios
        servicios_qs = Servicio.objects.filter(prestador=user)
        total_servicios = servicios_qs.count()
        servicios_activos = servicios_qs.filter(activo=True).count()
        
        # Limitaciones y permisos por plan
        limitaciones = {
            'max_servicios': plan_obj.max_servicios if plan_obj else 1,
            'servicios_creados': total_servicios,
            'servicios_activos': servicios_activos,
            'puede_crear_servicios': plan_obj.puede_crear_servicios if plan_obj else False,
            'puede_crear_mas': (plan_obj.puede_crear_servicios if plan_obj else False) and 
                              total_servicios < (plan_obj.max_servicios if plan_obj else 1),
            'puede_recibir_resenas': plan_obj.puede_recibir_resenas if plan_obj else False,
            'puede_subir_media': plan_obj.puede_subir_media if plan_obj else False,
            'puede_ver_estadisticas': plan_obj.puede_ver_estadisticas if plan_obj else False,
            'max_images': plan_obj.max_images if plan_obj else 0,
            'max_videos': plan_obj.max_videos if plan_obj else 0,
        }
        
        # Serializar reseñas
        resenas_data = []
        for resena in ultimas_resenas:
            resenas_data.append({
                'id': resena.id,
                'nombre': resena.nombre,
                'calificacion': resena.calificacion,
                'comentario': resena.comentario,
                'fecha': resena.fecha.strftime('%Y-%m-%d')
            })
        
        # Información del plan
        plan_info = None
        if plan_obj:
            plan_info = {
                'code': plan_obj.code,
                'name': plan_obj.name,
                'price_text': plan_obj.price_text,
                'precio_mensual': float(plan_obj.precio_mensual),
                'fields_enabled': plan_obj.fields_enabled,
                'max_images': plan_obj.max_images,
                'max_videos': plan_obj.max_videos,
                'max_servicios': plan_obj.max_servicios,
                'puede_crear_servicios': plan_obj.puede_crear_servicios,
                'puede_recibir_resenas': plan_obj.puede_recibir_resenas,
                'puede_subir_media': plan_obj.puede_subir_media,
                'puede_ver_estadisticas': plan_obj.puede_ver_estadisticas,
            }
        
        return Response({
            'estadisticas': {
                'total_visualizaciones': total_visualizaciones,
                'visualizaciones_mes': visualizaciones_mes,
                'total_resenas': total_resenas,
                'promedio_calificacion': round(promedio_calificacion, 1),
                'total_servicios': total_servicios,
                'servicios_activos': servicios_activos,
            },
            'plan': plan_info,
            'limitaciones': limitaciones,
            'ultimas_resenas': resenas_data,
            'prestador': {
                'id': prestador.id,
                'nombre_comercial': prestador.nombre_comercial,
                'ciudad': prestador.ciudad,
                'provincia': prestador.provincia,
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error obteniendo datos del dashboard: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([])  # No requiere autenticación para registrar visualizaciones
def registrar_visualizacion(request):
    """Endpoint para registrar visualizaciones de perfiles de prestadores"""
    try:
        prestador_id = request.data.get('prestador_id')
        if not prestador_id:
            return Response({'error': 'prestador_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            prestador = Prestador.objects.get(id=prestador_id)
        except Prestador.DoesNotExist:
            return Response({'error': 'Prestador no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener IP del cliente
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Obtener User-Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Verificar si ya existe una visualización reciente (últimos 5 minutos) desde la misma IP
        # para evitar spam de visualizaciones
        from datetime import timedelta
        visualizacion_reciente = VisualizacionPerfil.objects.filter(
            prestador=prestador,
            ip_address=ip,
            fecha__gte=timezone.now() - timedelta(minutes=5)
        ).exists()
        
        if not visualizacion_reciente:
            # Crear registro de visualización
            VisualizacionPerfil.objects.create(
                prestador=prestador,
                ip_address=ip,
                user_agent=user_agent
            )
        
        return Response({'success': True, 'message': 'Visualización registrada'})
        
    except Exception as e:
        return Response(
            {'error': f'Error registrando visualización: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

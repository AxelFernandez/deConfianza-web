from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Perfil, Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'code', 'name', 'price_text', 'precio_mensual', 'fields_enabled', 'max_images', 'max_videos', 
                  'puede_crear_servicios', 'puede_recibir_resenas', 'puede_subir_media', 'puede_ver_estadisticas', 
                  'max_servicios', 'is_active', 'order']

class PerfilSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    rubro_nombre = serializers.CharField(source='rubro.nombre', read_only=True)
    plan_info = PlanSerializer(source='plan', read_only=True)
    is_google_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion', 'ciudad', 'provincia', 'pais', 'es_prestador', 'plan', 
                  'onboarding_completed', 'categoria', 'rubro', 'categoria_nombre', 'rubro_nombre', 
                  'plan_info', 'social_id', 'social_provider', 'is_google_user']
    
    def get_is_google_user(self, obj):
        return bool(obj.social_provider == 'google' and obj.social_id)

class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(required=False)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'perfil']
        
    def create(self, validated_data):
        perfil_data = validated_data.pop('perfil', {})
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        Perfil.objects.create(usuario=user, **perfil_data)
        return user
    
    def update(self, instance, validated_data):
        perfil_data = validated_data.pop('perfil', {})
        password = validated_data.pop('password', None)
        
        # Validar campos de perfil habilitados por plan
        if perfil_data:
            try:
                perfil_instance = instance.perfil
                plan_obj = getattr(perfil_instance, 'plan', None)
                allowed_fields = []
                if plan_obj and isinstance(plan_obj.fields_enabled, list):
                    allowed_fields = plan_obj.fields_enabled
                # Si no se encuentra plan en BD, permitir solo campos básicos por defecto
                disallowed = [field_name for field_name in perfil_data.keys() if field_name not in allowed_fields]
                if disallowed:
                    # Opcional: podríamos ignorar en lugar de fallar. Elegimos fallar para feedback claro.
                    raise ValidationError({f: 'Campo no habilitado por el plan actual' for f in disallowed})
            except Exception:
                # En caso de error inesperado, no bloquear actualización de usuario, pero no aplicar perfil
                pass

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        
        perfil = instance.perfil
        for attr, value in perfil_data.items():
            setattr(perfil, attr, value)
        perfil.save()
        
        return instance

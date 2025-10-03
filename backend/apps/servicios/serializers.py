from rest_framework import serializers
from .models import Categoria, Rubro, Servicio, MediaPrestador, Resena
from apps.usuarios.models import Plan, Perfil
from django.contrib.auth.models import User

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class RubroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubro
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    prestador_username = serializers.CharField(source='prestador.username', read_only=True)
    categoria_nombre = serializers.CharField(source='prestador.perfil.categoria.nombre', read_only=True)
    rubro_nombre = serializers.CharField(source='prestador.perfil.rubro.nombre', read_only=True)
    
    class Meta:
        model = Servicio
        fields = ['id', 'prestador', 'prestador_username', 'nombre', 'descripcion', 'precio_base', 
                  'categoria_nombre', 'rubro_nombre', 'activo', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['prestador', 'fecha_creacion', 'fecha_actualizacion']

class MediaPrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaPrestador
        fields = '__all__'

    def validate(self, attrs):
        usuario = attrs.get('usuario')
        tipo = attrs.get('tipo')
        if not usuario or not tipo:
            return attrs

        perfil = getattr(usuario, 'perfil', None)
        plan = getattr(perfil, 'plan', None) if perfil else None

        if plan:
            if tipo == 'imagen':
                count_images = usuario.media_prestador.filter(tipo='imagen').count()
                if plan.max_images and count_images >= plan.max_images:
                    raise serializers.ValidationError({'archivo': 'Límite de imágenes alcanzado para tu plan'})
            if tipo == 'video':
                count_videos = usuario.media_prestador.filter(tipo='video').count()
                if plan.max_videos and count_videos >= plan.max_videos:
                    raise serializers.ValidationError({'archivo': 'Límite de videos alcanzado para tu plan'})

        return attrs

class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = '__all__'

    def create(self, validated_data):
        # Verificar si el prestador puede recibir reseñas según su plan
        usuario = validated_data['usuario']
        perfil = getattr(usuario, 'perfil', None)
        plan = getattr(perfil, 'plan', None)
        
        if not plan or not plan.puede_recibir_resenas:
            raise serializers.ValidationError("Este prestador no acepta reseñas")
        return super().create(validated_data)

class PrestadorListSerializer(serializers.ModelSerializer):
    """Serializer para la lista de prestadores (basado en Perfil)"""
    ubicacion = serializers.SerializerMethodField()
    servicios = serializers.SerializerMethodField()
    puntuacion = serializers.SerializerMethodField()
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    rubro_nombre = serializers.CharField(source='rubro.nombre', read_only=True)
    nombre_comercial = serializers.SerializerMethodField()
    fecha_registro = serializers.SerializerMethodField()
    
    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'nombre_comercial', 'telefono', 'direccion', 'ciudad', 'provincia', 'pais',
                  'ubicacion', 'categoria_nombre', 'rubro_nombre', 'puntuacion', 'servicios', 'fecha_registro']
    
    def get_nombre_comercial(self, obj):
        """Obtener nombre comercial del usuario"""
        user = obj.usuario
        return user.get_full_name() or user.username
    
    def get_fecha_registro(self, obj):
        """Obtener fecha de registro del usuario"""
        return obj.usuario.date_joined
    
    def get_ubicacion(self, obj):
        """Formatear ubicación completa para mostrar en la lista"""
        ubicacion_parts = []
        if obj.direccion:
            ubicacion_parts.append(obj.direccion)
        if obj.ciudad:
            ubicacion_parts.append(obj.ciudad)
        if obj.provincia:
            ubicacion_parts.append(obj.provincia)
        return ', '.join(ubicacion_parts) if ubicacion_parts else None
    
    def get_servicios(self, obj):
        """Obtener servicios activos del prestador solo si su plan lo permite"""
        plan = getattr(obj, 'plan', None)
        
        # Solo incluir servicios si el plan permite crear servicios
        if plan and plan.puede_crear_servicios:
            servicios = Servicio.objects.filter(prestador=obj.usuario, activo=True)
            return ServicioSerializer(servicios, many=True).data
        
        # Si no tiene permisos, no incluir servicios
        return None
    
    def get_puntuacion(self, obj):
        """Calcular puntuación promedio de las reseñas"""
        resenas = obj.usuario.resenas_recibidas.all()
        if not resenas:
            return 0
        return round(sum(r.calificacion for r in resenas) / resenas.count(), 1)
    
    def to_representation(self, instance):
        """Filtra los campos de salida según los permisos del plan del prestador."""
        data = super().to_representation(instance)
        
        # Obtener el plan del prestador
        plan = getattr(instance, 'plan', None)
        
        # Si servicios es None (no permitido), eliminar el campo completamente
        if data.get('servicios') is None:
            del data['servicios']
        
        # Filtrar otros campos según el plan
        if not plan:
            # Sin plan: mantener solo campos básicos
            basic_fields = {'id', 'usuario', 'nombre_comercial', 'ciudad', 'provincia', 'ubicacion', 'puntuacion', 'fecha_registro'}
            for key in list(data.keys()):
                if key not in basic_fields:
                    del data[key]
        else:
            # Con plan: aplicar filtros según fields_enabled
            allowed_fields = set(plan.fields_enabled) if plan.fields_enabled else set()
            
            # Filtrar campos de contacto/ubicación
            if 'telefono' not in allowed_fields and 'telefono' in data:
                del data['telefono']
            if 'direccion' not in allowed_fields and 'direccion' in data:
                del data['direccion']
        
        return data

class PrestadorDetailSerializer(serializers.ModelSerializer):
    """Serializer para el detalle de un prestador (basado en Perfil)"""
    plan_info = serializers.SerializerMethodField()
    servicios = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    resenas = serializers.SerializerMethodField()
    promedio_calificacion = serializers.SerializerMethodField()
    nombre_comercial = serializers.SerializerMethodField()
    fecha_registro = serializers.SerializerMethodField()
    
    class Meta:
        model = Perfil
        fields = '__all__'
        
    def get_nombre_comercial(self, obj):
        """Obtener nombre comercial del usuario"""
        user = obj.usuario
        return user.get_full_name() or user.username
    
    def get_fecha_registro(self, obj):
        """Obtener fecha de registro del usuario"""
        return obj.usuario.date_joined
        
    def get_promedio_calificacion(self, obj):
        resenas = obj.usuario.resenas_recibidas.all()
        if not resenas:
            return 0
        return sum(r.calificacion for r in resenas) / resenas.count()
    
    def get_servicios(self, obj):
        """Obtener servicios activos del prestador solo si su plan lo permite"""
        plan = getattr(obj, 'plan', None)
        
        # Solo incluir servicios si el plan permite crear servicios
        if plan and plan.puede_crear_servicios:
            servicios = Servicio.objects.filter(prestador=obj.usuario, activo=True)
            return ServicioSerializer(servicios, many=True).data
        
        # Si no tiene permisos, no incluir servicios
        return None

    def get_media(self, obj):
        """Obtener media del prestador solo si su plan lo permite"""
        plan = getattr(obj, 'plan', None)
        
        if plan and plan.puede_subir_media:
            media = obj.usuario.media_prestador.all()
            return MediaPrestadorSerializer(media, many=True).data
        
        return None
    
    def get_resenas(self, obj):
        """Obtener reseñas del prestador solo si su plan lo permite"""
        plan = getattr(obj, 'plan', None)
        
        if plan and plan.puede_recibir_resenas:
            resenas = obj.usuario.resenas_recibidas.all()
            return ResenaSerializer(resenas, many=True).data
        
        return None

    def get_plan_info(self, obj):
        """Obtener información del plan del prestador"""
        plan = getattr(obj, 'plan', None)
        
        if plan:
            from apps.usuarios.serializers import PlanSerializer
            return PlanSerializer(plan).data
        return None

    def to_representation(self, instance):
        """Filtra los campos de salida según los permisos del plan del prestador."""
        # Obtener la representación estándar de todos los campos
        data = super().to_representation(instance)
        
        # Obtener el plan del prestador para la lógica de filtrado
        plan = getattr(instance, 'plan', None)
        
        # Lista de campos que SIEMPRE se deben mostrar
        always_visible_fields = {
            'id', 'usuario', 'nombre_comercial', 'ciudad', 'provincia', 'plan_info', 
            'promedio_calificacion', 'es_prestador', 'categoria', 'rubro', 'fecha_registro'
        }
        
        if not plan:
            # Sin plan: solo mostrar campos básicos
            for key in list(data.keys()):
                if key not in always_visible_fields:
                    del data[key]
            return data

        # Con plan: aplicar filtros según permisos
        # 1. Filtrar campos de perfil basados en 'fields_enabled'
        allowed_profile_fields = set(plan.fields_enabled) if plan.fields_enabled else set()
        profile_fields_to_check = {'telefono', 'direccion', 'sitio_web', 'descripcion'}
        
        for field in profile_fields_to_check:
            if field not in allowed_profile_fields:
                if field in data:
                    del data[field]

        # 2. Filtrar media, reseñas y servicios si es None (no permitido)
        if data.get('media') is None:
            del data['media']
        if data.get('resenas') is None:
            del data['resenas']
        if data.get('servicios') is None:
            del data['servicios']
        
        return data
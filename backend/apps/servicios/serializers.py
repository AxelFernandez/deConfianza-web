from rest_framework import serializers
from .models import Categoria, Rubro, Servicio, Prestador, MediaPrestador, Resena
from apps.usuarios.models import Plan

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
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    rubro_nombre = serializers.CharField(source='rubro.nombre', read_only=True)
    
    class Meta:
        model = Servicio
        fields = ['id', 'prestador', 'prestador_username', 'nombre', 'descripcion', 'precio_base', 
                  'categoria', 'categoria_nombre', 'rubro', 'rubro_nombre', 'activo', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['prestador', 'fecha_creacion', 'fecha_actualizacion']

class MediaPrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaPrestador
        fields = '__all__'

    def validate(self, attrs):
        prestador = attrs.get('prestador')
        tipo = attrs.get('tipo')
        if not prestador or not tipo:
            return attrs

        user = prestador.usuario
        perfil = getattr(user, 'perfil', None)
        plan_code = getattr(perfil, 'plan', None)
        plan = Plan.objects.filter(code=plan_code).first() if plan_code else None

        if plan:
            if tipo == 'imagen':
                count_images = prestador.media.filter(tipo='imagen').count()
                if plan.max_images and count_images >= plan.max_images:
                    raise serializers.ValidationError({'archivo': 'Límite de imágenes alcanzado para tu plan'})
            if tipo == 'video':
                count_videos = prestador.media.filter(tipo='video').count()
                if plan.max_videos and count_videos >= plan.max_videos:
                    raise serializers.ValidationError({'archivo': 'Límite de videos alcanzado para tu plan'})

        return attrs

class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = '__all__'
        
    def create(self, validated_data):
        # Verificar si el prestador puede recibir reseñas según su plan
        prestador = validated_data['prestador']
        user = prestador.usuario
        perfil = getattr(user, 'perfil', None)
        plan = getattr(perfil, 'plan', None)
        
        if not plan or not plan.puede_recibir_resenas:
            raise serializers.ValidationError("Este prestador no acepta reseñas")
        return super().create(validated_data)

class PrestadorListSerializer(serializers.ModelSerializer):
    plan_nombre = serializers.SerializerMethodField()
    ubicacion = serializers.SerializerMethodField()
    servicios = serializers.SerializerMethodField()
    puntuacion = serializers.SerializerMethodField()
    
    class Meta:
        model = Prestador
        fields = ['id', 'nombre_comercial', 'direccion', 'ciudad', 'provincia', 
                  'telefono', 'sitio_web', 'plan_nombre', 'latitud', 'longitud',
                  'ubicacion', 'servicios', 'puntuacion']
    
    def get_plan_nombre(self, obj):
        user = obj.usuario
        perfil = getattr(user, 'perfil', None)
        plan = getattr(perfil, 'plan', None)
        return plan.name if plan else 'Gratuito'
    
    def get_ubicacion(self, obj):
        """Formatear ubicación para mostrar en la lista"""
        ubicacion_parts = []
        if obj.ciudad:
            ubicacion_parts.append(obj.ciudad)
        if obj.provincia:
            ubicacion_parts.append(obj.provincia)
        return ', '.join(ubicacion_parts) if ubicacion_parts else None
    
    def get_servicios(self, obj):
        """Obtener servicios activos del prestador"""
        servicios = Servicio.objects.filter(prestador=obj.usuario, activo=True)
        return ServicioSerializer(servicios, many=True).data
    
    def get_puntuacion(self, obj):
        """Calcular puntuación promedio de las reseñas"""
        resenas = obj.resenas.all()
        if not resenas:
            return 0
        return round(sum(r.calificacion for r in resenas) / resenas.count(), 1)

class PrestadorDetailSerializer(serializers.ModelSerializer):
    plan_info = serializers.SerializerMethodField()
    servicios = serializers.SerializerMethodField()
    media = MediaPrestadorSerializer(many=True, read_only=True)
    resenas = ResenaSerializer(many=True, read_only=True)
    promedio_calificacion = serializers.SerializerMethodField()
    
    class Meta:
        model = Prestador
        fields = '__all__'
        
    def get_promedio_calificacion(self, obj):
        resenas = obj.resenas.all()
        if not resenas:
            return 0
        return sum(r.calificacion for r in resenas) / resenas.count()
    
    def get_servicios(self, obj):
        servicios = Servicio.objects.filter(prestador=obj.usuario, activo=True)
        return ServicioSerializer(servicios, many=True).data
    
    def get_plan_info(self, obj):
        user = obj.usuario
        perfil = getattr(user, 'perfil', None)
        plan = getattr(perfil, 'plan', None)
        
        if plan:
            return {
                'code': plan.code,
                'name': plan.name,
                'price_text': plan.price_text,
                'precio_mensual': float(plan.precio_mensual),
            }
        return None



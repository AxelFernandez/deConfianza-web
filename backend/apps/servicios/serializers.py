from rest_framework import serializers
from .models import Categoria, Rubro, Servicio, RangoSuscripcion, Prestador, MediaPrestador, Resena, ServicioPrestador
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
    class Meta:
        model = Servicio
        fields = '__all__'

class RangoSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangoSuscripcion
        fields = '__all__'

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
        # Solo permitir reseñas si el prestador tiene un rango que lo permite
        prestador = validated_data['prestador']
        if not prestador.rango_suscripcion or not prestador.rango_suscripcion.permite_resenas:
            raise serializers.ValidationError("Este prestador no acepta reseñas")
        return super().create(validated_data)

class PrestadorListSerializer(serializers.ModelSerializer):
    rango = serializers.SerializerMethodField()
    
    class Meta:
        model = Prestador
        fields = ['id', 'nombre_comercial', 'direccion', 'ciudad', 'provincia', 
                  'telefono', 'sitio_web', 'rango', 'latitud', 'longitud']
    
    def get_rango(self, obj):
        if obj.rango_suscripcion:
            return obj.rango_suscripcion.rango
        return 1

class PrestadorDetailSerializer(serializers.ModelSerializer):
    rango_suscripcion = RangoSuscripcionSerializer(read_only=True)
    servicios = ServicioSerializer(many=True, read_only=True)
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


class ServicioPrestadorSerializer(serializers.ModelSerializer):
    servicio_base_nombre = serializers.CharField(source='servicio_base.nombre', read_only=True)
    prestador_username = serializers.CharField(source='prestador.username', read_only=True)
    
    class Meta:
        model = ServicioPrestador
        fields = ['id', 'prestador', 'prestador_username', 'nombre', 'descripcion', 'precio_base', 
                  'servicio_base', 'servicio_base_nombre', 'activo', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['prestador', 'fecha_creacion', 'fecha_actualizacion']

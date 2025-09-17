from rest_framework import serializers
from .models import Categoria, Rubro, Servicio, RangoSuscripcion, Prestador, MediaPrestador, Resena

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

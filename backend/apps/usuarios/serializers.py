from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion', 'ciudad', 'provincia', 'pais', 'es_prestador']

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

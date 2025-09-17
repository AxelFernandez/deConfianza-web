from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    """Perfil extendido para los usuarios"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, default="Argentina")
    es_prestador = models.BooleanField(default=False)
    
    def __str__(self):
        return self.usuario.username
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

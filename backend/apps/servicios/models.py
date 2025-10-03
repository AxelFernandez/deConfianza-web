from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    """Categoría general (Oficios o Profesiones)"""
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class Rubro(models.Model):
    """Rubros o áreas de servicios (ej: Gastronomía, Construcción, etc.)"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='rubros')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Rubro'
        verbose_name_plural = 'Rubros'

class Servicio(models.Model):
    """Servicios que ofrece un prestador"""
    prestador = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='servicios_creados')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.prestador.username} - {self.nombre}"
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'


class MediaPrestador(models.Model):
    """Imágenes y videos del prestador"""
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]
    
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='media_prestador', null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='prestadores/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.usuario:
            nombre = self.usuario.get_full_name() or self.usuario.username
        else:
            nombre = "Usuario eliminado"
        return f"{self.titulo} - {nombre}"
    
    class Meta:
        verbose_name = 'Media del Prestador'
        verbose_name_plural = 'Media de los Prestadores'

class Resena(models.Model):
    """Reseñas de usuarios sobre prestadores"""
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='resenas_recibidas', null=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.usuario:
            nombre = self.usuario.get_full_name() or self.usuario.username
        else:
            nombre = "Usuario eliminado"
        return f"{nombre} - {self.calificacion}/5"
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'




class VisualizacionPerfil(models.Model):
    """Registro de visualizaciones del perfil del prestador"""
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='visualizaciones_perfil', null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.usuario:
            nombre = self.usuario.get_full_name() or self.usuario.username
        else:
            nombre = "Usuario eliminado"
        return f"{nombre} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = 'Visualización de Perfil'
        verbose_name_plural = 'Visualizaciones de Perfiles'

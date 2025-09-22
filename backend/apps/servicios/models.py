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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='servicios')
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, related_name='servicios')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.prestador.username} - {self.nombre}"
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

class Prestador(models.Model):
    """Prestador de servicios"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_comercial = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True)
    sitio_web = models.URLField(blank=True)
    descripcion = models.TextField(blank=True)
    redes_sociales = models.JSONField(default=dict, blank=True)
    fecha_inicio_suscripcion = models.DateField(null=True, blank=True)
    fecha_fin_suscripcion = models.DateField(null=True, blank=True)
    
    # Ubicación geográfica
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default="Argentina")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre_comercial
    
    class Meta:
        verbose_name = 'Prestador'
        verbose_name_plural = 'Prestadores'

class MediaPrestador(models.Model):
    """Imágenes y videos del prestador"""
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]
    
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='media')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='prestadores/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.prestador.nombre_comercial}"
    
    class Meta:
        verbose_name = 'Media del Prestador'
        verbose_name_plural = 'Media de los Prestadores'

class Resena(models.Model):
    """Reseñas de usuarios sobre prestadores"""
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='resenas')
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.prestador.nombre_comercial} - {self.calificacion}/5"
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'




class VisualizacionPerfil(models.Model):
    """Registro de visualizaciones del perfil del prestador"""
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, related_name='visualizaciones')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.prestador.nombre_comercial} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = 'Visualización de Perfil'
        verbose_name_plural = 'Visualizaciones de Perfiles'

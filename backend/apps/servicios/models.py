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
    """Servicios específicos (ej: Plomería, Abogacía, etc.)"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, related_name='servicios')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

class RangoSuscripcion(models.Model):
    """Rangos de suscripción disponibles"""
    RANGO_CHOICES = [
        (1, 'Rango 1 - Gratuito'),
        (2, 'Rango 2 - Básico'),
        (3, 'Rango 3 - Premium'),
        (4, 'Rango 4 - Destacado'),
    ]
    
    nombre = models.CharField(max_length=50)
    rango = models.IntegerField(choices=RANGO_CHOICES, unique=True)
    precio_usd = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    descripcion = models.TextField()
    limite_imagenes = models.IntegerField(default=0)
    limite_videos = models.IntegerField(default=0)
    permite_resenas = models.BooleanField(default=False)
    asesoria_empresarial = models.BooleanField(default=False)
    acceso_informes = models.BooleanField(default=False)
    posicion_destacada = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Rango de Suscripción'
        verbose_name_plural = 'Rangos de Suscripción'

class Prestador(models.Model):
    """Prestador de servicios"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_comercial = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True)
    sitio_web = models.URLField(blank=True)
    descripcion = models.TextField(blank=True)
    redes_sociales = models.JSONField(default=dict, blank=True)
    servicios = models.ManyToManyField(Servicio, related_name='prestadores')
    rango_suscripcion = models.ForeignKey(RangoSuscripcion, on_delete=models.SET_NULL, null=True)
    fecha_inicio_suscripcion = models.DateField(null=True, blank=True)
    fecha_fin_suscripcion = models.DateField(null=True, blank=True)
    
    # Ubicación geográfica
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default="Argentina")
    
    # Campos adicionales para rangos superiores
    mision = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    valores = models.TextField(blank=True)
    tarifario = models.JSONField(default=dict, blank=True)
    
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


class ServicioPrestador(models.Model):
    """Servicios personalizados que ofrece un prestador"""
    prestador = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='servicios_prestador')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    servicio_base = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, blank=True, 
                                      help_text="Servicio del catálogo como referencia")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.prestador.username} - {self.nombre}"
    
    class Meta:
        verbose_name = 'Servicio del Prestador'
        verbose_name_plural = 'Servicios de los Prestadores'

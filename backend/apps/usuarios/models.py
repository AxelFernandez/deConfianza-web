from django.db import models
from django.contrib.auth.models import User

PROFILE_FIELD_CHOICES = [
    "telefono",
    "direccion",
    "ciudad",
    "provincia",
    "sitio_web",
    "descripcion",
]
class Perfil(models.Model):
    """Perfil extendido para los usuarios"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, default="Argentina")
    es_prestador = models.BooleanField(default=False)
    # Categoría y rubro para prestadores
    categoria = models.ForeignKey('servicios.Categoria', on_delete=models.SET_NULL, null=True, blank=True)
    rubro = models.ForeignKey('servicios.Rubro', on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True, help_text="Plan de suscripción del usuario")
    onboarding_completed = models.BooleanField(default=False)
    # Campo para identificar cuentas vinculadas a redes sociales
    social_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID de la cuenta social (Google, Facebook, etc.)")
    social_provider = models.CharField(max_length=50, blank=True, null=True, help_text="Proveedor social (google, facebook, etc.)")


class Plan(models.Model):
    """Planes de suscripción configurables desde base de datos"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    price_text = models.CharField(max_length=50, default="Gratis")
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Precio mensual en pesos argentinos")
    fields_enabled = models.JSONField(default=list)
    max_images = models.PositiveIntegerField(default=0)
    max_videos = models.PositiveIntegerField(default=0)
    
    # Permisos específicos
    puede_crear_servicios = models.BooleanField(default=True, help_text="Permite crear servicios personalizados")
    puede_recibir_resenas = models.BooleanField(default=True, help_text="Permite recibir y mostrar reseñas")
    puede_subir_media = models.BooleanField(default=True, help_text="Permite subir fotos y videos")
    puede_ver_estadisticas = models.BooleanField(default=True, help_text="Permite ver estadísticas detalladas")
    max_servicios = models.PositiveIntegerField(default=1, help_text="Número máximo de servicios que puede crear")
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} ({'activo' if self.is_active else 'inactivo'})"

    def clean(self):
        # Asegurar que fields_enabled sea una lista y sus valores válidos
        if not isinstance(self.fields_enabled, list):
            self.fields_enabled = []
        self.fields_enabled = [f for f in self.fields_enabled if f in PROFILE_FIELD_CHOICES]


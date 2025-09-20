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
    PLAN_CHOICES = [
        ("free", "Free"),
        ("basic", "Basic"),
        ("pro", "Pro"),
    ]
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    onboarding_completed = models.BooleanField(default=False)


class Plan(models.Model):
    """Planes de suscripción configurables desde base de datos"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    price_text = models.CharField(max_length=50, default="Gratis")
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Precio mensual en pesos argentinos")
    benefits = models.JSONField(default=list)
    fields_enabled = models.JSONField(default=list)
    max_images = models.PositiveIntegerField(default=0)
    max_videos = models.PositiveIntegerField(default=0)
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


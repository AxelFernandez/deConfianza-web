from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Suscripcion(models.Model):
    """Modelo para manejar las suscripciones de MercadoPago"""
    
    ESTADO_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('authorized', 'Autorizado'),
        ('in_process', 'En proceso'),
        ('in_mediation', 'En mediación'),
        ('rejected', 'Rechazado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
        ('charged_back', 'Contracargo'),
        ('active', 'Activo'),
    ]
    
    # Relaciones
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suscripciones')
    plan = models.ForeignKey('usuarios.Plan', on_delete=models.CASCADE)
    
    # Datos de MercadoPago
    mp_payment_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    mp_preference_id = models.CharField(max_length=100, null=True, blank=True)
    mp_external_reference = models.CharField(max_length=200, null=True, blank=True)
    
    # Estado y fechas
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pending')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    
    # Control
    activa = models.BooleanField(default=False)
    procesada = models.BooleanField(default=False)  # Para evitar procesar el mismo webhook múltiples veces
    
    # Metadatos adicionales de MP
    mp_metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Suscripción'
        verbose_name_plural = 'Suscripciones'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.plan.name} ({self.get_estado_display()})"
    
    def activar_suscripcion(self):
        """Activa la suscripción y actualiza el plan del usuario"""
        if self.estado == 'approved' and not self.activa:
            self.activa = True
            self.fecha_inicio = timezone.now()
            self.fecha_fin = self.fecha_inicio + timedelta(days=30)  # 1 mes
            
            # Actualizar el plan del usuario
            perfil = self.usuario.perfil
            perfil.plan = self.plan
            perfil.save()
            
            self.save()
            return True
        return False
    
    def desactivar_suscripcion(self):
        """Desactiva la suscripción"""
        if self.activa:
            self.activa = False
            # Opcional: volver al plan gratuito
            from apps.usuarios.models import Plan
            perfil = self.usuario.perfil
            try:
                plan_free = Plan.objects.get(code='free', is_active=True)
                perfil.plan = plan_free
            except Plan.DoesNotExist:
                perfil.plan = None
            perfil.save()
            self.save()
            return True
        return False
    
    @property
    def esta_vigente(self):
        """Verifica si la suscripción está vigente"""
        if not self.activa or not self.fecha_fin:
            return False
        return timezone.now() <= self.fecha_fin
    
    @property
    def dias_restantes(self):
        """Calcula los días restantes de la suscripción"""
        if not self.esta_vigente:
            return 0
        return (self.fecha_fin - timezone.now()).days


class LogWebhook(models.Model):
    """Log de webhooks recibidos de MercadoPago para debugging"""
    
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50)
    data_id = models.CharField(max_length=100, null=True, blank=True)
    payload = models.JSONField()
    procesado = models.BooleanField(default=False)
    error = models.TextField(null=True, blank=True)
    suscripcion = models.ForeignKey(Suscripcion, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Log de Webhook'
        verbose_name_plural = 'Logs de Webhooks'
    
    def __str__(self):
        return f"{self.tipo} - {self.fecha.strftime('%Y-%m-%d %H:%M')} ({'✓' if self.procesado else '✗'})"

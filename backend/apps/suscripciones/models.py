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
    mp_preference_id = models.CharField(max_length=100, null=True, blank=True)  # Para pagos únicos o preapproval_id para suscripciones
    mp_external_reference = models.CharField(max_length=200, null=True, blank=True)
    
    # Campos específicos para suscripciones automáticas
    is_recurring = models.BooleanField(default=False, help_text="True si es una suscripción automática")
    preapproval_id = models.CharField(max_length=100, null=True, blank=True, help_text="ID del preapproval de MercadoPago")
    
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
        """Activa la suscripción"""
        if self.estado == 'approved' and not self.activa:
            self.activa = True
            self.fecha_inicio = timezone.now()
            self.fecha_fin = self.fecha_inicio + timedelta(days=30)  # 1 mes
            
            # Ya no necesitamos sincronizar con perfil.plan
            # El plan se obtiene dinámicamente desde la suscripción activa
            
            self.save()
            return True
        return False
    
    def desactivar_suscripcion(self):
        """Desactiva la suscripción"""
        if self.activa:
            self.activa = False
            # Ya no necesitamos actualizar perfil.plan
            # El plan se calculará dinámicamente (volverá al plan gratuito automáticamente)
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


class CambioPlanProgramado(models.Model):
    """Modelo para manejar cambios de plan programados (downgrades)"""
    
    ESTADO_CHOICES = [
        ('pending', 'Pendiente'),
        ('processed', 'Procesado'),
        ('cancelled', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cambios_plan')
    plan_actual = models.ForeignKey('usuarios.Plan', on_delete=models.CASCADE, related_name='cambios_desde')
    plan_nuevo = models.ForeignKey('usuarios.Plan', on_delete=models.CASCADE, related_name='cambios_hacia')
    suscripcion_actual = models.ForeignKey(Suscripcion, on_delete=models.CASCADE, related_name='cambios_programados')
    
    # Fechas
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_programada = models.DateTimeField(help_text="Fecha en que se aplicará el cambio")
    fecha_procesado = models.DateTimeField(null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pending')
    es_upgrade = models.BooleanField(default=False, help_text="True si es upgrade, False si es downgrade")
    
    # Notas
    notas = models.TextField(blank=True, help_text="Notas adicionales sobre el cambio")
    
    class Meta:
        ordering = ['-fecha_solicitud']
        verbose_name = 'Cambio de Plan Programado'
        verbose_name_plural = 'Cambios de Plan Programados'
    
    def __str__(self):
        tipo = "Upgrade" if self.es_upgrade else "Downgrade"
        return f"{self.usuario.username}: {self.plan_actual.name} → {self.plan_nuevo.name} ({tipo}) - {self.get_estado_display()}"
    
    def procesar_cambio(self):
        """Procesa el cambio de plan"""
        if self.estado != 'pending':
            return False
        
        try:
            # Desactivar suscripción actual
            self.suscripcion_actual.desactivar_suscripcion()
            
            # Crear nueva suscripción con el nuevo plan
            nueva_suscripcion = Suscripcion.objects.create(
                usuario=self.usuario,
                plan=self.plan_nuevo,
                estado='approved',
                monto=self.plan_nuevo.precio_mensual,
                activa=True,
                fecha_inicio=timezone.now(),
                fecha_fin=timezone.now() + timedelta(days=30),
                fecha_pago=timezone.now()
            )
            
            # Marcar cambio como procesado
            self.estado = 'processed'
            self.fecha_procesado = timezone.now()
            self.save()
            
            return True
        except Exception as e:
            self.notas += f"\nError al procesar: {str(e)}"
            self.save()
            return False
    
    def cancelar_cambio(self):
        """Cancela el cambio programado"""
        if self.estado == 'pending':
            self.estado = 'cancelled'
            self.save()
            return True
        return False


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

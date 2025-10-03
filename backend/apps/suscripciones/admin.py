from django.contrib import admin
from django.utils.html import format_html
from .models import Suscripcion, LogWebhook, CambioPlanProgramado


@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'usuario_info', 'plan_info', 'estado_badge', 'monto', 
        'activa', 'fecha_creacion', 'fecha_pago', 'dias_restantes_info'
    )
    list_filter = ('estado', 'activa', 'plan__name', 'fecha_creacion', 'fecha_pago')
    search_fields = ('usuario__username', 'usuario__email', 'mp_payment_id', 'mp_external_reference')
    readonly_fields = (
        'mp_payment_id', 'mp_preference_id', 'mp_external_reference', 
        'fecha_creacion', 'fecha_pago', 'procesada', 'mp_metadata'
    )
    list_editable = ('activa',)
    ordering = ('-fecha_creacion',)
    
    fieldsets = (
        ('Información General', {
            'fields': ('usuario', 'plan', 'estado', 'monto', 'activa')
        }),
        ('MercadoPago', {
            'fields': ('mp_payment_id', 'mp_preference_id', 'mp_external_reference', 'procesada'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_pago', 'fecha_inicio', 'fecha_fin')
        }),
        ('Metadatos', {
            'fields': ('mp_metadata',),
            'classes': ('collapse',)
        })
    )
    
    def usuario_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.usuario.username,
            obj.usuario.email
        )
    usuario_info.short_description = 'Usuario'
    
    def plan_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>${}</small>',
            obj.plan.name,
            obj.plan.precio_mensual
        )
    plan_info.short_description = 'Plan'
    
    def estado_badge(self, obj):
        colors = {
            'pending': '#fbbf24',      # amarillo
            'approved': '#10b981',     # verde
            'authorized': '#10b981',   # verde
            'in_process': '#3b82f6',   # azul
            'in_mediation': '#f59e0b', # naranja
            'rejected': '#ef4444',     # rojo
            'cancelled': '#6b7280',    # gris
            'refunded': '#8b5cf6',     # morado
            'charged_back': '#dc2626', # rojo oscuro
        }
        color = colors.get(obj.estado, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def dias_restantes_info(self, obj):
        if not obj.activa:
            return format_html('<span style="color: #6b7280;">Inactiva</span>')
        
        if obj.esta_vigente:
            dias = obj.dias_restantes
            if dias > 7:
                color = '#10b981'  # verde
            elif dias > 3:
                color = '#f59e0b'  # naranja
            else:
                color = '#ef4444'  # rojo
            
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} días</span>',
                color,
                dias
            )
        else:
            return format_html('<span style="color: #ef4444;">Vencida</span>')
    
    dias_restantes_info.short_description = 'Vigencia'
    
    actions = ['activar_suscripciones', 'desactivar_suscripciones']
    
    def activar_suscripciones(self, request, queryset):
        count = 0
        for suscripcion in queryset:
            if suscripcion.estado == 'approved' and suscripcion.activar_suscripcion():
                count += 1
        
        self.message_user(request, f'{count} suscripciones activadas correctamente.')
    activar_suscripciones.short_description = 'Activar suscripciones seleccionadas'
    
    def desactivar_suscripciones(self, request, queryset):
        count = 0
        for suscripcion in queryset:
            if suscripcion.desactivar_suscripcion():
                count += 1
        
        self.message_user(request, f'{count} suscripciones desactivadas correctamente.')
    desactivar_suscripciones.short_description = 'Desactivar suscripciones seleccionadas'


@admin.register(LogWebhook)
class LogWebhookAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'tipo', 'data_id', 'procesado_badge', 'suscripcion_link', 'error_preview')
    list_filter = ('tipo', 'procesado', 'fecha')
    search_fields = ('data_id', 'tipo', 'error')
    readonly_fields = ('fecha', 'payload')
    ordering = ('-fecha',)
    
    fieldsets = (
        ('Información General', {
            'fields': ('fecha', 'tipo', 'data_id', 'procesado', 'suscripcion')
        }),
        ('Datos', {
            'fields': ('payload',),
            'classes': ('collapse',)
        }),
        ('Error', {
            'fields': ('error',),
            'classes': ('collapse',)
        })
    )
    
    def procesado_badge(self, obj):
        if obj.procesado:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">✓ Procesado</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">✗ Pendiente</span>'
            )
    procesado_badge.short_description = 'Estado'
    
    def suscripcion_link(self, obj):
        if obj.suscripcion:
            return format_html(
                '<a href="/admin/suscripciones/suscripcion/{}/change/">Suscripción #{}</a>',
                obj.suscripcion.id,
                obj.suscripcion.id
            )
        return '-'
    suscripcion_link.short_description = 'Suscripción'
    
    def error_preview(self, obj):
        if obj.error:
            preview = obj.error[:50]
            if len(obj.error) > 50:
                preview += '...'
            return format_html('<span style="color: #ef4444;">{}</span>', preview)
        return '-'
    error_preview.short_description = 'Error'


@admin.register(CambioPlanProgramado)
class CambioPlanProgramadoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'usuario_info', 'cambio_info', 'tipo_badge', 'estado_badge', 
        'fecha_programada', 'dias_hasta_cambio', 'fecha_solicitud'
    )
    list_filter = ('estado', 'es_upgrade', 'fecha_programada', 'fecha_solicitud')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('fecha_solicitud', 'fecha_procesado')
    ordering = ('fecha_programada', '-fecha_solicitud')
    
    fieldsets = (
        ('Información del Cambio', {
            'fields': ('usuario', 'plan_actual', 'plan_nuevo', 'suscripcion_actual', 'es_upgrade')
        }),
        ('Fechas', {
            'fields': ('fecha_solicitud', 'fecha_programada', 'fecha_procesado')
        }),
        ('Estado', {
            'fields': ('estado', 'notas')
        })
    )
    
    def usuario_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.usuario.username,
            obj.usuario.email
        )
    usuario_info.short_description = 'Usuario'
    
    def cambio_info(self, obj):
        return format_html(
            '<strong>{}</strong> → <strong>{}</strong><br>'
            '<small>${} → ${}</small>',
            obj.plan_actual.name,
            obj.plan_nuevo.name,
            obj.plan_actual.precio_mensual,
            obj.plan_nuevo.precio_mensual
        )
    cambio_info.short_description = 'Cambio'
    
    def tipo_badge(self, obj):
        if obj.es_upgrade:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">▲ Upgrade</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #f59e0b; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">▼ Downgrade</span>'
            )
    tipo_badge.short_description = 'Tipo'
    
    def estado_badge(self, obj):
        colors = {
            'pending': '#fbbf24',    # amarillo
            'processed': '#10b981',  # verde
            'cancelled': '#6b7280',  # gris
        }
        color = colors.get(obj.estado, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def dias_hasta_cambio(self, obj):
        from django.utils import timezone
        if obj.estado != 'pending':
            return '-'
        
        dias = (obj.fecha_programada - timezone.now()).days
        if dias < 0:
            return format_html('<span style="color: #ef4444;">Vencido</span>')
        elif dias == 0:
            return format_html('<span style="color: #f59e0b; font-weight: bold;">Hoy</span>')
        else:
            return format_html('<span style="color: #3b82f6;">{} días</span>', dias)
    dias_hasta_cambio.short_description = 'Tiempo Restante'
    
    actions = ['procesar_cambios', 'cancelar_cambios']
    
    def procesar_cambios(self, request, queryset):
        count = 0
        for cambio in queryset.filter(estado='pending'):
            if cambio.procesar_cambio():
                count += 1
        
        self.message_user(request, f'{count} cambios procesados correctamente.')
    procesar_cambios.short_description = 'Procesar cambios seleccionados'
    
    def cancelar_cambios(self, request, queryset):
        count = 0
        for cambio in queryset.filter(estado='pending'):
            if cambio.cancelar_cambio():
                count += 1
        
        self.message_user(request, f'{count} cambios cancelados correctamente.')
    cancelar_cambios.short_description = 'Cancelar cambios seleccionados'

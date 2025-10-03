"""
Vista para comparar sistemas de pago único vs suscripciones automáticas
Solo para testing y demostración
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Suscripcion
from apps.usuarios.models import Plan


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comparar_sistemas_pago(request):
    """
    API para comparar ambos sistemas de pago y ver recomendaciones
    """
    
    # Obtener estadísticas actuales
    total_suscripciones = Suscripcion.objects.count()
    suscripciones_activas = Suscripcion.objects.filter(activa=True).count()
    suscripciones_recurrentes = Suscripcion.objects.filter(is_recurring=True).count()
    suscripciones_manuales = total_suscripciones - suscripciones_recurrentes
    
    # Obtener planes disponibles
    planes = Plan.objects.filter(is_active=True)
    planes_data = []
    
    for plan in planes:
        planes_data.append({
            'code': plan.code,
            'name': plan.name,
            'precio_mensual': float(plan.precio_mensual),
            'is_free': plan.precio_mensual <= 0,
            'descripcion': f"Plan {plan.name} - ${plan.precio_mensual}/mes" if plan.precio_mensual > 0 else "Plan Gratuito"
        })
    
    # URLs de las APIs
    apis_disponibles = {
        'pago_unico': {
            'url': '/api/suscripciones/crear-preferencia/',
            'description': 'Sistema actual - Pago único mensual',
            'method': 'POST',
            'body': {'plan': 'full'},
            'renovacion_automatica': False,
            'experiencia_usuario': 'Regular - Usuario debe renovar manualmente'
        },
        'suscripcion_automatica': {
            'url': '/api/suscripciones/crear-suscripcion/',
            'description': 'Sistema nuevo - Suscripción automática',
            'method': 'POST',
            'body': {'plan': 'full'},
            'renovacion_automatica': True,
            'experiencia_usuario': 'Excelente - Renovación automática'
        }
    }
    
    # Recomendaciones
    recomendaciones = []
    
    if suscripciones_recurrentes == 0:
        recomendaciones.append({
            'tipo': 'implementacion',
            'titulo': 'Implementar Suscripciones Automáticas',
            'descripcion': 'No tienes suscripciones automáticas. Te recomendamos implementarlas para mejor retención.',
            'prioridad': 'alta'
        })
    
    if suscripciones_manuales > suscripciones_recurrentes:
        recomendaciones.append({
            'tipo': 'migracion',
            'titulo': 'Migrar a Suscripciones Automáticas',
            'descripcion': f'Tienes {suscripciones_manuales} suscripciones manuales vs {suscripciones_recurrentes} automáticas.',
            'prioridad': 'media'
        })
    
    # Beneficios de suscripciones automáticas
    beneficios = [
        'Renovación automática mensual - Sin intervención del usuario',
        'Mayor retención de clientes - Menos abandono por olvido',
        'Flujo de caja predecible - Ingresos recurrentes garantizados',
        'Mejor experiencia de usuario - Una sola autorización',
        'Menos trabajo administrativo - Sin recordatorios de renovación'
    ]
    
    return Response({
        'estadisticas': {
            'total_suscripciones': total_suscripciones,
            'suscripciones_activas': suscripciones_activas,
            'suscripciones_recurrentes': suscripciones_recurrentes,
            'suscripciones_manuales': suscripciones_manuales,
            'porcentaje_automaticas': round((suscripciones_recurrentes / max(total_suscripciones, 1)) * 100, 1)
        },
        'planes_disponibles': planes_data,
        'apis_disponibles': apis_disponibles,
        'recomendaciones': recomendaciones,
        'beneficios_suscripciones_automaticas': beneficios,
        'configuracion_requerida': {
            'webhooks': [
                'preapproval - Para eventos de suscripción',
                'authorized_payment - Para pagos automáticos'
            ],
            'url_webhook': '/api/suscripciones/webhook/suscripciones/',
            'variables_entorno': [
                'MERCADOPAGO_ACCESS_TOKEN',
                'MERCADOPAGO_PUBLIC_KEY'
            ]
        },
        'documentacion': '/static/README_SUSCRIPCIONES.md'
    })


@api_view(['GET'])
def demo_flujo_suscripciones(request):
    """
    Demo del flujo de suscripciones automáticas (sin autenticación para testing)
    """
    
    flujo_demo = {
        'paso_1': {
            'titulo': 'Usuario elige plan',
            'accion': 'Frontend llama a /api/suscripciones/crear-suscripcion/',
            'resultado': 'Recibe init_point de MercadoPago'
        },
        'paso_2': {
            'titulo': 'Usuario autoriza débito',
            'accion': 'Usuario va a init_point y autoriza débito automático',
            'resultado': 'MercadoPago envía webhook preapproval con status=authorized'
        },
        'paso_3': {
            'titulo': 'Sistema activa suscripción',
            'accion': 'Webhook procesa autorización',
            'resultado': 'Suscripción se activa inmediatamente'
        },
        'paso_4': {
            'titulo': 'Cobro automático mensual',
            'accion': 'MercadoPago cobra automáticamente cada mes',
            'resultado': 'Webhook authorized_payment extiende suscripción'
        },
        'paso_5_opcional': {
            'titulo': 'Cancelación',
            'accion': 'Usuario cancela desde el dashboard',
            'resultado': 'Sistema cancela preapproval en MercadoPago'
        }
    }
    
    ejemplos_webhook = {
        'preapproval_authorized': {
            'type': 'preapproval',
            'action': 'updated',
            'data': {'id': 'preapproval_id'},
            'descripcion': 'Usuario autorizó débito automático'
        },
        'payment_approved': {
            'type': 'authorized_payment',
            'action': 'created',
            'data': {'id': 'payment_id'},
            'descripcion': 'Pago mensual automático exitoso'
        }
    }
    
    return Response({
        'titulo': 'Demo - Flujo de Suscripciones Automáticas',
        'flujo_completo': flujo_demo,
        'ejemplos_webhooks': ejemplos_webhook,
        'ventajas': [
            'Una sola autorización del usuario',
            'Pagos automáticos mensuales',
            'Sin recordatorios ni gestión manual',
            'Mejor retención de clientes'
        ],
        'consideraciones': [
            'Requiere configurar webhooks adicionales',
            'Usuario puede cancelar en cualquier momento',
            'Fallos de pago (tarjeta sin fondos) se manejan automáticamente'
        ]
    })

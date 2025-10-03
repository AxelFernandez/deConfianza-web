"""
Utilidades para manejar suscripciones y cambios de plan
"""

from decimal import Decimal
from django.utils import timezone
from datetime import timedelta


def calcular_prorrateo(suscripcion_actual, plan_nuevo):
    """
    Calcula el monto de prorrateo para un upgrade de plan.
    
    Args:
        suscripcion_actual: Instancia de Suscripcion actual
        plan_nuevo: Instancia de Plan al que se quiere cambiar
    
    Returns:
        dict con:
            - monto_a_pagar: Decimal con el monto a cobrar
            - dias_restantes: int con días restantes del ciclo
            - credito_plan_actual: Decimal del crédito por días no usados
            - costo_plan_nuevo: Decimal del costo prorrateado del plan nuevo
            - detalle: str con explicación del cálculo
    """
    
    # Validar que la suscripción esté vigente
    if not suscripcion_actual.esta_vigente:
        return {
            'monto_a_pagar': Decimal('0'),
            'dias_restantes': 0,
            'credito_plan_actual': Decimal('0'),
            'costo_plan_nuevo': Decimal('0'),
            'detalle': 'La suscripción actual no está vigente',
            'error': True
        }
    
    # Calcular días restantes
    dias_restantes = (suscripcion_actual.fecha_fin - timezone.now()).days
    
    # Si quedan 0 días o menos, no hay prorrateo
    if dias_restantes <= 0:
        return {
            'monto_a_pagar': plan_nuevo.precio_mensual,
            'dias_restantes': 0,
            'credito_plan_actual': Decimal('0'),
            'costo_plan_nuevo': plan_nuevo.precio_mensual,
            'detalle': 'Suscripción vencida. Se cobrará el mes completo del nuevo plan.',
            'error': False
        }
    
    # Calcular costo diario de ambos planes
    costo_diario_actual = suscripcion_actual.plan.precio_mensual / 30
    costo_diario_nuevo = plan_nuevo.precio_mensual / 30
    
    # Calcular crédito del plan actual (lo que ya pagó y no usó)
    credito_plan_actual = costo_diario_actual * dias_restantes
    
    # Calcular costo del plan nuevo para los días restantes
    costo_plan_nuevo = costo_diario_nuevo * dias_restantes
    
    # Monto a pagar es la diferencia
    monto_a_pagar = costo_plan_nuevo - credito_plan_actual
    
    # Asegurar que nunca sea negativo
    monto_a_pagar = max(monto_a_pagar, Decimal('0'))
    
    # Generar detalle
    detalle = f"""
Días restantes en tu ciclo actual: {dias_restantes} días
Plan actual ({suscripcion_actual.plan.name}): ${float(suscripcion_actual.plan.precio_mensual):.2f}/mes (${float(costo_diario_actual):.2f}/día)
Nuevo plan ({plan_nuevo.name}): ${float(plan_nuevo.precio_mensual):.2f}/mes (${float(costo_diario_nuevo):.2f}/día)

Crédito por días no usados: ${float(credito_plan_actual):.2f}
Costo del nuevo plan por {dias_restantes} días: ${float(costo_plan_nuevo):.2f}
Monto a pagar hoy: ${float(monto_a_pagar):.2f}

Tu nuevo plan será válido por {dias_restantes} días, luego se renovará automáticamente al precio completo.
    """.strip()
    
    return {
        'monto_a_pagar': monto_a_pagar,
        'dias_restantes': dias_restantes,
        'credito_plan_actual': credito_plan_actual,
        'costo_plan_nuevo': costo_plan_nuevo,
        'costo_diario_actual': costo_diario_actual,
        'costo_diario_nuevo': costo_diario_nuevo,
        'detalle': detalle,
        'error': False
    }


def determinar_tipo_cambio(plan_actual, plan_nuevo):
    """
    Determina si el cambio es upgrade o downgrade.
    
    Args:
        plan_actual: Instancia de Plan actual
        plan_nuevo: Instancia de Plan nuevo
    
    Returns:
        str: 'upgrade', 'downgrade', o 'same'
    """
    if plan_nuevo.precio_mensual > plan_actual.precio_mensual:
        return 'upgrade'
    elif plan_nuevo.precio_mensual < plan_actual.precio_mensual:
        return 'downgrade'
    else:
        return 'same'


def calcular_fecha_proximo_cobro(suscripcion):
    """
    Calcula la fecha del próximo cobro de una suscripción.
    
    Args:
        suscripcion: Instancia de Suscripcion
    
    Returns:
        datetime: Fecha del próximo cobro
    """
    if not suscripcion or not suscripcion.fecha_fin:
        return None
    
    return suscripcion.fecha_fin


def obtener_suscripcion_activa(usuario):
    """
    Obtiene la suscripción activa de un usuario.
    
    Args:
        usuario: Instancia de User
    
    Returns:
        Suscripcion o None
    """
    from .models import Suscripcion
    
    return Suscripcion.objects.filter(
        usuario=usuario,
        activa=True,
        fecha_fin__gt=timezone.now()
    ).select_related('plan').first()


def puede_cambiar_plan(usuario, plan_nuevo):
    """
    Verifica si un usuario puede cambiar a un plan específico.
    
    Args:
        usuario: Instancia de User
        plan_nuevo: Instancia de Plan
    
    Returns:
        dict con:
            - puede: bool
            - razon: str con la razón si no puede
    """
    suscripcion_actual = obtener_suscripcion_activa(usuario)
    
    if not suscripcion_actual:
        return {
            'puede': False,
            'razon': 'No tienes una suscripción activa'
        }
    
    if suscripcion_actual.plan.id == plan_nuevo.id:
        return {
            'puede': False,
            'razon': 'Ya tienes este plan activo'
        }
    
    # Verificar si ya tiene un cambio programado pendiente
    from .models import CambioPlanProgramado
    
    cambio_pendiente = CambioPlanProgramado.objects.filter(
        usuario=usuario,
        estado='pending'
    ).first()
    
    if cambio_pendiente:
        return {
            'puede': False,
            'razon': f'Ya tienes un cambio programado para el {cambio_pendiente.fecha_programada.strftime("%d/%m/%Y")}'
        }
    
    return {
        'puede': True,
        'razon': None
    }


def formatear_precio(precio):
    """
    Formatea un precio para mostrar en la UI.
    
    Args:
        precio: Decimal o float
    
    Returns:
        str: Precio formateado
    """
    return f"${float(precio):,.2f}"

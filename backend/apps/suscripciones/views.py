import logging
import mercadopago
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.usuarios.models import Plan
from .models import Suscripcion, LogWebhook

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_preferencia_pago(request):
    """Crear preferencia de pago en MercadoPago"""
    plan_code = request.data.get('plan')
    
    if not plan_code:
        return Response({'error': 'Plan requerido'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        plan = Plan.objects.get(code=plan_code, is_active=True)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # Verificar que el plan tenga precio
    if plan.precio_mensual <= 0:
        return Response({'error': 'Plan gratuito no requiere pago'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Configurar MercadoPago
    if not settings.MERCADOPAGO_ACCESS_TOKEN:
        return Response({'error': 'MercadoPago no configurado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    # Crear external_reference único
    external_reference = f"{request.user.id}_{plan.code}_{int(timezone.now().timestamp())}"
    
    # Crear preferencia
    preference_data = {
        "items": [
            {
                "title": f"Suscripción {plan.name}",
                "description": f"Plan {plan.name} - DeConfianza (1 mes)",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": float(plan.precio_mensual)
            }
        ],
        "payer": {
            "name": request.user.first_name or "Usuario",
            "surname": request.user.last_name or "DeConfianza",
            "email": request.user.email,
        },
        "back_urls": {
            "success": f"{settings.FRONTEND_URL}/suscripcion/exito",
            "failure": f"{settings.FRONTEND_URL}/suscripcion/cancelado",
            "pending": f"{settings.FRONTEND_URL}/suscripcion/pendiente"
        },
        "auto_return": "approved",
        "external_reference": external_reference,
        "notification_url": f"{settings.BACKEND_URL}/api/suscripciones/webhook/mercadopago/",
        "expires": True,
        "expiration_date_from": timezone.now().isoformat(),
        "expiration_date_to": (timezone.now() + timezone.timedelta(hours=24)).isoformat(),
    }
    
    try:
        preference_response = sdk.preference().create(preference_data)
        
        if preference_response["status"] == 201:
            preference_id = preference_response["response"]["id"]
            
            # Crear o actualizar suscripción pendiente
            suscripcion, created = Suscripcion.objects.get_or_create(
                usuario=request.user,
                plan=plan,
                estado='pending',
                defaults={
                    'mp_preference_id': preference_id,
                    'mp_external_reference': external_reference,
                    'monto': plan.precio_mensual,
                }
            )
            
            if not created:
                # Actualizar suscripción existente
                suscripcion.mp_preference_id = preference_id
                suscripcion.mp_external_reference = external_reference
                suscripcion.monto = plan.precio_mensual
                suscripcion.save()
            
            # Determinar URL según ambiente
            init_point = preference_response["response"]["sandbox_init_point"] if settings.MERCADOPAGO_SANDBOX else preference_response["response"]["init_point"]
            
            return Response({
                'preference_id': preference_id,
                'init_point': init_point,
                'external_reference': external_reference,
                'monto': float(plan.precio_mensual),
                'plan': plan.name
            })
        else:
            logger.error(f"Error creando preferencia MP: {preference_response}")
            return Response({'error': 'Error creando preferencia de pago'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Excepción creando preferencia MP: {str(e)}")
        return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def webhook_mercadopago(request):
    """Webhook para recibir notificaciones de MercadoPago"""
    
    # Log del webhook recibido
    webhook_log = LogWebhook.objects.create(
        tipo=request.data.get('type', 'unknown'),
        data_id=request.data.get('data', {}).get('id'),
        payload=request.data
    )
    
    try:
        # Solo procesar notificaciones de pago
        if request.data.get('type') == 'payment':
            payment_id = request.data.get('data', {}).get('id')
            
            if not payment_id:
                webhook_log.error = "No se encontró payment_id en el webhook"
                webhook_log.save()
                return Response({'status': 'error', 'message': 'payment_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener información del pago desde MP
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(payment_id)
            
            if payment_info["status"] != 200:
                webhook_log.error = f"Error obteniendo pago de MP: {payment_info}"
                webhook_log.save()
                return Response({'status': 'error', 'message': 'Error obteniendo información del pago'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            payment_data = payment_info["response"]
            external_reference = payment_data.get('external_reference', '')
            
            if not external_reference:
                webhook_log.error = "No se encontró external_reference en el pago"
                webhook_log.save()
                return Response({'status': 'error', 'message': 'external_reference requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Parsear external_reference: "user_id_plan_code_timestamp"
            try:
                parts = external_reference.split('_')
                if len(parts) < 3:
                    raise ValueError("Formato de external_reference inválido")
                
                user_id = int(parts[0])
                plan_code = parts[1]
                
                user = User.objects.get(id=user_id)
                plan = Plan.objects.get(code=plan_code)
                
                # Buscar suscripción existente o crear nueva
                suscripcion, created = Suscripcion.objects.get_or_create(
                    mp_external_reference=external_reference,
                    defaults={
                        'usuario': user,
                        'plan': plan,
                        'monto': Decimal(str(payment_data.get('transaction_amount', 0)))
                    }
                )
                
                # Evitar procesar el mismo pago múltiples veces
                if suscripcion.procesada and suscripcion.mp_payment_id == str(payment_id):
                    webhook_log.procesado = True
                    webhook_log.suscripcion = suscripcion
                    webhook_log.save()
                    return Response({'status': 'ok', 'message': 'Pago ya procesado'})
                
                # Actualizar datos de la suscripción
                suscripcion.mp_payment_id = str(payment_id)
                suscripcion.estado = payment_data['status']
                suscripcion.mp_metadata = payment_data
                suscripcion.procesada = True
                
                if payment_data['status'] == 'approved':
                    suscripcion.fecha_pago = timezone.now()
                    suscripcion.activar_suscripcion()
                    
                    logger.info(f"Suscripción activada para usuario {user.username} - Plan {plan.name}")
                
                suscripcion.save()
                
                webhook_log.procesado = True
                webhook_log.suscripcion = suscripcion
                webhook_log.save()
                
                return Response({'status': 'ok', 'message': 'Webhook procesado correctamente'})
                
            except (ValueError, IndexError, User.DoesNotExist, Plan.DoesNotExist) as e:
                error_msg = f"Error procesando external_reference '{external_reference}': {str(e)}"
                webhook_log.error = error_msg
                webhook_log.save()
                logger.error(error_msg)
                return Response({'status': 'error', 'message': 'Error procesando referencia'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Tipo de webhook no soportado
            webhook_log.procesado = True
            webhook_log.save()
            return Response({'status': 'ok', 'message': 'Tipo de webhook no procesado'})
    
    except Exception as e:
        error_msg = f"Error procesando webhook: {str(e)}"
        webhook_log.error = error_msg
        webhook_log.save()
        logger.error(error_msg)
        return Response({'status': 'error', 'message': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_pago(request, payment_id):
    """Verificar estado de un pago específico"""
    try:
        suscripcion = Suscripcion.objects.get(
            usuario=request.user,
            mp_payment_id=payment_id
        )
        
        return Response({
            'estado': suscripcion.estado,
            'activa': suscripcion.activa,
            'plan': suscripcion.plan.name,
            'fecha_pago': suscripcion.fecha_pago,
            'fecha_fin': suscripcion.fecha_fin,
            'esta_vigente': suscripcion.esta_vigente,
            'dias_restantes': suscripcion.dias_restantes
        })
        
    except Suscripcion.DoesNotExist:
        return Response({'error': 'Pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_suscripciones(request):
    """Listar suscripciones del usuario autenticado"""
    suscripciones = Suscripcion.objects.filter(usuario=request.user)
    
    data = []
    for suscripcion in suscripciones:
        data.append({
            'id': suscripcion.id,
            'plan': suscripcion.plan.name,
            'estado': suscripcion.get_estado_display(),
            'monto': float(suscripcion.monto),
            'activa': suscripcion.activa,
            'fecha_creacion': suscripcion.fecha_creacion,
            'fecha_pago': suscripcion.fecha_pago,
            'fecha_inicio': suscripcion.fecha_inicio,
            'fecha_fin': suscripcion.fecha_fin,
            'esta_vigente': suscripcion.esta_vigente,
            'dias_restantes': suscripcion.dias_restantes
        })
    
    return Response(data)

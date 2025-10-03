"""
Vistas para manejar suscripciones automáticas de MercadoPago
Usa Preapprovals para renovación automática
"""

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
from datetime import datetime, timedelta

from apps.usuarios.models import Plan
from .models import Suscripcion, LogWebhook

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_suscripcion_automatica(request):
    """
    Crear suscripción automática (preapproval) en MercadoPago
    Esto permite renovación automática mensual
    """
    plan_code = request.data.get('plan')
    
    if not plan_code:
        return Response({'error': 'Plan requerido'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        plan = Plan.objects.get(code=plan_code, is_active=True)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # Si el plan es gratuito, activarlo directamente
    if plan.precio_mensual <= 0:
        # Usar la lógica existente para planes gratuitos
        from .views import crear_preferencia_pago
        return crear_preferencia_pago(request)
    
    # Configurar MercadoPago
    if not settings.MERCADOPAGO_ACCESS_TOKEN:
        return Response({'error': 'MercadoPago no configurado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    # Crear external_reference único para la suscripción
    external_reference = f"sub_{request.user.id}_{plan.code}_{int(timezone.now().timestamp())}"
    
    # URLs de retorno
    if settings.DEBUG:
        base_url = "https://localhost:5173"
    else:
        base_url = settings.FRONTEND_URL
    
    success_url = f"{base_url}/suscripcion/exito?external_reference={external_reference}"
    failure_url = f"{base_url}/suscripcion/cancelado?external_reference={external_reference}"
    
    # Calcular fechas de la suscripción
    start_date = timezone.now()
    end_date = start_date + timedelta(days=365)  # 1 año de suscripción
    
    # Crear preapproval (suscripción automática)
    preapproval_data = {
        "reason": f"Suscripción {plan.name} - DeConfianza",
        "external_reference": external_reference,
        "payer_email": request.user.email,
        "back_url": success_url,
        "auto_recurring": {
            "frequency": 1,
            "frequency_type": "months",
            "transaction_amount": float(plan.precio_mensual),
            "currency_id": "ARS",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "status": "pending"
    }
    
    try:
        # Crear preapproval en MercadoPago
        preapproval_response = sdk.preapproval().create(preapproval_data)
        
        if preapproval_response["status"] == 200 or preapproval_response["status"] == 201:
            preapproval_data = preapproval_response["response"]
            
            # Crear registro de suscripción pendiente
            suscripcion = Suscripcion.objects.create(
                usuario=request.user,
                plan=plan,
                estado='pending',
                monto=plan.precio_mensual,
                mp_external_reference=external_reference,
                mp_preference_id=preapproval_data.get('id'),  # Guardamos el preapproval_id
                mp_metadata={
                    'preapproval_id': preapproval_data.get('id'),
                    'init_point': preapproval_data.get('init_point'),
                    'auto_recurring': True
                }
            )
            
            logger.info(f"Preapproval creado para usuario {request.user.username} - Plan {plan.name}")
            
            return Response({
                'preapproval_id': preapproval_data.get('id'),
                'init_point': preapproval_data.get('init_point'),
                'sandbox_init_point': preapproval_data.get('sandbox_init_point'),
                'external_reference': external_reference,
                'auto_recurring': True,
                'plan': plan.name,
                'amount': float(plan.precio_mensual),
                'frequency': 'monthly'
            })
        else:
            logger.error(f"Error creando preapproval: {preapproval_response}")
            return Response({
                'error': 'Error creando suscripción automática',
                'details': preapproval_response.get('message', 'Error desconocido')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error en MercadoPago preapproval: {str(e)}")
        return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def webhook_suscripciones_mp(request):
    """
    Webhook específico para suscripciones automáticas
    Maneja eventos de preapprovals y authorized_payments
    """
    logger.info(f"Webhook suscripciones recibido: {request.data}")
    
    # Crear log del webhook
    webhook_log = LogWebhook.objects.create(
        tipo=request.data.get('type', 'unknown'),
        data_id=request.data.get('data', {}).get('id'),
        payload=request.data
    )
    
    try:
        action = request.data.get('action')
        tipo = request.data.get('type')
        data_id = request.data.get('data', {}).get('id')
        
        if not data_id:
            webhook_log.error = "data_id faltante"
            webhook_log.save()
            return Response({'status': 'error', 'message': 'data_id requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Configurar SDK
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        if tipo == 'preapproval':
            # Evento de suscripción (activación, cancelación, etc.)
            preapproval_response = sdk.preapproval().get(data_id)
            
            if preapproval_response["status"] != 200:
                webhook_log.error = f"Error obteniendo preapproval: {preapproval_response}"
                webhook_log.save()
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            
            preapproval_data = preapproval_response["response"]
            external_reference = preapproval_data.get('external_reference')
            
            if not external_reference:
                webhook_log.error = "external_reference faltante en preapproval"
                webhook_log.save()
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Buscar suscripción por external_reference
            try:
                suscripcion = Suscripcion.objects.get(mp_external_reference=external_reference)
                
                # Actualizar estado de la suscripción
                old_status = suscripcion.estado
                suscripcion.estado = preapproval_data.get('status', 'pending')
                suscripcion.mp_metadata.update({
                    'preapproval_data': preapproval_data,
                    'last_webhook': timezone.now().isoformat()
                })
                
                if preapproval_data.get('status') == 'authorized':
                    # Suscripción autorizada - activar
                    suscripcion.activa = True
                    suscripcion.fecha_inicio = timezone.now()
                    suscripcion.fecha_fin = timezone.now() + timedelta(days=30)
                    logger.info(f"Suscripción autorizada: {external_reference}")
                
                suscripcion.save()
                webhook_log.suscripcion = suscripcion
                webhook_log.procesado = True
                webhook_log.save()
                
                logger.info(f"Preapproval procesado: {external_reference} - {old_status} -> {suscripcion.estado}")
                
            except Suscripcion.DoesNotExist:
                webhook_log.error = f"Suscripción no encontrada: {external_reference}"
                webhook_log.save()
                return Response({'status': 'error', 'message': 'Suscripción no encontrada'})
        
        elif tipo == 'authorized_payment':
            # Pago automático recurrente
            payment_response = sdk.payment().get(data_id)
            
            if payment_response["status"] != 200:
                webhook_log.error = f"Error obteniendo payment: {payment_response}"
                webhook_log.save()
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            
            payment_data = payment_response["response"]
            external_reference = payment_data.get('external_reference')
            
            # Extraer el external_reference de la suscripción
            if external_reference and external_reference.startswith('sub_'):
                # Buscar suscripción activa del usuario
                preapproval_id = payment_data.get('preapproval_id')
                if preapproval_id:
                    try:
                        suscripcion = Suscripcion.objects.get(
                            mp_metadata__preapproval_id=preapproval_id,
                            activa=True
                        )
                        
                        if payment_data.get('status') == 'approved':
                            # Pago aprobado - extender suscripción
                            suscripcion.fecha_fin = timezone.now() + timedelta(days=30)
                            suscripcion.fecha_pago = timezone.now()
                            
                            # Guardar información del pago en metadata
                            payments_history = suscripcion.mp_metadata.get('payments_history', [])
                            payments_history.append({
                                'payment_id': data_id,
                                'amount': payment_data.get('transaction_amount'),
                                'date': timezone.now().isoformat(),
                                'status': payment_data.get('status')
                            })
                            suscripcion.mp_metadata['payments_history'] = payments_history
                            suscripcion.save()
                            
                            webhook_log.suscripcion = suscripcion
                            webhook_log.procesado = True
                            webhook_log.save()
                            
                            logger.info(f"Pago automático procesado: {data_id} - Suscripción extendida hasta {suscripcion.fecha_fin}")
                        
                    except Suscripcion.DoesNotExist:
                        webhook_log.error = f"Suscripción no encontrada para preapproval_id: {preapproval_id}"
                        webhook_log.save()
        
        return Response({'status': 'ok'})
        
    except Exception as e:
        error_msg = f"Error procesando webhook: {str(e)}"
        logger.error(error_msg)
        webhook_log.error = error_msg
        webhook_log.save()
        return Response({'status': 'error', 'message': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancelar_suscripcion_automatica(request):
    """Cancelar suscripción automática en MercadoPago"""
    try:
        # Buscar suscripción activa del usuario
        suscripcion = request.user.suscripciones.filter(
            activa=True,
            mp_metadata__auto_recurring=True
        ).first()
        
        if not suscripcion:
            return Response({'error': 'No se encontró suscripción automática activa'}, status=status.HTTP_404_NOT_FOUND)
        
        preapproval_id = suscripcion.mp_metadata.get('preapproval_id')
        if not preapproval_id:
            return Response({'error': 'ID de suscripción no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Cancelar en MercadoPago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        cancel_response = sdk.preapproval().update(preapproval_id, {"status": "cancelled"})
        
        if cancel_response["status"] == 200:
            # Desactivar suscripción local
            suscripcion.activa = False
            suscripcion.estado = 'cancelled'
            suscripcion.mp_metadata.update({
                'cancelled_at': timezone.now().isoformat(),
                'cancelled_by': 'user'
            })
            suscripcion.save()
            
            logger.info(f"Suscripción cancelada: {preapproval_id} - Usuario: {request.user.username}")
            
            return Response({
                'message': 'Suscripción cancelada exitosamente',
                'cancelled_at': timezone.now().isoformat()
            })
        else:
            return Response({
                'error': 'Error cancelando suscripción en MercadoPago',
                'details': cancel_response
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error cancelando suscripción: {str(e)}")
        return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

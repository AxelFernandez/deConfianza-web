import logging
import mercadopago
from decimal import Decimal
from .utils import (
    calcular_prorrateo,
    determinar_tipo_cambio,
    obtener_suscripcion_activa,
    puede_cambiar_plan,
    calcular_fecha_proximo_cobro
)
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
    
    # Si el plan es gratuito, activarlo directamente sin pago
    if plan.precio_mensual <= 0:
        # Activar plan gratuito creando suscripción
        from apps.usuarios.models import Perfil
        from django.utils import timezone
        from datetime import timedelta
        
        try:
            perfil = request.user.perfil
            
            # Crear registro de suscripción gratuita
            suscripcion, created = Suscripcion.objects.get_or_create(
                usuario=request.user,
                plan=plan,
                defaults={
                    'estado': 'approved',
                    'monto': 0,
                    'fecha_inicio': timezone.now(),
                    'fecha_fin': timezone.now() + timedelta(days=30),
                    'fecha_pago': timezone.now(),
                    'activa': True,
                }
            )
            
            if not created and not suscripcion.activa:
                suscripcion.estado = 'approved'
                suscripcion.fecha_inicio = timezone.now()
                suscripcion.fecha_fin = timezone.now() + timedelta(days=30)
                suscripcion.fecha_pago = timezone.now()
                suscripcion.activa = True
                suscripcion.save()
            
            return Response({
                'message': 'Plan gratuito activado exitosamente',
                'plan': plan.name,
                'is_free': True,
                'suscripcion_id': suscripcion.id
            })
            
        except Exception as e:
            logger.error(f"Error activando plan gratuito: {str(e)}")
            return Response({'error': 'Error activando plan gratuito'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Configurar MercadoPago
    if not settings.MERCADOPAGO_ACCESS_TOKEN:
        return Response({'error': 'MercadoPago no configurado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    # Crear external_reference único
    external_reference = f"{request.user.id}_{plan.code}_{int(timezone.now().timestamp())}"
    
    # URLs para desarrollo vs producción
    if settings.DEBUG and 'localhost' in settings.FRONTEND_URL:
        # En desarrollo local, usamos URLs de ejemplo válidas para MercadoPago
        base_url = "https://localhost:5173"
        success_url = f"{base_url}/suscripcion/exito?external_reference={external_reference}"
        failure_url = f"{base_url}/suscripcion/cancelado?external_reference={external_reference}"
        pending_url = f"{base_url}/suscripcion/pendiente?external_reference={external_reference}"
    else:
        # En producción usamos las URLs reales
        success_url = f"{settings.FRONTEND_URL}/suscripcion/exito"
        failure_url = f"{settings.FRONTEND_URL}/suscripcion/cancelado"
        pending_url = f"{settings.FRONTEND_URL}/suscripcion/pendiente"

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
            "success": success_url,
            "failure": failure_url,
            "pending": pending_url
        },
        "external_reference": external_reference,
        "notification_url": f"{settings.BACKEND_URL}/api/suscripciones/webhook/mercadopago/",
        "expires": True,
        "expiration_date_from": timezone.now().isoformat(),
        "expiration_date_to": (timezone.now() + timezone.timedelta(hours=24)).isoformat(),
    }
    
    logger.info(f"Creando preferencia MP para usuario {request.user.id}, plan {plan.code}")
    logger.info(f"URLs configuradas - Success: {success_url}, Failure: {failure_url}, Pending: {pending_url}")
    
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def solicitar_cambio_plan(request):
    """
    Solicita un cambio de plan.
    - Si es upgrade: calcula prorrateo y crea preferencia de pago
    - Si es downgrade: programa el cambio para fin de ciclo
    """
    plan_code = request.data.get('plan_code')
    
    if not plan_code:
        return Response({'error': 'plan_code requerido'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        plan_nuevo = Plan.objects.get(code=plan_code, is_active=True)
    except Plan.DoesNotExist:
        return Response({'error': 'Plan no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # Verificar si puede cambiar de plan
    validacion = puede_cambiar_plan(request.user, plan_nuevo)
    if not validacion['puede']:
        return Response({'error': validacion['razon']}, status=status.HTTP_400_BAD_REQUEST)
    
    # Obtener suscripción activa
    suscripcion_actual = obtener_suscripcion_activa(request.user)
    
    if not suscripcion_actual:
        return Response({'error': 'No tienes una suscripción activa'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Determinar tipo de cambio
    tipo_cambio = determinar_tipo_cambio(suscripcion_actual.plan, plan_nuevo)
    
    if tipo_cambio == 'same':
        return Response({'error': 'Ya tienes este plan activo'}, status=status.HTTP_400_BAD_REQUEST)
    
    # UPGRADE: Calcular prorrateo y crear preferencia de pago
    if tipo_cambio == 'upgrade':
        calculo = calcular_prorrateo(suscripcion_actual, plan_nuevo)
        
        if calculo['error']:
            return Response({'error': calculo['detalle']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si el monto a pagar es 0 (ej: upgrade de plan gratis a gratis)
        if calculo['monto_a_pagar'] == 0:
            # Cambio inmediato sin pago
            suscripcion_actual.desactivar_suscripcion()
            
            nueva_suscripcion = Suscripcion.objects.create(
                usuario=request.user,
                plan=plan_nuevo,
                estado='approved',
                monto=plan_nuevo.precio_mensual,
                activa=True,
                fecha_inicio=timezone.now(),
                fecha_fin=suscripcion_actual.fecha_fin,  # Mantener misma fecha fin
                fecha_pago=timezone.now()
            )
            
            return Response({
                'tipo': 'upgrade',
                'cambio_inmediato': True,
                'mensaje': f'Tu plan ha sido actualizado a {plan_nuevo.name}',
                'suscripcion_id': nueva_suscripcion.id
            })
        
        # Crear preferencia de pago en MercadoPago
        if not settings.MERCADOPAGO_ACCESS_TOKEN:
            return Response({'error': 'MercadoPago no configurado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        external_reference = f"upgrade_{request.user.id}_{plan_code}_{int(timezone.now().timestamp())}"
        
        # URLs de retorno
        if settings.DEBUG:
            base_url = "https://localhost:5173"
        else:
            base_url = settings.FRONTEND_URL
        
        success_url = f"{base_url}/suscripcion/exito?external_reference={external_reference}&tipo=upgrade"
        failure_url = f"{base_url}/suscripcion/cancelado?tipo=upgrade"
        pending_url = f"{base_url}/suscripcion/pendiente?tipo=upgrade"
        
        preference_data = {
            "items": [{
                "title": f"Upgrade a {plan_nuevo.name}",
                "description": f"Cambio de {suscripcion_actual.plan.name} a {plan_nuevo.name} (prorrateado)",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": float(calculo['monto_a_pagar'])
            }],
            "payer": {
                "name": request.user.first_name or "Usuario",
                "surname": request.user.last_name or "DeConfianza",
                "email": request.user.email,
            },
            "back_urls": {
                "success": success_url,
                "failure": failure_url,
                "pending": pending_url
            },
            "external_reference": external_reference,
            "auto_return": "approved",
            "metadata": {
                "tipo": "upgrade",
                "suscripcion_anterior_id": suscripcion_actual.id,
                "plan_anterior": suscripcion_actual.plan.code,
                "plan_nuevo": plan_code,
                "dias_restantes": calculo['dias_restantes']
            }
        }
        
        try:
            preference_response = sdk.preference().create(preference_data)
            
            if preference_response["status"] in [200, 201]:
                preference = preference_response["response"]
                
                # Crear registro temporal de suscripción pendiente
                Suscripcion.objects.create(
                    usuario=request.user,
                    plan=plan_nuevo,
                    estado='pending',
                    monto=calculo['monto_a_pagar'],
                    mp_external_reference=external_reference,
                    mp_preference_id=preference.get('id'),
                    mp_metadata={
                        'tipo': 'upgrade',
                        'suscripcion_anterior_id': suscripcion_actual.id,
                        'calculo_prorrateo': {
                            'monto_a_pagar': float(calculo['monto_a_pagar']),
                            'dias_restantes': calculo['dias_restantes'],
                            'credito_plan_actual': float(calculo['credito_plan_actual']),
                            'costo_plan_nuevo': float(calculo['costo_plan_nuevo'])
                        }
                    }
                )
                
                return Response({
                    'tipo': 'upgrade',
                    'preference_id': preference.get('id'),
                    'init_point': preference.get('init_point'),
                    'sandbox_init_point': preference.get('sandbox_init_point'),
                    'calculo': {
                        'monto_a_pagar': float(calculo['monto_a_pagar']),
                        'dias_restantes': calculo['dias_restantes'],
                        'detalle': calculo['detalle']
                    }
                })
            else:
                return Response({
                    'error': 'Error creando preferencia de pago',
                    'details': preference_response
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error en MercadoPago: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # DOWNGRADE: Programar cambio para fin de ciclo
    else:  # tipo_cambio == 'downgrade'
        from .models import CambioPlanProgramado
        
        cambio_programado = CambioPlanProgramado.objects.create(
            usuario=request.user,
            plan_actual=suscripcion_actual.plan,
            plan_nuevo=plan_nuevo,
            suscripcion_actual=suscripcion_actual,
            fecha_programada=suscripcion_actual.fecha_fin,
            es_upgrade=False
        )
        
        return Response({
            'tipo': 'downgrade',
            'cambio_programado': True,
            'cambio_id': cambio_programado.id,
            'fecha_programada': cambio_programado.fecha_programada,
            'mensaje': f'Tu plan cambiará a {plan_nuevo.name} el {cambio_programado.fecha_programada.strftime("%d/%m/%Y")}',
            'detalle': f'Seguirás disfrutando de {suscripcion_actual.plan.name} hasta entonces.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancelar_cambio_programado(request):
    """Cancela un cambio de plan programado"""
    from .models import CambioPlanProgramado
    
    try:
        cambio = CambioPlanProgramado.objects.get(
            usuario=request.user,
            estado='pending'
        )
        
        if cambio.cancelar_cambio():
            return Response({
                'mensaje': 'Cambio de plan cancelado exitosamente',
                'cambio_id': cambio.id
            })
        else:
            return Response({
                'error': 'No se pudo cancelar el cambio'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except CambioPlanProgramado.DoesNotExist:
        return Response({
            'error': 'No tienes un cambio de plan pendiente'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def info_suscripcion_actual(request):
    """Obtiene información detallada de la suscripción actual del usuario"""
    from .models import CambioPlanProgramado
    
    suscripcion = obtener_suscripcion_activa(request.user)
    
    if not suscripcion:
        return Response({
            'tiene_suscripcion': False,
            'mensaje': 'No tienes una suscripción activa'
        })
    
    # Verificar si tiene cambio programado
    cambio_programado = CambioPlanProgramado.objects.filter(
        usuario=request.user,
        estado='pending'
    ).first()
    
    data = {
        'tiene_suscripcion': True,
        'suscripcion': {
            'id': suscripcion.id,
            'plan': {
                'id': suscripcion.plan.id,
                'code': suscripcion.plan.code,
                'name': suscripcion.plan.name,
                'precio_mensual': float(suscripcion.plan.precio_mensual)
            },
            'monto': float(suscripcion.monto),
            'activa': suscripcion.activa,
            'fecha_inicio': suscripcion.fecha_inicio,
            'fecha_fin': suscripcion.fecha_fin,
            'proximo_cobro': calcular_fecha_proximo_cobro(suscripcion),
            'esta_vigente': suscripcion.esta_vigente,
            'dias_restantes': suscripcion.dias_restantes
        },
        'cambio_programado': None
    }
    
    if cambio_programado:
        data['cambio_programado'] = {
            'id': cambio_programado.id,
            'plan_nuevo': {
                'id': cambio_programado.plan_nuevo.id,
                'code': cambio_programado.plan_nuevo.code,
                'name': cambio_programado.plan_nuevo.name,
                'precio_mensual': float(cambio_programado.plan_nuevo.precio_mensual)
            },
            'fecha_programada': cambio_programado.fecha_programada,
            'es_upgrade': cambio_programado.es_upgrade,
            'dias_hasta_cambio': (cambio_programado.fecha_programada - timezone.now()).days
        }
    
    return Response(data)

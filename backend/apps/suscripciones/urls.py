from django.urls import path
from . import views
from . import views_subscriptions
from . import views_comparison

urlpatterns = [
    # Pagos únicos (sistema actual)
    path('crear-preferencia/', views.crear_preferencia_pago, name='crear_preferencia_pago'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
    path('verificar-pago/<str:payment_id>/', views.verificar_pago, name='verificar_pago'),
    path('mis-suscripciones/', views.mis_suscripciones, name='mis_suscripciones'),
    
    # Cambio de planes
    path('solicitar-cambio-plan/', views.solicitar_cambio_plan, name='solicitar_cambio_plan'),
    path('cancelar-cambio-programado/', views.cancelar_cambio_programado, name='cancelar_cambio_programado'),
    path('info-suscripcion/', views.info_suscripcion_actual, name='info_suscripcion_actual'),
    
    # Suscripciones automáticas (nuevo)
    path('crear-suscripcion/', views_subscriptions.crear_suscripcion_automatica, name='crear_suscripcion_automatica'),
    path('webhook/suscripciones/', views_subscriptions.webhook_suscripciones_mp, name='webhook_suscripciones_mp'),
    path('cancelar-suscripcion/', views_subscriptions.cancelar_suscripcion_automatica, name='cancelar_suscripcion_automatica'),
    
    # Comparación y demo
    path('comparar-sistemas/', views_comparison.comparar_sistemas_pago, name='comparar_sistemas_pago'),
    path('demo-flujo/', views_comparison.demo_flujo_suscripciones, name='demo_flujo_suscripciones'),
]

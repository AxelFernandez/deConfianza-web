from django.urls import path
from . import views

urlpatterns = [
    path('crear-preferencia/', views.crear_preferencia_pago, name='crear_preferencia_pago'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
    path('verificar-pago/<str:payment_id>/', views.verificar_pago, name='verificar_pago'),
    path('mis-suscripciones/', views.mis_suscripciones, name='mis_suscripciones'),
]

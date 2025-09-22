from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, 
    RubroViewSet, 
    ServicioViewSet, 
    PrestadorViewSet, 
    MediaPrestadorViewSet, 
    ResenaViewSet,
    dashboard_prestador,
    registrar_visualizacion
)

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('rubros', RubroViewSet)
router.register('servicios', ServicioViewSet)
router.register('prestadores', PrestadorViewSet)
router.register('media', MediaPrestadorViewSet)
router.register('resenas', ResenaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_prestador, name='dashboard_prestador'),
    path('mis-servicios/', ServicioViewSet.as_view({'get': 'mis_servicios', 'post': 'create'}), name='mis-servicios-list'),
    path('mis-servicios/<int:pk>/', ServicioViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='mis-servicios-detail'),
    path('mis-resenas/', ServicioViewSet.as_view({'get': 'mis_resenas'}), name='mis-resenas-list'),
    path('registrar-visualizacion/', registrar_visualizacion, name='registrar-visualizacion'),
]

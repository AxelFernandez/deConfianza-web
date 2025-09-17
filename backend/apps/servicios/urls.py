from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, 
    RubroViewSet, 
    ServicioViewSet, 
    RangoSuscripcionViewSet, 
    PrestadorViewSet, 
    MediaPrestadorViewSet, 
    ResenaViewSet
)

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('rubros', RubroViewSet)
router.register('servicios', ServicioViewSet)
router.register('rangos', RangoSuscripcionViewSet)
router.register('prestadores', PrestadorViewSet)
router.register('media', MediaPrestadorViewSet)
router.register('resenas', ResenaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

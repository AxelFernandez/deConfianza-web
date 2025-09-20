from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet, google_login_view, planes_view

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    # Rutas explícitas primero para evitar colisiones con el router (lookup)
    path('planes/', planes_view, name='planes'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/google/', google_login_view, name='google_login'),
    # Rutas del router al final
    path('', include(router.urls)),
]

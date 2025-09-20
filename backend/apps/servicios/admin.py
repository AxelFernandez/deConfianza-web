from django.contrib import admin
from .models import (
    Categoria,
    Rubro,
    Servicio,
    RangoSuscripcion,
    Prestador,
    MediaPrestador,
    Resena,
    ServicioPrestador,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Rubro)
class RubroAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria")
    list_filter = ("categoria",)
    search_fields = ("nombre",)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "rubro")
    list_filter = ("rubro",)
    search_fields = ("nombre",)


@admin.register(RangoSuscripcion)
class RangoSuscripcionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "rango", "precio_usd")
    list_filter = ("rango",)
    search_fields = ("nombre",)


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_comercial", "usuario", "ciudad", "provincia", "pais")
    list_filter = ("ciudad", "provincia", "pais", "rango_suscripcion")
    search_fields = ("nombre_comercial", "usuario__username", "usuario__email")


@admin.register(MediaPrestador)
class MediaPrestadorAdmin(admin.ModelAdmin):
    list_display = ("id", "prestador", "tipo", "titulo", "fecha_subida")
    list_filter = ("tipo", "fecha_subida")
    search_fields = ("titulo", "prestador__nombre_comercial")


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ("id", "prestador", "calificacion", "nombre", "fecha")
    list_filter = ("calificacion", "fecha")
    search_fields = ("prestador__nombre_comercial", "nombre", "comentario")


@admin.register(ServicioPrestador)
class ServicioPrestadorAdmin(admin.ModelAdmin):
    list_display = ("id", "prestador", "nombre", "precio_base", "activo", "fecha_creacion")
    list_filter = ("activo", "fecha_creacion", "servicio_base")
    search_fields = ("prestador__username", "nombre", "descripcion")



from django.contrib import admin
from .models import (
    Categoria,
    Rubro,
    Servicio,
    Prestador,
    MediaPrestador,
    Resena,
    VisualizacionPerfil,
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
    list_display = ("id", "nombre", "prestador", "categoria", "rubro", "precio_base", "activo", "fecha_creacion")
    list_filter = ("activo", "categoria", "rubro", "fecha_creacion")
    search_fields = ("nombre", "prestador__username", "descripcion")


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_comercial", "usuario", "ciudad", "provincia", "pais")
    list_filter = ("ciudad", "provincia", "pais")
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




@admin.register(VisualizacionPerfil)
class VisualizacionPerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "prestador", "ip_address", "fecha")
    list_filter = ("fecha", "prestador")
    search_fields = ("prestador__nombre_comercial", "ip_address")
    readonly_fields = ("fecha",)



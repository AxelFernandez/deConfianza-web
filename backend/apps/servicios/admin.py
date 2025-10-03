from django.contrib import admin
from .models import (
    Categoria,
    Rubro,
    Servicio,
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
    list_display = ("id", "nombre", "prestador", "get_categoria", "get_rubro", "precio_base", "activo", "fecha_creacion")
    list_filter = ("activo", "prestador__perfil__categoria", "prestador__perfil__rubro", "fecha_creacion")
    search_fields = ("nombre", "prestador__username", "descripcion")
    
    def get_categoria(self, obj):
        """Obtener categoría del perfil del prestador"""
        return obj.prestador.perfil.categoria.nombre if hasattr(obj.prestador, 'perfil') and obj.prestador.perfil.categoria else 'Sin categoría'
    get_categoria.short_description = 'Categoría'
    
    def get_rubro(self, obj):
        """Obtener rubro del perfil del prestador"""
        return obj.prestador.perfil.rubro.nombre if hasattr(obj.prestador, 'perfil') and obj.prestador.perfil.rubro else 'Sin rubro'
    get_rubro.short_description = 'Rubro'




@admin.register(MediaPrestador)
class MediaPrestadorAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "tipo", "titulo", "fecha_subida")
    list_filter = ("tipo", "fecha_subida")
    search_fields = ("titulo", "usuario__username", "usuario__email")


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "calificacion", "nombre", "fecha")
    list_filter = ("calificacion", "fecha")
    search_fields = ("usuario__username", "usuario__email", "nombre", "comentario")




@admin.register(VisualizacionPerfil)
class VisualizacionPerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "ip_address", "fecha")
    list_filter = ("fecha", "usuario")
    search_fields = ("usuario__username", "usuario__email", "ip_address")
    readonly_fields = ("fecha",)



from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, Rubro, Servicio, RangoSuscripcion, Prestador, MediaPrestador, Resena, ServicioPrestador
from .serializers import (
    CategoriaSerializer, 
    RubroSerializer, 
    ServicioSerializer,
    RangoSuscripcionSerializer,
    PrestadorListSerializer,
    PrestadorDetailSerializer,
    MediaPrestadorSerializer,
    ResenaSerializer,
    ServicioPrestadorSerializer
)

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    @action(detail=True, methods=['get'])
    def rubros(self, request, pk=None):
        """Obtener todos los rubros de una categoría"""
        categoria = self.get_object()
        rubros = categoria.rubros.all()
        serializer = RubroSerializer(rubros, many=True)
        return Response(serializer.data)

class RubroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rubro.objects.all()
    serializer_class = RubroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria']
    
    @action(detail=True, methods=['get'])
    def servicios(self, request, pk=None):
        """Obtener todos los servicios de un rubro"""
        rubro = self.get_object()
        servicios = rubro.servicios.all()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)

class ServicioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['rubro', 'rubro__categoria']
    search_fields = ['nombre', 'descripcion']
    
    @action(detail=True, methods=['get'])
    def prestadores(self, request, pk=None):
        """Obtener todos los prestadores de un servicio"""
        servicio = self.get_object()
        prestadores = servicio.prestadores.all()
        serializer = PrestadorListSerializer(prestadores, many=True)
        return Response(serializer.data)

class RangoSuscripcionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RangoSuscripcion.objects.all()
    serializer_class = RangoSuscripcionSerializer

class PrestadorViewSet(viewsets.ModelViewSet):
    queryset = Prestador.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ciudad', 'provincia', 'servicios', 'servicios__rubro', 'servicios__rubro__categoria']
    search_fields = ['nombre_comercial', 'descripcion', 'servicios__nombre']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PrestadorListSerializer
        return PrestadorDetailSerializer
    
    def get_queryset(self):
        queryset = Prestador.objects.all()
        
        # Filtrado por ubicación
        ciudad = self.request.query_params.get('ciudad', None)
        if ciudad:
            queryset = queryset.filter(ciudad__icontains=ciudad)
            
        provincia = self.request.query_params.get('provincia', None)
        if provincia:
            queryset = queryset.filter(provincia__icontains=provincia)
            
        # Filtrado por servicio, rubro o categoría
        servicio_id = self.request.query_params.get('servicio', None)
        if servicio_id:
            queryset = queryset.filter(servicios__id=servicio_id)
            
        rubro_id = self.request.query_params.get('rubro', None)
        if rubro_id:
            queryset = queryset.filter(servicios__rubro__id=rubro_id)
            
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id:
            queryset = queryset.filter(servicios__rubro__categoria__id=categoria_id)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def resenas(self, request, pk=None):
        prestador = self.get_object()
        resenas = prestador.resenas.all()
        serializer = ResenaSerializer(resenas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def media(self, request, pk=None):
        prestador = self.get_object()
        media = prestador.media.all()
        serializer = MediaPrestadorSerializer(media, many=True)
        return Response(serializer.data)

class MediaPrestadorViewSet(viewsets.ModelViewSet):
    queryset = MediaPrestador.objects.all()
    serializer_class = MediaPrestadorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prestador', 'tipo']

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prestador', 'calificacion']


class ServicioPrestadorViewSet(viewsets.ModelViewSet):
    serializer_class = ServicioPrestadorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['activo', 'servicio_base']
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ServicioPrestador.objects.filter(prestador=self.request.user)
        return ServicioPrestador.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(prestador=self.request.user)

"""
Comando para crear categorías y rubros de prueba.
Uso: python manage.py crear_rubros_test
"""
from django.core.management.base import BaseCommand
from apps.servicios.models import Categoria, Rubro


class Command(BaseCommand):
    help = 'Crea categorías y rubros para el entorno de test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando categorías y rubros de test...'))
        self.stdout.write('')
        
        # Definir estructura de categorías con sus rubros
        categorias_rubros = {
            'Oficios': {
                'descripcion': 'Servicios de oficios y trabajos manuales',
                'rubros': [
                    {'nombre': 'Albañilería', 'descripcion': 'Construcción, refacciones, mampostería'},
                    {'nombre': 'Plomería', 'descripcion': 'Instalación y reparación de cañerías y sanitarios'},
                    {'nombre': 'Electricidad', 'descripcion': 'Instalaciones eléctricas y reparaciones'},
                    {'nombre': 'Carpintería', 'descripcion': 'Trabajos en madera, muebles a medida'},
                    {'nombre': 'Pintura', 'descripcion': 'Pintura de interiores y exteriores'},
                    {'nombre': 'Herrería', 'descripcion': 'Trabajos en metal, rejas, portones'},
                    {'nombre': 'Jardinería', 'descripcion': 'Mantenimiento de jardines y parques'},
                    {'nombre': 'Gasista', 'descripcion': 'Instalación y reparación de gas'},
                    {'nombre': 'Techista', 'descripcion': 'Instalación y reparación de techos'},
                    {'nombre': 'Vidriero', 'descripcion': 'Instalación y reparación de vidrios'},
                ]
            },
            'Profesiones': {
                'descripcion': 'Servicios profesionales especializados',
                'rubros': [
                    {'nombre': 'Abogacía', 'descripcion': 'Servicios legales y jurídicos'},
                    {'nombre': 'Contabilidad', 'descripcion': 'Servicios contables y auditoría'},
                    {'nombre': 'Arquitectura', 'descripcion': 'Diseño y planificación de obras'},
                    {'nombre': 'Ingeniería', 'descripcion': 'Servicios de ingeniería civil, industrial, etc.'},
                    {'nombre': 'Medicina', 'descripcion': 'Servicios médicos y de salud'},
                    {'nombre': 'Odontología', 'descripcion': 'Servicios odontológicos'},
                    {'nombre': 'Psicología', 'descripcion': 'Atención psicológica y terapias'},
                    {'nombre': 'Veterinaria', 'descripcion': 'Atención veterinaria y cuidado animal'},
                    {'nombre': 'Nutrición', 'descripcion': 'Asesoramiento nutricional'},
                    {'nombre': 'Kinesiología', 'descripcion': 'Rehabilitación física y terapias'},
                ]
            },
            'Servicios del Hogar': {
                'descripcion': 'Servicios de limpieza y mantenimiento del hogar',
                'rubros': [
                    {'nombre': 'Limpieza', 'descripcion': 'Limpieza de casas y departamentos'},
                    {'nombre': 'Lavandería', 'descripcion': 'Lavado y planchado de ropa'},
                    {'nombre': 'Mudanzas', 'descripcion': 'Servicios de mudanza y transporte'},
                    {'nombre': 'Fumigación', 'descripcion': 'Control de plagas'},
                    {'nombre': 'Cerrajería', 'descripcion': 'Instalación y reparación de cerraduras'},
                    {'nombre': 'Tapicería', 'descripcion': 'Tapizado de muebles'},
                    {'nombre': 'Cortinados', 'descripcion': 'Confección e instalación de cortinas'},
                ]
            },
            'Tecnología': {
                'descripcion': 'Servicios de tecnología e informática',
                'rubros': [
                    {'nombre': 'Desarrollo Web', 'descripcion': 'Creación de sitios web y aplicaciones'},
                    {'nombre': 'Diseño Gráfico', 'descripcion': 'Diseño de logos, flyers, branding'},
                    {'nombre': 'Reparación de PC', 'descripcion': 'Reparación de computadoras'},
                    {'nombre': 'Redes y Sistemas', 'descripcion': 'Instalación y mantenimiento de redes'},
                    {'nombre': 'Fotografía', 'descripcion': 'Servicios fotográficos profesionales'},
                    {'nombre': 'Video y Edición', 'descripcion': 'Producción y edición de video'},
                    {'nombre': 'Marketing Digital', 'descripcion': 'Gestión de redes sociales y publicidad'},
                ]
            },
            'Gastronomía': {
                'descripcion': 'Servicios de alimentación y gastronomía',
                'rubros': [
                    {'nombre': 'Catering', 'descripcion': 'Servicio de comidas para eventos'},
                    {'nombre': 'Repostería', 'descripcion': 'Elaboración de tortas y postres'},
                    {'nombre': 'Cocina a domicilio', 'descripcion': 'Chef a domicilio'},
                    {'nombre': 'Bartender', 'descripcion': 'Servicio de barra y tragos'},
                    {'nombre': 'Parrillero', 'descripcion': 'Servicio de parrilla para eventos'},
                ]
            },
            'Belleza y Estética': {
                'descripcion': 'Servicios de belleza, estética y cuidado personal',
                'rubros': [
                    {'nombre': 'Peluquería', 'descripcion': 'Corte y peinado'},
                    {'nombre': 'Manicura', 'descripcion': 'Cuidado de uñas'},
                    {'nombre': 'Maquillaje', 'descripcion': 'Maquillaje social y artístico'},
                    {'nombre': 'Barbería', 'descripcion': 'Corte y arreglo de barba'},
                    {'nombre': 'Depilación', 'descripcion': 'Servicios de depilación'},
                    {'nombre': 'Spa y Masajes', 'descripcion': 'Tratamientos de relajación'},
                ]
            },
            'Educación': {
                'descripcion': 'Servicios educativos y de capacitación',
                'rubros': [
                    {'nombre': 'Clases Particulares', 'descripcion': 'Apoyo escolar y universitario'},
                    {'nombre': 'Idiomas', 'descripcion': 'Enseñanza de idiomas'},
                    {'nombre': 'Música', 'descripcion': 'Clases de instrumentos musicales'},
                    {'nombre': 'Arte', 'descripcion': 'Clases de dibujo, pintura, escultura'},
                    {'nombre': 'Deportes', 'descripcion': 'Entrenamiento personal y deportivo'},
                    {'nombre': 'Yoga y Pilates', 'descripcion': 'Clases de yoga y pilates'},
                ]
            },
            'Eventos': {
                'descripcion': 'Organización y servicios para eventos',
                'rubros': [
                    {'nombre': 'Organización de Eventos', 'descripcion': 'Planificación integral de eventos'},
                    {'nombre': 'DJ', 'descripcion': 'Música para eventos'},
                    {'nombre': 'Animación', 'descripcion': 'Animación infantil y para adultos'},
                    {'nombre': 'Decoración', 'descripcion': 'Decoración de eventos'},
                    {'nombre': 'Sonido e Iluminación', 'descripcion': 'Equipos de sonido y luces'},
                ]
            },
            'Transporte': {
                'descripcion': 'Servicios de transporte y logística',
                'rubros': [
                    {'nombre': 'Remis y Taxi', 'descripcion': 'Servicio de transporte de pasajeros'},
                    {'nombre': 'Fletes', 'descripcion': 'Transporte de mercaderías'},
                    {'nombre': 'Mensajería', 'descripcion': 'Envío de paquetes y documentos'},
                    {'nombre': 'Mecánica', 'descripcion': 'Reparación de vehículos'},
                    {'nombre': 'Gomería', 'descripcion': 'Reparación de neumáticos'},
                    {'nombre': 'Lavado de Autos', 'descripcion': 'Limpieza y pulido de vehículos'},
                ]
            },
            'Mascotas': {
                'descripcion': 'Servicios relacionados con mascotas',
                'rubros': [
                    {'nombre': 'Veterinaria', 'descripcion': 'Atención veterinaria'},
                    {'nombre': 'Peluquería Canina', 'descripcion': 'Estética para mascotas'},
                    {'nombre': 'Paseador de Perros', 'descripcion': 'Paseo de mascotas'},
                    {'nombre': 'Adiestramiento', 'descripcion': 'Entrenamiento de mascotas'},
                    {'nombre': 'Guardería', 'descripcion': 'Cuidado temporal de mascotas'},
                ]
            },
        }
        
        categorias_creadas = 0
        categorias_actualizadas = 0
        rubros_creados = 0
        rubros_actualizados = 0
        
        for categoria_nombre, categoria_data in categorias_rubros.items():
            # Crear o actualizar categoría
            categoria, created = Categoria.objects.get_or_create(
                nombre=categoria_nombre,
                defaults={'descripcion': categoria_data['descripcion']}
            )
            
            if created:
                categorias_creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Categoría "{categoria_nombre}" creada')
                )
            else:
                categorias_actualizadas += 1
                categoria.descripcion = categoria_data['descripcion']
                categoria.save()
                self.stdout.write(
                    self.style.WARNING(f'⟳ Categoría "{categoria_nombre}" actualizada')
                )
            
            # Crear o actualizar rubros de esta categoría
            for rubro_data in categoria_data['rubros']:
                rubro, created = Rubro.objects.get_or_create(
                    nombre=rubro_data['nombre'],
                    categoria=categoria,
                    defaults={'descripcion': rubro_data['descripcion']}
                )
                
                if created:
                    rubros_creados += 1
                    self.stdout.write(f'  └─ ✓ Rubro "{rubro_data["nombre"]}" creado')
                else:
                    rubros_actualizados += 1
                    rubro.descripcion = rubro_data['descripcion']
                    rubro.save()
                    self.stdout.write(f'  └─ ⟳ Rubro "{rubro_data["nombre"]}" actualizado')
            
            self.stdout.write('')
        
        # Resumen
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Resumen:'))
        self.stdout.write(self.style.SUCCESS(f'  • Categorías creadas: {categorias_creadas}'))
        self.stdout.write(self.style.SUCCESS(f'  • Categorías actualizadas: {categorias_actualizadas}'))
        self.stdout.write(self.style.SUCCESS(f'  • Total categorías: {categorias_creadas + categorias_actualizadas}'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'  • Rubros creados: {rubros_creados}'))
        self.stdout.write(self.style.SUCCESS(f'  • Rubros actualizados: {rubros_actualizados}'))
        self.stdout.write(self.style.SUCCESS(f'  • Total rubros: {rubros_creados + rubros_actualizados}'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        
        # Estadísticas por categoría
        self.stdout.write(self.style.SUCCESS('Rubros por categoría:'))
        for categoria in Categoria.objects.all():
            count = categoria.rubros.count()
            self.stdout.write(f'  📂 {categoria.nombre}: {count} rubros')
        self.stdout.write('')


"""
Comando para crear los planes de suscripción de prueba.
Uso: python manage.py crear_planes_test
"""
from django.core.management.base import BaseCommand
from apps.usuarios.models import Plan


class Command(BaseCommand):
    help = 'Crea los planes de suscripción para el entorno de test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando planes de test...'))
        
        planes = [
            {
                'code': 'free',
                'name': 'Gratis',
                'price_text': 'Gratis',
                'precio_mensual': 0.00,
                'fields_enabled': ['direccion','ciudad','provincia'],
                'max_images': 0,
                'max_videos': 0,
                'puede_crear_servicios': True,
                'puede_recibir_resenas': False,
                'puede_subir_media': False,
                'puede_ver_estadisticas': False,
                'max_servicios': 0,
                'is_active': True,
                'order': 1,
            },
            {
                'code': 'standard',
                'name': 'Estándar',
                'price_text': '$2.999/mes',
                'precio_mensual': 2999.00,
                'fields_enabled': ['direccion', 'telefono','ciudad','provincia'],  # Dirección y teléfono
                'max_images': 3,
                'max_videos': 0,
                'puede_crear_servicios': True,
                'puede_recibir_resenas': False,
                'puede_subir_media': True,
                'puede_ver_estadisticas': False,
                'max_servicios': 3,
                'is_active': True,
                'order': 2,
            },
            {
                'code': 'premium',
                'name': 'Premium',
                'price_text': '$9.999/mes',
                'precio_mensual': 9999.00,
                'fields_enabled': [
                    'direccion',
                    'telefono',
                    'ciudad',
                    'provincia',
                    'sitio_web',
                    'descripcion'
                ],  # Todos los campos
                'max_images': 10,
                'max_videos': 2,
                'puede_crear_servicios': True,
                'puede_recibir_resenas': True,
                'puede_subir_media': True,
                'puede_ver_estadisticas': True,
                'max_servicios': 10,
                'is_active': True,
                'order': 3,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for plan_data in planes:
            plan, created = Plan.objects.update_or_create(
                code=plan_data['code'],
                defaults=plan_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Plan "{plan.name}" creado exitosamente')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⟳ Plan "{plan.name}" actualizado')
                )
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Resumen:'))
        self.stdout.write(self.style.SUCCESS(f'  • Planes creados: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  • Planes actualizados: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'  • Total de planes: {created_count + updated_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        
        # Mostrar resumen de los planes
        self.stdout.write(self.style.SUCCESS('Planes configurados:'))
        self.stdout.write('')
        
        for plan in Plan.objects.filter(is_active=True).order_by('order'):
            self.stdout.write(self.style.SUCCESS(f'📦 {plan.name} ({plan.price_text})'))
            self.stdout.write(f'   • Código: {plan.code}')
            self.stdout.write(f'   • Precio: ${plan.precio_mensual}')
            self.stdout.write(f'   • Campos habilitados: {", ".join(plan.fields_enabled) if plan.fields_enabled else "Ninguno"}')
            self.stdout.write(f'   • Imágenes: {plan.max_images}')
            self.stdout.write(f'   • Videos: {plan.max_videos}')
            self.stdout.write(f'   • Servicios: {plan.max_servicios}')
            self.stdout.write(f'   • Reseñas: {"Sí" if plan.puede_recibir_resenas else "No"}')
            self.stdout.write(f'   • Estadísticas: {"Sí" if plan.puede_ver_estadisticas else "No"}')
            self.stdout.write('')


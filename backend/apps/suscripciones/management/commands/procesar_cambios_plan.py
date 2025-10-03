"""
Comando para procesar cambios de plan programados.
Este comando debe ser ejecutado por un cron job diariamente.

Uso:
    python manage.py procesar_cambios_plan
    
Cron job sugerido (diario a las 2 AM):
    0 2 * * * cd /app && python manage.py procesar_cambios_plan >> /var/log/cambios_plan.log 2>&1
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.suscripciones.models import CambioPlanProgramado
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Procesa los cambios de plan programados que están listos para ejecutarse'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué cambios se procesarían sin ejecutarlos',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        self.stdout.write(self.style.SUCCESS('=== Procesando Cambios de Plan ==='))
        self.stdout.write(f'Fecha actual: {timezone.now()}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: No se ejecutarán cambios reales'))
        
        # Obtener cambios pendientes que deben ejecutarse hoy o antes
        cambios_pendientes = CambioPlanProgramado.objects.filter(
            estado='pending',
            fecha_programada__lte=timezone.now()
        ).select_related('usuario', 'plan_actual', 'plan_nuevo', 'suscripcion_actual')
        
        total = cambios_pendientes.count()
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS('✓ No hay cambios pendientes para procesar'))
            return
        
        self.stdout.write(f'\n📋 Encontrados {total} cambios pendientes:\n')
        
        exitos = 0
        errores = 0
        
        for cambio in cambios_pendientes:
            tipo = "Upgrade" if cambio.es_upgrade else "Downgrade"
            self.stdout.write(
                f'\n  {cambio.id}. {cambio.usuario.username}: '
                f'{cambio.plan_actual.name} → {cambio.plan_nuevo.name} ({tipo})'
            )
            self.stdout.write(f'     Programado para: {cambio.fecha_programada}')
            
            if dry_run:
                self.stdout.write(self.style.WARNING('     [DRY-RUN] No se procesará'))
                continue
            
            # Procesar el cambio
            try:
                if cambio.procesar_cambio():
                    exitos += 1
                    self.stdout.write(self.style.SUCCESS('     ✓ Procesado exitosamente'))
                    logger.info(f'Cambio de plan procesado: {cambio.id} - {cambio.usuario.username}')
                else:
                    errores += 1
                    self.stdout.write(self.style.ERROR('     ✗ Error al procesar'))
                    logger.error(f'Error procesando cambio: {cambio.id}')
            except Exception as e:
                errores += 1
                self.stdout.write(self.style.ERROR(f'     ✗ Excepción: {str(e)}'))
                logger.exception(f'Excepción procesando cambio {cambio.id}: {str(e)}')
        
        # Resumen
        self.stdout.write('\n' + '='*50)
        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Resumen:'))
            self.stdout.write(f'  Total procesados: {exitos + errores}')
            self.stdout.write(self.style.SUCCESS(f'  Exitosos: {exitos}'))
            if errores > 0:
                self.stdout.write(self.style.ERROR(f'  Con errores: {errores}'))
        else:
            self.stdout.write(self.style.WARNING(f'\n[DRY-RUN] Se procesarían {total} cambios'))
        
        self.stdout.write('\n' + '='*50 + '\n')
        
        # También procesar suscripciones vencidas
        self.stdout.write(self.style.SUCCESS('\n=== Verificando Suscripciones Vencidas ===\n'))
        
        from apps.suscripciones.models import Suscripcion
        suscripciones_vencidas = Suscripcion.objects.filter(
            activa=True,
            fecha_fin__lt=timezone.now()
        ).select_related('usuario', 'plan')
        
        vencidas_count = suscripciones_vencidas.count()
        
        if vencidas_count == 0:
            self.stdout.write(self.style.SUCCESS('✓ No hay suscripciones vencidas'))
        else:
            self.stdout.write(f'📋 Encontradas {vencidas_count} suscripciones vencidas:\n')
            
            for suscripcion in suscripciones_vencidas:
                self.stdout.write(
                    f'  - {suscripcion.usuario.username}: {suscripcion.plan.name} '
                    f'(Vencida: {suscripcion.fecha_fin})'
                )
                
                if not dry_run:
                    suscripcion.desactivar_suscripcion()
                    self.stdout.write(self.style.SUCCESS('    ✓ Desactivada'))
                    logger.info(f'Suscripción vencida desactivada: {suscripcion.id}')
                else:
                    self.stdout.write(self.style.WARNING('    [DRY-RUN] Se desactivaría'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Proceso completado\n'))

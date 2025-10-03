#!/bin/bash

# ================================================
# Script para configurar Cron Job - Cambio de Planes
# ================================================
#
# Este script ayuda a configurar el cron job para
# procesar cambios de plan programados automáticamente.
#
# Uso:
#   chmod +x cron-setup.sh
#   ./cron-setup.sh
#
# ================================================

echo "================================================"
echo "  Configuración de Cron Job"
echo "  Sistema de Cambio de Planes"
echo "================================================"
echo ""

# Detectar directorio del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "📁 Directorio del proyecto: $PROJECT_DIR"
echo ""

# Determinar comando según entorno
read -p "¿Usar Docker? (s/n): " use_docker

if [ "$use_docker" = "s" ] || [ "$use_docker" = "S" ]; then
    COMMAND="cd $PROJECT_DIR && docker exec deconfianza-web-backend-dev-1 python manage.py procesar_cambios_plan"
    echo "✅ Comando configurado para Docker"
else
    read -p "Ruta al virtualenv (o enter para omitir): " venv_path
    if [ -n "$venv_path" ]; then
        COMMAND="cd $PROJECT_DIR && source $venv_path/bin/activate && python manage.py procesar_cambios_plan"
    else
        COMMAND="cd $PROJECT_DIR && python manage.py procesar_cambios_plan"
    fi
    echo "✅ Comando configurado para entorno local"
fi

echo ""
echo "================================================"
echo "  Opciones de Configuración"
echo "================================================"
echo ""
echo "1. Diario a las 2 AM (recomendado)"
echo "2. Cada 6 horas"
echo "3. Cada hora"
echo "4. Personalizado"
echo ""
read -p "Selecciona opción [1-4]: " schedule_option

case $schedule_option in
    1)
        CRON_SCHEDULE="0 2 * * *"
        DESCRIPTION="Diario a las 2 AM"
        ;;
    2)
        CRON_SCHEDULE="0 */6 * * *"
        DESCRIPTION="Cada 6 horas"
        ;;
    3)
        CRON_SCHEDULE="0 * * * *"
        DESCRIPTION="Cada hora"
        ;;
    4)
        read -p "Ingresa cron schedule (ej: 0 2 * * *): " custom_schedule
        CRON_SCHEDULE="$custom_schedule"
        DESCRIPTION="Personalizado"
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

# Configurar log file
LOG_FILE="$PROJECT_DIR/logs/cambios_plan.log"
mkdir -p "$PROJECT_DIR/logs"

# Crear entrada de cron
CRON_LINE="$CRON_SCHEDULE $COMMAND >> $LOG_FILE 2>&1"

echo ""
echo "================================================"
echo "  Resumen de Configuración"
echo "================================================"
echo ""
echo "📅 Schedule: $DESCRIPTION"
echo "🕒 Cron: $CRON_SCHEDULE"
echo "💻 Comando: $COMMAND"
echo "📝 Log: $LOG_FILE"
echo ""
echo "Línea de cron:"
echo "----------------------------------------"
echo "$CRON_LINE"
echo "----------------------------------------"
echo ""

read -p "¿Agregar a crontab? (s/n): " add_to_cron

if [ "$add_to_cron" = "s" ] || [ "$add_to_cron" = "S" ]; then
    # Backup del crontab actual
    crontab -l > "$PROJECT_DIR/crontab.backup" 2>/dev/null
    echo "💾 Backup creado: crontab.backup"
    
    # Verificar si ya existe
    if crontab -l 2>/dev/null | grep -q "procesar_cambios_plan"; then
        echo "⚠️  Ya existe una entrada similar en crontab"
        read -p "¿Deseas reemplazarla? (s/n): " replace
        
        if [ "$replace" = "s" ] || [ "$replace" = "S" ]; then
            # Remover línea anterior
            crontab -l 2>/dev/null | grep -v "procesar_cambios_plan" | crontab -
            echo "🗑️  Entrada anterior removida"
        else
            echo "❌ Operación cancelada"
            exit 0
        fi
    fi
    
    # Agregar nueva línea
    (crontab -l 2>/dev/null; echo ""; echo "# DeConfianza - Procesar cambios de plan"; echo "$CRON_LINE") | crontab -
    
    echo ""
    echo "✅ ¡Cron job configurado exitosamente!"
    echo ""
    echo "Para verificar:"
    echo "  crontab -l"
    echo ""
    echo "Para ver logs:"
    echo "  tail -f $LOG_FILE"
    echo ""
    echo "Para probar manualmente:"
    echo "  $COMMAND"
    echo ""
else
    echo ""
    echo "📋 Copia esta línea manualmente:"
    echo ""
    echo "$CRON_LINE"
    echo ""
    echo "Y agrégala con:"
    echo "  crontab -e"
    echo ""
fi

echo "================================================"
echo "  🎉 Configuración Completa"
echo "================================================"
echo ""
echo "💡 Tip: Prueba primero con --dry-run:"
echo "   $COMMAND --dry-run"
echo ""

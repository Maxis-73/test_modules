#!/bin/bash

# Configuración
REPO_URL="LINK_DEL_REPOSITORIO"
BRANCH="RAMA_DEL_REPOSITORIO"
REPO_DIR="/tmp/odoo_modules_repo"
ADDONS_DIR="/opt/odoo/custom-addons"  # Según tu instalación
LOG_FILE="/opt/odoo/logs/module_updates.log"

# Función para registrar logs
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Crear directorio de logs si no existe
mkdir -p $(dirname $LOG_FILE)

log "Iniciando actualización de módulos Odoo"

# Clonar o actualizar el repositorio
if [ -d "$REPO_DIR" ]; then
    log "Actualizando repositorio existente"
    cd $REPO_DIR
    git fetch --all
    git reset --hard origin/$BRANCH
    git clean -fd
else
    log "Clonando repositorio por primera vez"
    git clone -b $BRANCH $REPO_URL $REPO_DIR
    cd $REPO_DIR
fi

# Crear directorio de addons si no existe
mkdir -p $ADDONS_DIR

# Sincronizar módulos (ajusta según la estructura de tu repo)
log "Sincronizando módulos"
rsync -av --delete $REPO_DIR/modulos/ $ADDONS_DIR/

# Ajustar permisos
log "Ajustando permisos"
chown -R odoo:odoo $ADDONS_DIR
chmod -R 755 $ADDONS_DIR

# Reiniciar Odoo
log "Reiniciando servicio Odoo"
systemctl restart odoo

log "Actualización completada con éxito"
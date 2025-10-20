# Odoo Docker Setup

Este setup te permite ejecutar Odoo localmente con todos los addons del directorio actual disponibles.

## Requisitos

- Docker
- Docker Compose

## Instrucciones de uso

### 1. Iniciar los servicios

```bash
docker-compose up -d
```

### 2. Acceder a Odoo

- URL: http://localhost:8069
- Usuario administrador: admin
- Contraseña de base de datos: admin123

### 3. Crear una nueva base de datos

1. Ve a http://localhost:8069
2. Haz clic en "Create database"
3. Completa los campos:
   - Database name: `odoo_dev` (o el nombre que prefieras)
   - Email: tu email
   - Password: la contraseña que desees
   - Language: Spanish / Español
   - Country: tu país

### 4. Instalar addons personalizados

Una vez creada la base de datos, ve a:
- Aplicaciones → Actualizar lista de aplicaciones
- Busca tus addons personalizados:
  - botpress_ai
  - brand_ambassador
  - device_management
  - google_cloud_storage
  - isp_mikrotik
  - livechat_ai
  - mini_bank
  - payment_facilitator
  - smarty
  - storage_abstraction

### 5. Comandos útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f odoo

# Reiniciar solo Odoo (útil durante desarrollo)
docker-compose restart odoo

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes (CUIDADO: elimina la base de datos)
docker-compose down -v
```

### 6. Desarrollo

- Los archivos en el directorio actual están montados en `/mnt/extra-addons` dentro del contenedor
- Odoo está configurado en modo desarrollo con auto-reload
- Cualquier cambio en los archivos Python se reflejará automáticamente

### 7. Troubleshooting

Si tienes problemas:

1. Verifica que los puertos 8069 y 5432 estén libres
2. Revisa los logs: `docker-compose logs`
3. Reinicia los servicios: `docker-compose restart`

### 8. Dependencias externas de Python (pip dentro del contenedor)

Para instalar librerías de Python adicionales en el contenedor de Odoo:

#### 8.1 Instalar desde `requirements.txt`

Coloca tus dependencias en `requirements.txt` en la raíz del repo (ya existe uno). Dentro del contenedor, el archivo se monta en `/mnt/extra-addons/requirements.txt`.

```bash
# Instalar como root dentro del contenedor (PEP 668: usar --break-system-packages)
docker compose exec -u root odoo python3 -m pip install --no-cache-dir --break-system-packages -r /mnt/extra-addons/requirements.txt

# Reiniciar Odoo para que tome los paquetes
docker compose restart odoo
```

#### 8.2 Instalar un paquete puntual

```bash
docker compose exec -u root odoo python3 -m pip install --no-cache-dir --break-system-packages openpyxl==3.1.5
docker compose restart odoo
```

#### Notas

- Las instalaciones hechas con `exec` persisten mientras el contenedor exista. Si eliminas y recreas el contenedor, tendrás que reinstalarlas.
- Para entornos reproducibles, se recomienda construir una imagen personalizada que incluya las dependencias (opcional):

```Dockerfile
FROM odoo:18.0
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt
```

Y en `docker-compose.yml` (o un override) referenciar la imagen construida:

```yaml
services:
  odoo:
    build: .
    image: odoo:18.0-custom
```

#### 8.3 Troubleshooting: "externally-managed-environment"

Si ves este error al instalar con pip dentro del contenedor:

```
error: externally-managed-environment
This environment is externally managed ... See PEP 668 ...
```

Solución rápida: usa el flag `--break-system-packages` como se muestra en los comandos anteriores.

Alternativa avanzada: crear un virtualenv dentro del contenedor y usarlo (requiere ajustar cómo se inicia Odoo si quieres usar siempre ese venv):

```bash
docker compose exec -u root odoo python3 -m venv /opt/odoo-venv
docker compose exec -u root odoo /opt/odoo-venv/bin/pip install --no-cache-dir -r /mnt/extra-addons/requirements.txt
# Para una sesión interactiva con el venv
docker compose exec -u root odoo bash -lc 'source /opt/odoo-venv/bin/activate && python -m pip list'
```

## Estructura de archivos

- `docker-compose.yml`: Configuración de servicios
- `odoo.conf`: Configuración de Odoo
- `./*`: Todos los addons personalizados 
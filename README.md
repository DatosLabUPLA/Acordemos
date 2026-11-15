# Acordemos en Docker

Acordemos usa Python 3.5.10 y Django 1.11.7. El archivo `compose.yaml`
define Gunicorn, Nginx y el almacenamiento persistente para Coolify.

## Desplegar en Coolify desde GitHub

1. Carga por SSH o SFTP una copia consistente de `GestorAcuerdos.sqlite3` y
   `media/` en el servidor de destino. Desde el directorio que contiene ese
   respaldo, prepara el montaje antes del primer despliegue:

   ```sh
   sudo install -d -m 0700 -o 10001 -g 10001 /srv/acordemos/data
   sudo install -d -m 0755 -o 10001 -g 10001 /srv/acordemos/data/media
   sudo install -m 0600 -o 10001 -g 10001 GestorAcuerdos.sqlite3 /srv/acordemos/data/
   sudo cp -a media/. /srv/acordemos/data/media/
   sudo chown -R 10001:10001 /srv/acordemos/data/media
   sudo chmod -R u=rwX,go=rX /srv/acordemos/data/media
   ```

   Usa el bloque anterior para la carga inicial. Para el corte final, detén
   las escrituras en origen y restaura el respaldo definitivo con la aplicación
   de destino detenida.

2. Sube los cambios al fork. En Coolify crea una aplicación desde el repositorio
   de GitHub y la rama que elegiste. Selecciona **Docker Compose**, con
   **Base Directory** `/` y **Docker Compose Location** `/compose.yaml`.
   Si ya creaste el recurso, ajusta la ruta, guarda y pulsa **Load Compose**.

3. Define estas variables en Coolify:

   | Variable | Valor |
   | --- | --- |
   | `DJANGO_SECRET_KEY` | Una clave aleatoria persistente para este entorno. |
   | `DJANGO_ALLOWED_HOSTS` | Nombre del dominio sin esquema ni puerto. Para varios dominios, sepáralos por comas sin espacios. |
   | `GOOGLE_OAUTH2_KEY` y `GOOGLE_OAUTH2_SECRET` | ID y secreto del cliente OAuth. En Google Cloud registra `https://acordemos.datoslab.cl/auth/google/callback` como URI de redireccionamiento autorizada, sin barra final. |
   | `DJANGO_EMAIL_BACKEND` | Usa `django.core.mail.backends.smtp.EmailBackend` para habilitar correo. Por defecto el correo se descarta. |
   | `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | Configuración SMTP si habilitas correo. El puerto por defecto es 587 con STARTTLS. |

4. Asigna el dominio HTTPS al servicio **web**, con puerto interno **8000**. El
   proxy de Coolify usa su entrada HTTPS habitual. Compose no publica un
   puerto del host, por lo que otras aplicaciones pueden usar su propio
   puerto interno 8000. Gunicorn atiende en `django` y Nginx sirve estáticos y
   adjuntos bajo las rutas que usa el proyecto.

5. Despliega y prueba el acceso, los adjuntos y una escritura controlada.
   Reconstruye y comprueba que el dato siga presente. Cada despliegue monta
   el mismo directorio. Las migraciones se ejecutan por separado, después de
   revisar el plan y respaldar la base.

Mantén un respaldo consistente de SQLite y una copia de los adjuntos fuera del
servidor de Coolify. La aplicación usa un solo worker de Gunicorn para reducir
la contención de SQLite. Despliega una sola réplica de Django por directorio de
datos.

El SQLite y `Administrador.txt` del fork se retiran del árbol actual. Las
revisiones anteriores conservan el contenido que ya había sido publicado.

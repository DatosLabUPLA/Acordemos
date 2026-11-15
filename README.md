# Acordemos en Docker

Acordemos usa Python 3.5.10 y Django 1.11.7. El archivo `compose.yaml`
define Gunicorn, Nginx y el almacenamiento persistente para Coolify.

## Desplegar en Coolify desde GitHub

1. Sube los cambios al fork. En Coolify crea una aplicación desde el repositorio
   de GitHub y la rama que elegiste. Selecciona **Docker Compose**, con
   **Base Directory** `/` y **Docker Compose Location** `/compose.yaml`.
   Si ya creaste el recurso, ajusta la ruta, guarda y pulsa **Load Compose**.

2. Define estas variables en Coolify:

   | Variable | Valor |
   | --- | --- |
   | `DJANGO_SECRET_KEY` | Una clave aleatoria persistente para este entorno. |
   | `DJANGO_ALLOWED_HOSTS` | Nombre del dominio sin esquema ni puerto. Para varios dominios, sepáralos por comas sin espacios. |
   | `GOOGLE_OAUTH2_KEY` y `GOOGLE_OAUTH2_SECRET` | ID y secreto del cliente OAuth. En Google Cloud registra `https://acordemos.datoslab.cl/auth/google/callback` como URI de redireccionamiento autorizada, sin barra final. |
   | `DJANGO_EMAIL_BACKEND` | Usa `django.core.mail.backends.smtp.EmailBackend` para habilitar correo. Por defecto el correo se descarta. |
   | `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | Configuración SMTP si habilitas correo. El puerto por defecto es 587 con STARTTLS. |

3. Asigna el dominio HTTPS al servicio **web**, con puerto interno **8000**. El
   proxy de Coolify usa su entrada HTTPS habitual. Compose no publica un
   puerto del host, por lo que otras aplicaciones pueden usar su propio
   puerto interno 8000. Gunicorn atiende en `django` y Nginx sirve estáticos y
   adjuntos bajo las rutas que usa el proyecto.

4. Despliega. Docker crea el volumen `acordemos-data`. Si falta SQLite, la
   página muestra un aviso y el servicio `django` sigue disponible en **Files**.
5. Abre **Acordemos → Files → django → /data/import**. Sube un respaldo
   consistente con el nombre exacto `GestorAcuerdos.sqlite3`. Para los adjuntos,
   sube el contenido de `media/` a `/data/media/` conservando sus subcarpetas.
6. Pulsa **Redeploy**. El arranque prepara los permisos y mueve el respaldo a
   `/data/GestorAcuerdos.sqlite3` si todavía falta la base activa. Comprueba que
   la portada, el acceso y los adjuntos funcionen.

La carpeta `/data/import` es para la primera carga. Un respaldo que se suba
ahí después no sobrescribe la base activa. Las migraciones se ejecutan por
separado, después de revisar el plan y respaldar la base.

El volumen existe fuera de los contenedores y se reutiliza en cada redeploy
del mismo recurso de Coolify. Conserva el recurso y su volumen. Si venías de
la versión con `/srv/acordemos/data`, sube al volumen una copia consistente
de esa base si está disponible. En caso contrario, usa el último respaldo.

Mantén un respaldo consistente de SQLite y una copia de los adjuntos fuera del
servidor de Coolify. La aplicación usa un solo worker de Gunicorn para reducir
la contención de SQLite. Despliega una sola réplica de Django por directorio de
datos.

El SQLite y `Administrador.txt` del fork se retiran del árbol actual. Las
revisiones anteriores conservan el contenido que ya había sido publicado.

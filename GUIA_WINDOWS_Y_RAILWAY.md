# Laboratorio Django + MySQL | Guía práctica para Windows y Railway

**Basado en el README-DJANGO-PRACTICA-1.md del catedrático.**
Esta entrega incluye el código completo para registro, login, logout, recuperación de contraseña y alta/listado de clientes. Está preparada para Windows + MySQL local y despliegue en Railway + MySQL. No incluye evidencia ficticia.

## A. Requisitos

- Python 3.12 o 3.13, pip y Git instalado.
- XAMPP (con MySQL iniciado) o instalación propia de MySQL.
- Editor VS Code.
- Cuenta GitHub y Railway para publicar.

## B. Ejecutar en Windows (PowerShell)

1. Descomprime el ZIP. Abre PowerShell **dentro de la carpeta `django_clientes`** (donde está `manage.py`).
2. Ejecuta:

```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Si no tienes Python 3.13, usa `py -3.12 -m venv venv` (o `python -m venv venv`).
Si PowerShell no permite la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

3. Abre `.env` en VS Code y configura el usuario y contraseña **reales** de tu MySQL local. Por defecto la guía usa `root` sin contraseña, pero podría diferir en tu instalación.
4. Inicia MySQL (por ejemplo, XAMPP) y crea la BD desde phpMyAdmin, en la pestaña SQL:

```sql
CREATE DATABASE django_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. Vuelve a PowerShell:

```powershell
python manage.py check
python manage.py migrate
python manage.py runserver
```

6. Abre **http://127.0.0.1:8000/registro/**, crea usuario e inicia sesión. En **http://127.0.0.1:8000/clientes/**, registra al menos un cliente y confirma el listado. Cierra sesión e intenta ingresar de nuevo a `/clientes/` para comprobar el redireccionamiento al login.

### Capturas de la parte local

- **Evidencia 1:** terminal PowerShell mostrando `(venv)` y `Starting development server at http://127.0.0.1:8000/`.
- **Evidencia 2 (recomendada):** formulario de login o registro visible en el navegador.
- **Evidencia 3 (recomendada):** clientes guardados en listado; si es posible, phpMyAdmin mostrando la tabla `clientes_cliente`.

## C. Subir el código a GitHub

Abre **otra terminal** en `django_clientes` (donde está `manage.py`):

```powershell
git init
git add .
git commit -m "Laboratorio Django con autenticacion y clientes"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

Crea primero un repositorio **vacío** en GitHub y sustituye la URL. **Revisa que `.env` NO figure en `git status`**; el `.gitignore` incluido lo excluye. Nunca subas contraseñas ni `venv`.

## D. Desplegar en Railway con MySQL (recomendación)

1. En https://railway.com/ entra con tu cuenta. Crea un proyecto y selecciona **Deploy from GitHub repo**; autoriza el repositorio si la plataforma lo pide.
2. Agrega **un servicio de base de datos MySQL** al mismo proyecto (`+ New` → `Database` → `MySQL`). Confirma el nombre que Railway da al servicio (por ejemplo `MySQL`).
3. Selecciona tu servicio **web** → `Variables` y crea estas referencias al servicio MySQL. Si el servicio tiene otro nombre, cámbialo dentro de `${{ ... }}`:

| Variable web | Valor de ejemplo si el servicio se llama MySQL |
|---|---|
| `DB_NAME` | `${{MySQL.MYSQLDATABASE}}` |
| `DB_USER` | `${{MySQL.MYSQLUSER}}` |
| `DB_PASSWORD` | `${{MySQL.MYSQLPASSWORD}}` |
| `DB_HOST` | `${{MySQL.MYSQLHOST}}` |
| `DB_PORT` | `${{MySQL.MYSQLPORT}}` |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_SECRET_KEY` | Una clave aleatoria larga, que NO se publica |
| `DJANGO_ALLOWED_HOSTS` | `tu-dominio.up.railway.app` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://tu-dominio.up.railway.app` |

4. Para generar una clave, desde tu Windows con Django instalado:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. Ve a `Settings` → `Networking` del servicio web, genera un dominio público de Railway. Copia el host exactamente a `DJANGO_ALLOWED_HOSTS` (sin `https://`) y la URL a `DJANGO_CSRF_TRUSTED_ORIGINS` (con `https://`). Guarda las variables y **despliega los cambios pendientes**.
6. El repositorio trae `railway.json` y `start.sh`. Este último ejecuta **migrate → collectstatic → gunicorn**, y utiliza el puerto dinámico de Railway. Comprueba en `Deployments` que aparece **SUCCESS/Active** y que los logs no reportan errores de conexión.
7. Abre el dominio público de Railway y verifica `/registro/`, `/login/` y `/clientes/`.

**ATENCIÓN:** Railway puede aplicar límites de prueba y cargos si se exceden los créditos del plan; revisa el precio vigente antes de dejar el proyecto encendido.

### Capturas del despliegue

- **Evidencia 4:** Railway → Deployments del servicio web con estado `SUCCESS` o `Active`.
- **Evidencia 5:** panel de servicio MySQL en estado activo (evita mostrar credenciales).
- **Evidencia 6:** sitio alojado en el dominio HTTPS, mostrando login y clientes.
- Copia la URL completa al PDF final; el enlace solo cuenta si abre en internet y permite validar el sistema.

## E. Correo de recuperación

Por defecto la guía usa `django.core.mail.backends.console.EmailBackend`. Eso **no envía correos reales**: el enlace aparece en la terminal en local o en logs del hosting. Si el docente exige comprobar recuperación de contraseña con correos en la web publicada, configura `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` y puerto usando un proveedor de correo autorizado. No pegues credenciales en el código ni las capturas.

## F. Comprobación adicional

```powershell
python manage.py test
python manage.py check --deploy
```

`check --deploy` puede advertir sobre aspectos adicionales de seguridad: las recomendaciones deben revisarse según el entorno. Los tests automáticos requieren dependencias instaladas y acceso a MySQL; para ejecutar pruebas básicas de lógica sin un servidor MySQL, puedes cambiar temporalmente `DB_ENGINE=sqlite` en `.env`, pero eso **no equivale** a completar el laboratorio con MySQL.

## G. Contenido del PDF final

1. Carátula: universidad, carrera, curso, título, estudiante, carné, docente, fecha.
2. Evidencia local, capturas reales de terminal y pantallas.
3. Evidencia del proceso de despliegue y base de datos en Railway.
4. URL HTTPS pública y prueba del funcionamiento.

**Nota académica:** el documento entregado en este paquete es una plantilla con espacios marcados para capturas y enlace real; no puede presentarse como si ya existieran esas evidencias.

Fuentes técnicas: 
- Guía del laboratorio (README-DJANGO-PRACTICA-1.md).
- https://docs.djangoproject.com/en/6.0/faq/install/
- https://docs.railway.com/databases/mysql
- https://railway.com/guides/django
- https://docs.railway.com/pricing/free-trial

## H. Problemas frecuentes

- **MySQL Server has gone away / Can't connect to MySQL server:** activa MySQL y revisa `.env` (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`).
- **Unsupported MariaDB server version:** verifica la versión real de MariaDB en XAMPP. Django 6 requiere MariaDB 10.6+ o MySQL 8.0.11+, así que algunos XAMPP antiguos son incompatibles. Usa una versión de base compatible; no cambies silenciosamente a SQLite si el docente exige MySQL.
- **DisallowedHost en Railway:** copia el dominio asignado a `DJANGO_ALLOWED_HOSTS` sin `https://`.
- **403 CSRF verification failed en Railway:** agrega la URL con `https://` a `DJANGO_CSRF_TRUSTED_ORIGINS`, guarda variables y vuelve a desplegar.
- **502 / Application failed to respond:** revisa el log de deployments; verifica que se ejecuta `bash start.sh`, que MySQL está activo y que Railway pasa `PORT` automáticamente.
- **Sin CSS:** verifica que `collectstatic` se ejecuta en el arranque y que WhiteNoise está en `MIDDLEWARE`.
- **No llega el correo de recuperación:** sin `SMTP_HOST`, el proyecto usa la salida de consola, como la guía; eso no envía email real.

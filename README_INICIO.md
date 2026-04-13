# Guía de Inicio — Sistema de Gestión de Pedidos

Documentación para que otros desarrolladores levanten el proyecto desde cero en su entorno local.

---

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

| Herramienta | Versión mínima |
|---|---|
| Python | 3.11+ |
| MySQL | 8.0+ |
| pip | 24+ |


---

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd gestion_pedidos3Juanes.1
```

---

## 2. Crear y activar el entorno virtual


#borrar la carpeta env si existe

```bash
# Crear entorno virtual
python -m venv env

# Activar en Windows
env\Scripts\activate

## 3. Instalar dependencias

#recomendable utilizar solo el cmd(command prompt)
pip install -r requeriments.txt
```

> **Nota:** El paquete `mysqlclient` requiere que MySQL esté instalado en el sistema. En Windows puede ser necesario instalar primero las 
1
#Primero instala el motor de la base de datos
#https://dev.mysql.com/downloads/installer/ 
2
#Despues la interfaz grafica de MYSQL WORKBENCH
#https://dev.mysql.com/downloads/workbench/

---

## 4. Configurar la base de datos MySQL

### 4.1 Crear la base de datos

Conéctate a tu servidor MySQL y crea la base de datos:

```sql
CREATE DATABASE gestion_pedidos_Juanes
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

> El archivo `estructura_mysql_gestion_pedidos.txt` contiene el DDL completo de las tablas como referencia.

### 4.2 Configurar credenciales en settings.py

Abre `proyecto_pedidos/settings.py` y ajusta el bloque `DATABASES` con tus datos:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_pedidos_Juanes',
        'USER': 'root',          # tu usuario MySQL
        'PASSWORD': 'tu_pass',   # tu contraseña MySQL
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

> **Seguridad:** No cometas credenciales reales al repositorio. Usa variables de entorno o un archivo `.env` ignorado por Git en producción.

---

## 5. Aplicar migraciones

Crea las migraciones
```bash
python manage.py makemigrations clientes productos pedidos
```

Luego ejecuta las migraciones para crear las tablas en la base de datos
```bash
python manage.py migrate
```


---

## 7. Levantar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación quedará disponible en: **http://127.0.0.1:8000/**

---

## 8. Acceso al sistema

| URL | Descripción |
|---|---|
| `http://127.0.0.1:8000/` | Dashboard principal |
| `http://127.0.0.1:8000/login/` | Inicio de sesión |
| `http://127.0.0.1:8000/registro/` | Registro de usuario |
| `http://127.0.0.1:8000/admin/` | Panel de administración Django |

---

## 9. API REST

La API vive bajo el prefijo `/api/`. Consulta [README_ENDPOINTS.md](README_ENDPOINTS.md) para el listado completo.

### Obtener token JWT

```http
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

### Usar el token en Postman / curl

Agrega el header en cada petición protegida:

```
Authorization: Bearer <token_recibido>
```

### Recursos disponibles en la API

| Recurso | URL base |
|---|---|
| Clientes | `/api/clientes/` |
| Productos | `/api/productos/` |
| Pedidos | `/api/pedidos/` |
| Detalles de pedido | `/api/detalles/` |

Todos los recursos admiten operaciones CRUD estándar (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).

---

## 10. Estructura del proyecto

```
proyecto_pedidos/       # Configuración principal (settings, urls, wsgi)
├── clientes/           # App de clientes (modelos, vistas, formularios)
├── pedidos/            # App central: pedidos, detalles, API, exportaciones
│   ├── api_urls.py     # Rutas de la API REST
│   ├── api_views.py    # ViewSets de DRF
│   ├── authentication.py  # Clase JWT personalizada
│   ├── reportes.py     # Generación PDF / Excel
│   └── views/          # Vistas divididas por módulo
└── productos/          # App de productos (modelos, vistas, formularios)
```

---

## 11. Stack tecnológico

- **Backend:** Python 3.11+ · Django 6.0 · Django REST Framework 3.16
- **Base de datos:** MySQL 8.0+ · mysqlclient 2.2.8
- **Frontend:** Bootstrap 5 · Bootstrap Icons · SweetAlert2
- **Exportaciones:** ReportLab (PDF) · openpyxl (Excel)
- **Autenticación:** JWT personalizado + sesiones Django

---

## Solución de problemas frecuentes

| Error | Causa probable | Solución |
|---|---|---|
| `django.db.utils.OperationalError` | Credenciales o base de datos incorrectas | Revisar bloque `DATABASES` en settings.py |
| `ModuleNotFoundError: MySQLdb` | mysqlclient no instalado correctamente | Reinstalar `mysqlclient` con las C libraries de MySQL |
| `No module named 'proyecto_pedidos'` | Ejecutar `manage.py` fuera de la raíz del proyecto | Correr todos los comandos desde la carpeta raíz |
| Redirige a `/login/` en todos los endpoints | No estás autenticado | Iniciar sesión en `/login/` o usar token JWT |

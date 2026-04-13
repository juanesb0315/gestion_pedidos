# README de Endpoints para Pruebas

Este documento resume los endpoints actuales del proyecto para pruebas funcionales.

Base URL local:
http://127.0.0.1:8000/

## 1) Antes de probar

1. Levanta el servidor:
python manage.py runserver

2. Inicia sesion en:
http://127.0.0.1:8000/login/

Nota:
- Casi todos los endpoints requieren autenticacion.
- Si no estas autenticado, veras redireccion 302 a /login/.

## 2) Endpoints de autenticacion

- GET /login/
- POST /login/
- GET /logout/
- GET /registro/
- POST /registro/

## 3) Endpoints de pedidos

- GET /
- GET /listar/
- GET /crear/
- POST /crear/
- GET /editar/<id_pedido>/
- POST /editar/<id_pedido>/
- GET /eliminar/<id_pedido>/
- GET /detalle/<id_pedido>/

## 4) Endpoints de clientes

- GET /clientes/
- GET /clientes/crear/
- POST /clientes/crear/
- GET /clientes/editar/<id_cliente>/
- POST /clientes/editar/<id_cliente>/
- GET /clientes/eliminar/<id_cliente>/

## 5) Endpoints de productos

- GET /productos/
- GET /productos/crear/
- POST /productos/crear/
- GET /productos/editar/<id_producto>/
- POST /productos/editar/<id_producto>/
- GET /productos/eliminar/<id_producto>/

## 6) Endpoints de detalles

- GET /detalles/
- GET /pedido/<id_pedido>/agregar/
- POST /pedido/<id_pedido>/agregar/
- GET /detalle/editar/<id_detalle>/
- POST /detalle/editar/<id_detalle>/
- GET /detalle/eliminar/<id_detalle>/

## 7) Endpoints de exportacion PDF

- GET /exportar/pedidos/pdf/
- GET /exportar/clientes/pdf/
- GET /exportar/productos/pdf/
- GET /exportar/detalles/pdf/

## 8) Endpoints de exportacion Excel

- GET /exportar/pedidos/excel/
- GET /exportar/clientes/excel/
- GET /exportar/productos/excel/
- GET /exportar/detalles/excel/
- GET /exportar/todo/excel/

## 9) Endpoint de administracion

- GET /admin/

## 10) Prueba rapida con PowerShell

Si quieres verificar que endpoints privados redirigen a login cuando no hay sesion:

Invoke-WebRequest -Uri "http://127.0.0.1:8000/clientes/" -MaximumRedirection 0

Invoke-WebRequest -Uri "http://127.0.0.1:8000/exportar/clientes/excel/" -MaximumRedirection 0

Esperado:
- StatusCode 302
- Header Location con /login/?next=...

## 11) Resumen de estados esperados

- 200: pagina cargada correctamente
- 302: redireccion (normalmente a login por falta de sesion)
- 404: ruta incorrecta o recurso inexistente
- 500: error interno del servidor

## 12) Nota importante

Aunque aqui se usa la palabra API, este proyecto actualmente es mayormente web renderizada por Django (templates) con endpoints de CRUD y exportacion.
No es una API REST formal con JSON para todas las entidades.

## 13) API REST JSON (nuevo)

Ahora tambien existe una API REST en paralelo para usar con Postman.

Base API:
http://127.0.0.1:8000/api/

Endpoints disponibles:

- POST /api/token/  (obtiene JWT para Postman)
body:
{
"username": "juanes",
"password": "123456789"
}

- GET /api/clientes/
- POST /api/clientes/
- GET /api/clientes/<id>/
- PUT /api/clientes/<id>/
- PATCH /api/clientes/<id>/
- DELETE /api/clientes/<id>/

- GET /api/productos/
- POST /api/productos/
- GET /api/productos/<id>/
- PUT /api/productos/<id>/
- PATCH /api/productos/<id>/
- DELETE /api/productos/<id>/

- GET /api/pedidos/
- POST /api/pedidos/
- GET /api/pedidos/<id>/
- PUT /api/pedidos/<id>/
- PATCH /api/pedidos/<id>/
- DELETE /api/pedidos/<id>/

- GET /api/detalles/
- POST /api/detalles/
- GET /api/detalles/<id>/
- PUT /api/detalles/<id>/
- PATCH /api/detalles/<id>/
- DELETE /api/detalles/<id>/

Notas:
- GET es publico (solo lectura).
- POST, PUT, PATCH y DELETE requieren usuario autenticado.
- /api/token/ solo acepta POST (si usas GET devuelve 405).
- Puedes usar login de DRF en: /api-auth/login/




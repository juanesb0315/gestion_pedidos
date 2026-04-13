"""
WSGI config for proyecto_pedidos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# define modulo de settings para wsgi
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_pedidos.settings')

# instancia la aplicacion wsgi
application = get_wsgi_application()

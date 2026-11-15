"""
WSGI config for Acordemos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Acordemos.settings")

django_application = get_wsgi_application()
database_path = settings.DATABASES['default']['NAME']


def application(environ, start_response):
    if not (os.access(database_path, os.R_OK | os.W_OK)
            and os.path.getsize(database_path) > 0):
        start_response('503 Service Unavailable', [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ('Cache-Control', 'no-store'),
        ])
        return [b'Acordemos: pendiente de restaurar la base de datos.\n']
    return django_application(environ, start_response)

"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

from configurations.wsgi import get_wsgi_application
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")
application = get_wsgi_application()

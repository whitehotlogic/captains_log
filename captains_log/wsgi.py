"""
WSGI config for captains_log project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""


import os

from logbook_app.logbook import Logbook
from django.core.wsgi import get_wsgi_application
from captains_log.logging_config import set_up_logging

set_up_logging()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "captains_log.settings")

application = get_wsgi_application()
Logbook().initiate_hourly_entries()

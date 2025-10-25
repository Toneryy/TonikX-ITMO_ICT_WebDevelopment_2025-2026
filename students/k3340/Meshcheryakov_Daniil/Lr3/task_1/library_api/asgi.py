"""
ASGI config for library_api project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_api.settings')

application = get_asgi_application()


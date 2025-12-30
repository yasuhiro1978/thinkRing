"""
ASGI config for thinkring project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thinkring.settings')

application = get_asgi_application()


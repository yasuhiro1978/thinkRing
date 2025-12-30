"""
WSGI config for thinkring project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thinkring.settings')

application = get_wsgi_application()


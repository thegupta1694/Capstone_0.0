"""
ASGI config for project_allocation project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_allocation.settings')

application = get_asgi_application() 
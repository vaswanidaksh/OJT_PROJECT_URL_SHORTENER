import os
import sys

path = '/home/devanshbaghel18/OJT_PROJECT_URL_SHORTENER'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortner_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

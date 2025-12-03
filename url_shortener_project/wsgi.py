import os
import sys

project_path = '/home/devanshbaghel18/OJT_PROJECT_URL_SHORTENER'
if project_path not in sys.path:
    sys.path.append(project_path)

# Change directory to Django project folder
os.chdir(os.path.join(project_path, 'url_shortener_project'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortener_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

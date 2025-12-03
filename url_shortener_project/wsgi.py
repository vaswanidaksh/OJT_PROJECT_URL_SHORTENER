import os
import sys

# Path to your project
project_home = '/home/ayoo/OJT_PROJECT_URL_SHORTENER'

# Add project path to sys.path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortener_project.settings')

# Activate virtualenv
activate_this = '/home/ayoo/OJT_PROJECT_URL_SHORTENER/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

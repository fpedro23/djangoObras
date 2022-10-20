"""
WSGI config for djangoObrasYProgramas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site

os.environ['PYTHON_EGG_CACHE'] = '/eggCache'


# Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('/home/obrasapf/djangoObras/venv/lib/python2.7/site-packages/')

# Add the app's directory to the PYTHONPATH
#sys.path.append('/home/obrasapf/djangoObras')
#sys.path.append('/home/obrasapf/djangoObras/djangoObrasYProgramas')

# Activate your virtual env
#activate_env = os.path.expanduser("/home/obrasapf/djangoObras/venv/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoObrasYProgramas.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

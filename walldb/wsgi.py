import os
import site
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'walldb.settings'

sys.path.append('/home/walldb/walldb/')

site_packages_path = '/home/walldb/.virtualenvs/walldb/lib/python2.7/site-packages/'
site.addsitedir(os.path.abspath(site_packages_path))

application = get_wsgi_application()

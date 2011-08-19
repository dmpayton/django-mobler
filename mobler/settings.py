import os
from django.conf import settings

BROWSCAP_PATH = getattr(settings, 'BROWSCAP_PATH', None)
if BROWSCAP_PATH is None:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    BROWSCAP_PATH = os.path.join(this_dir, 'browscap.ini')

MOBILE_DOMAIN = getattr(settings, 'MOBILE_DOMAIN', 'http://m.example.com')
MOBLER_CACHE_KEY = getattr(settings, 'MOBLER_CACHE_KEY', 'mobler-cache')
MOBLER_CACHE_TIMEOUT = getattr(settings, 'MOBLER_CACHE_TIMEOUT', 60*60*1)
MOBLER_COOKIE_NAME = getattr(settings, 'MOBLER_COOKIE_NAME', 'mobler-override')
MOBLER_COOKIE_AGE = getattr(settings, 'MOBLER_COOKIE_AGE', 60*60*24*31)
MOBLER_PRESERVE_URL = getattr(settings, 'MOBLER_PRESERVE_URL', True)


import os
from django.conf import settings

MOBLER_DEFAULT_UA_STRINGS = (
    'Android',
    'BlackBerry',
    'IEMobile',
    'Maemo',
    'Opera Mini',
    'SymbianOS',
    'WebOS',
    'Windows Phone',
    'iPhone',
    )
MOBILE_DOMAIN = getattr(settings, 'MOBILE_DOMAIN', 'http://m.example.com')
MOBLER_COOKIE_NAME = getattr(settings, 'MOBLER_COOKIE_NAME', 'mobler-override')
MOBLER_COOKIE_AGE = getattr(settings, 'MOBLER_COOKIE_AGE', 60*60*24*31)
MOBLER_PRESERVE_URL = getattr(settings, 'MOBLER_PRESERVE_URL', True)
MOBLER_UA_STRINGS = getattr(settings, 'MOBLER_UA_STRINGS', MOBLER_DEFAULT_UA_STRINGS)

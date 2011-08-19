import urllib
from django import template
from mobler import settings as mobler_settings

register = template.Library()
COOKIE_NAME = mobler_settings.MOBLER_COOKIE_NAME

@register.simple_tag
def full_site_override(request):
    path = request.path
    params = request.GET.copy()
    params.setdefault(COOKIE_NAME, '1')
    return '%s?%s' % (path, urllib.urlencode(params))

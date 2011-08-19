from django.shortcuts import redirect
from mobler import settings as mobler_settings
from mobler.browscap import browser
import time
import urlparse
import urllib

COOKIE_AGE = mobler_settings.MOBLER_COOKIE_AGE
COOKIE_NAME = mobler_settings.MOBLER_COOKIE_NAME

def build_full_path(request):
    ''' Build a full path+querystring (sans Mobler override) from a request '''
    path = request.path
    if request.GET:
        params = request.GET.copy()
        if COOKIE_NAME in params:
            del params[COOKIE_NAME]
        path += '?%s' % urllib.urlencode(params)
    return path

class MobileDetectionMiddleware(object):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_mobile = browser.detect_mobile(user_agent)
        do_override = (request.COOKIES.get(COOKIE_NAME) == '1')

        ## Check for the override GET param. If we have it, set the cookie and refresh.
        if is_mobile and request.GET.get(COOKIE_NAME):
            response = redirect(build_full_path(request))
            response.set_cookie(COOKIE_NAME, '1', time.time()+COOKIE_AGE)
            return response

        ## If we have a mobile UA but no browser override, redirect
        ## to the mobile site.
        if is_mobile and not do_override:
            mobile_url = mobler_settings.MOBILE_DOMAIN
            if mobler_settings.MOBLER_PRESERVE_URL:
                mobile_url = urlparse.urljoin(mobile_url, build_full_path(request))
            return redirect(mobile_url)

        ## We might be mobile, so set a flag on the request for convenience.
        request.is_mobile = is_mobile

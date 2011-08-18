from django.shortcuts import redirect
from mobler import settings as mobler_settings
from mobler.browscap import browser
import time
import urlparse

COOKIE_AGE = mobler_settings.MOBLER_COOKIE_AGE
COOKIE_NAME = mobler_settings.MOBLER_COOKIE_NAME

class MobileDetectionMiddleware(object):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_mobile = browser.detect_mobile(user_agent)
        do_override = (request.COOKIES.get(COOKIE_NAME) == '1') or request.GET.get(COOKIE_NAME)

        ## If we have a mobile UA but no browser override, redirect
        ## to the mobile site.
        if is_mobile and not do_override:
            mobile_url = mobler_settings.MOBILE_DOMAIN
            if mobler_settings.MOBLER_PRESERVE_URL:
                mobile_url = urlparse.urljoin(mobile_url, request.path)
            return redirect(mobile_url)

        ## We might be mobile, so set a flag on the request for convenience.
        request.is_mobile = is_mobile

    def process_response(self, request, response):
        ## If we have a valid response and the override flag is set, set the cookie
        valid_response = response.status_code == 200
        do_override = request.GET.get(COOKIE_NAME)
        if valid_response and request.is_mobile and do_override:
            response.set_cookie(COOKIE_NAME, '1', time.time()+COOKIE_AGE)
        return response

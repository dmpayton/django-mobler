from django.test import TestCase
from django.test.client import Client
from mobler import settings as mobler_settings
from mobler.browscap import browser
import urlparse

TEST_AGENTS = {
    ## is_mobile: us_list
    True: (
        'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'
        ),
    False: (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; U; ru; rv:5.0.1.6) Gecko/20110501 Firefox/5.0.1 Firefox/5.0.1',
        ),
}

MOBILE_UA = TEST_AGENTS[True][0]
BROWSER_UA = TEST_AGENTS[False][0]
COOKIE_NAME = mobler_settings.MOBLER_COOKIE_NAME

class MoblerTests(TestCase):
    def test_browscap(self):
        ''' Test that browscap is properly parsing user agents '''
        for is_mobile, ua_list in TEST_AGENTS.iteritems():
            for ua_string in ua_list:
                self.assertEqual(is_mobile, browser.detect_mobile(ua_string))

    def test_mobile_redirect(self):
        ''' Test that mobile UA's get redirected and browser UA's don't '''
        response = self.client.get('/', {}, HTTP_USER_AGENT=MOBILE_UA)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/', {}, HTTP_USER_AGENT=BROWSER_UA)
        self.assertNotEqual(response.status_code, 302)

    def test_querystring_override(self):
        ''' Test that mobile UA's with the override GET parameter are not redirected '''
        response = self.client.get('/', {COOKIE_NAME: '1'}, HTTP_USER_AGENT=MOBILE_UA)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies[COOKIE_NAME].value, '1')

    def test_cookie_override(self):
        ''' Test that mobile UA's with the override cookie are not redirected '''
        self.client.cookies[COOKIE_NAME] = '1'
        response = self.client.get('/', {}, HTTP_USER_AGENT=MOBILE_UA)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies[COOKIE_NAME].value, '1')

    def test_url_preserved(self):
        ''' Test that the URL is preserved when redirecting to the mobile site '''
        mobler_settings.MOBLER_PRESERVE_URL = True
        response = self.client.get('/foo/bar/', {}, HTTP_USER_AGENT=MOBILE_UA)
        redirect_url = urlparse.urlparse(response._headers['location'][1])
        self.assertEqual(redirect_url.path, '/foo/bar/')

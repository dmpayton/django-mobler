from django.test import TestCase
from django.test.client import Client
from mobler import settings as mobler_settings
from mobler.browscap import browser
import urlparse

TEST_AGENTS = {
    ## is_mobile: ua_list
    True: (
        'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3',
        'Mozilla/5.0 (BlackBerry; U; BlackBerry AAAA; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/X.X.X.X Mobile Safari/534.11+'

        ## List from django-browscap
        'Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.13337/504; U; cs) Presto/2.2.0',
        'BlackBerry9000/4.6.0.126 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/170',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; cs-cz) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
        'Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95/31.0.017; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
        'Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413',
        ),
    False: (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; U; ru; rv:5.0.1.6) Gecko/20110501 Firefox/5.0.1 Firefox/5.0.1',

        ## List from django-browscap
        'Windows-RSS-Platform/2.0 (MSIE 8.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; GTB6; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.19) Gecko/20081202 Iceweasel/2.0.0.19 (Debian-2.0.0.19-0etch1)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.11) Gecko/2009060215 (CK-Stahuj.cz) Firefox/3.0.11 (.NET CLR 2.0.50727)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; cs-cz) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/(null) Safari/525.27.1',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; cs; rv:1.9.0.11) Gecko/2009060214 Firefox/3.0.11',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.4.4',
        'Opera/9.64 (Windows NT 5.1; U; cs) Presto/2.1.1',
        'Opera/9.52 (X11; Linux i686; U; en)',
        'Wget/1.10.2',
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
                try:
                    self.assertEqual(is_mobile, browser.detect_mobile(ua_string))
                except AssertionError:
                    print is_mobile, ua_string

    def test_internal_cache(self):
        ''' Test that user-agents are properly stored in the internal cache. '''
        for is_mobile, ua_list in TEST_AGENTS.iteritems():
            for ua_string in ua_list:
                browser.detect_mobile(ua_string)
                self.assertEqual(is_mobile, browser._cache[ua_string])

    def test_mobile_redirect(self):
        ''' Test that mobile UA's get redirected and browser UA's don't '''
        ## Mobile UA's should be redirected
        response = self.client.get('/', {}, HTTP_USER_AGENT=MOBILE_UA)
        self.assertEqual(response.status_code, 302)

        ## Browser UA's should *not* be redirected
        response = self.client.get('/', {}, HTTP_USER_AGENT=BROWSER_UA)
        self.assertNotEqual(response.status_code, 302)

    def test_override(self):
        ''' Test that mobile UA's with the override GET parameter are not redirected '''
        ## Test that setting the override param results in a redirect
        response = self.client.get('/', {COOKIE_NAME: '1'}, HTTP_USER_AGENT=MOBILE_UA)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies[COOKIE_NAME].value, '1')

        ## With the cookie set, make sure future requests are not redirected.
        response = self.client.get('/', {}, HTTP_USER_AGENT=MOBILE_UA)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies[COOKIE_NAME].value, '1')

    def test_url_preserved(self):
        ''' Test that the URL is preserved when redirecting to the mobile site '''
        mobler_settings.MOBLER_PRESERVE_URL = True
        response = self.client.get('/foo/bar/?fizz=buzz', {}, HTTP_USER_AGENT=MOBILE_UA)
        redirect_url = urlparse.urlparse(response._headers['location'][1])
        self.assertEqual(redirect_url.path, '/foo/bar/')
        self.assertEqual(redirect_url.query, 'fizz=buzz')

import os
import re
from ConfigParser import SafeConfigParser
from django.core.cache import cache
from mobler import settings as mobler_settings

CACHE_KEY = mobler_settings.MOBLER_CACHE_KEY
CACHE_TIMEOUT = mobler_settings.MOBLER_CACHE_TIMEOUT

class BrowscapParser(object):
    def __init__(self):
        self.mobile_browsers = cache.get(CACHE_KEY, [])
        self._cache = {}
        if not self.mobile_browsers:
            config = SafeConfigParser()
            config.read(mobler_settings.BROWSCAP_PATH)

            browsers = {}
            parents = set()

            for name in config.sections():
                data = dict(config.items(name))
                parent = data.get('parent')
                if parent:
                    parents.add(parent)
                browsers[name] = data

            for name, data in browsers.iteritems():
                if name in parents:
                    continue

                parent = data.get('parent')
                if parent:
                    data.update(browsers[parent])

                if data.get('ismobiledevice') == 'true':
                    name = re.escape(name)
                    name = name.replace("\\?", ".").replace("\\*", ".*?")
                    name = "^%s$" % name
                    self.mobile_browsers.append(name)
            self.mobile_browsers = map(re.compile, self.mobile_browsers)
            cache.set(CACHE_KEY, self.mobile_browsers, CACHE_TIMEOUT)

    def detect_mobile(self, user_agent):
        ''' Detect whether a given User-Agent is a mobile device. '''
        ## If we've cached this UA, return that value
        try:
            return self._cache[user_agent]
        except KeyError:
            ## No match, we'll have to look it up.
            pass

        ## Iterate through our list of regexps to determin if this UA is mobile
        for ua in self.mobile_browsers:
            if ua.match(user_agent):
                ## We have a match!
                self._cache[user_agent] = True
                break
        else:
            ## No match found
            self._cache[user_agent] = False

        return self._cache[user_agent]

browser = BrowscapParser()

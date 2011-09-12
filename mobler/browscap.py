import os
from mobler import settings as mobler_settings

UA_STRINGS = mobler_settings.MOBLER_UA_STRINGS

class BrowscapParser(object):
    def __init__(self):
        self._cache = {}

    def detect_mobile(self, user_agent):
        try:
            return self._cache[user_agent]
        except KeyError:
            for lookup in UA_STRINGS:
                if lookup in user_agent:
                    self._cache[user_agent] = True
                    break
            else:
                self._cache[user_agent] = False
        return self._cache[user_agent]

browser = BrowscapParser()

from .main import *
import sys


__all__ = ["create_database","add_user","validate_user","edit_user_pro_status","delete_user","return_pro_status"]

class GhostBase:
    def __init__(self):
        self._url = None
        self.apikey = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def __getattr__(self, name):
        if name == 'url':
            raise AttributeError(f"'GhostBase' object has no attribute '{name}'. You need to set the URL explicitly.")
        raise AttributeError(f"module 'ghostbase' has no attribute '{name}'")

sys.modules[__name__] = GhostBase()

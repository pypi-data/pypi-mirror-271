from .main import *

__all__ = ["create_database", "add_user", "validate_user", "edit_user_pro_status", "delete_user", "return_pro_status"]

class GhostBase:
    def __init__(self):
        self._url = None
        self._apikey = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def apikey(self):
        return self._apikey

    @apikey.setter
    def apikey(self, value):
        self._apikey = value

    def __getattr__(self, name):
        if name == 'url' or name == 'apikey':
            raise AttributeError(f"'GhostBase' object has no attribute '{name}'. You need to set the URL and API key explicitly.")
        raise AttributeError(f"module 'ghostbase' has no attribute '{name}'")

# Instantiate GhostBase as a singleton
ghostbase = GhostBase()

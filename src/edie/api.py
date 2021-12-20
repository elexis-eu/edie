import requests
from urllib.parse import urlencode

class ApiClient(object):
    """A client for the ELEXIS API"""

    def __init__(self, endpoint):
        if not endpoint.endswith("/"):
            self.endpoint = endpoint + "/"
        else:
            self.endpoint = endpoint


    def dictionaries(self):
        return requests.get(self.endpoint + "dictionaries").json()

    
    def about(self, dictionary_id):
        return requests.get(self.endpoint + "about/" + dictionary_id).json()


    def list(self, dictionary_id, limit=None, offset=None):
        q = {}
        if limit:
            q["limit"] = limit
        if offset:
            q["offset"] = offset
        qstr = urlencode(q)
        if qstr:
            url = f"{self.endpoint}list/{dictionary_id}?{qstr}"
        else:
            url = f"{self.endpoint}list/{dictionary_id}"
        return requests.get(url).json()

    def json(self, dictionary_id, entry_id):
        headers = {'Accept': 'application/json'} 
        r = requests.get(f"{self.endpoint}json/{dictionary_id}/{entry_id}",
                headers=headers)
        return r.json()

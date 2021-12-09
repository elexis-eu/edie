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

    
    def about(self, dictionary):
        return requests.get(self.endpoint + "about/" + dictionary).json()


    def list(self, dictionary, limit=None, offset=None):
        q = {}
        if limit:
            q["limit"] = limit
        if offset:
            q["offset"] = offset
        qstr = urlencode(q)
        if qstr:
            url = f"{self.endpoint}list/{dictionary}?{qstr}"
        else:
            url = f"{self.endpoint}list/{dictionary}"
        return requests.get(url).json()

    def json(self, dictionary, id):
        headers = {'Accept': 'application/json'} 
        r = requests.get(f"{self.endpoint}json/{dictionary}/{id}",
                headers=headers)
        return r.json()

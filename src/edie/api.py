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

class LexonomyApiClient(object):
    def __init__(self, endpoint, username, password):
        if not endpoint.endswith("/"):
            self.endpoint = endpoint + "/"
        else:
            self.endpoint = endpoint
        self.data = {'email':username, 'apikey':password}


    def list_dictionaries(self):
        return requests.post(self.endpoint + "listDict", json=self.data).json()

    def list_dictionaries_lang(self, lang):
        data = self.data
        data['lang']=lang
        return requests.post(self.endpoint + "listDict", json=self.data).json()

lexonomyApi = LexonomyApiClient("https://lexonomy.elex.is/api/", 'rambousek+elexis@gmail.com','GXCQJ6S2FZUATM5Z2S0MGZ7XOMXKUFNP')
print(lexonomyApi.list_dictionaries_lang('sl'))
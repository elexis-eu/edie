import requests
from urllib.parse import urlencode

class ApiClient(object):
    """A client for the ELEXIS API"""

    def __init__(self, endpoint, api_key):
        if not endpoint.endswith("/"):
            self.endpoint = endpoint + "/"
        else:
            self.endpoint = endpoint
        self.api_key = api_key

    def __get_header(self):
        if self.api_key:
            return {"X-API-KEY": self.api_key}
        else:
            return {}

    def dictionaries(self):
        headers = self.__get_header()
        return requests.get(self.endpoint + "dictionaries",
                headers=headers).json()

    
    def about(self, dictionary):
        headers = self.__get_header()
        return requests.get(self.endpoint + "about/" + dictionary,
                headers=headers).json()


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
        headers = self.__get_header()
        return requests.get(url, headers=headers).json()

    def json(self, dictionary, id):
        headers = self.__get_header()
        headers['Accept'] = 'application/json'
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
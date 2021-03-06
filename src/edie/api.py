import requests
import sys
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

    def about(self, dictionary_id):
        headers = self.__get_header()
        response = requests.get(self.endpoint + "about/" + dictionary_id,
                                headers=headers)
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

    def list(self, dictionary_id: str, limit: int = None, offset: int = None):
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

        headers = self.__get_header()

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            response.raise_for_status()
        return response.json()

    def json(self, dictionary_id, entry_id):
        headers = self.__get_header()
        headers['Accept'] = 'application/json'
        r = requests.get(f"{self.endpoint}json/{dictionary_id}/{entry_id}",
                         headers=headers)
        return r.json()

    def tei(self, dictionary_id, entry_id):
        headers = self.__get_header()
        headers['Accept'] = "text/xml"
        r = requests.get(f"{self.endpoint}json/{dictionary_id}/{entry_id}",
                         headers=headers)
        return r.content

    def ontolex(self, dictionary_id, entry_id):
        headers = self.__get_header()
        headers['Accept'] = "text/turtle"
        r = requests.get(f"{self.endpoint}ontolex/{dictionary_id}/{entry_id}",
                         headers=headers)
        return r.content


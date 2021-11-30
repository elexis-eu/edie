import requests

def all_dict_metadata():
    url = "https://lexonomy.elex.is/api/listDict"
    myobj = {
        "email": "rambousek@gmail.com",
        "apikey": "8VBOZ1COTZT5YPGL05GKTZKV006RXJ54"
    }
    x = requests.post(url, data=myobj)
    print(x.text)

def dict_metadata(lang):
    url = "https://lexonomy.elex.is/api/listDict"
    myobj = {
        "email": "rambousek@gmail.com",
        "apikey": "8VBOZ1COTZT5YPGL05GKTZKV006RXJ54",
        "lang": lang
    }
    x = requests.post(url, data=myobj)
    print(x.text)

dict_metadata("sl")
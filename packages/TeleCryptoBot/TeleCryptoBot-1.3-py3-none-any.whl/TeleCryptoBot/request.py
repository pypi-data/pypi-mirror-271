import requests
import json

# default url api
default_url = "https://pay.crypt.bot/api/"
testnet_url = "https://testnet-pay.crypt.bot/api/"
class RequestBody:
    def req(self, key, method, data=None):
        headers = { 'Crypto-Pay-API-Token':key}
        requrl = default_url + method
        result = requests.get(requrl, headers=headers, params=data)
        result_json = json.loads(result.text)
        if(result_json['ok'] == False):
            return str(result_json['error']['code']) +" "+ result_json['error']['name']
        else:
            return result_json
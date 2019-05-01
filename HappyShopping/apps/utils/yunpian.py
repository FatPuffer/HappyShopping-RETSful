import requests
import json


class YunPian():

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"
        
    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【乐购商城】您的验证码是#code#。如非本人操作，请忽略本短信"
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict
 #       print(re_dict)

 #if __name__ == "__main__":
 #    yun_pian = YunPian("68257cf662560d39fad0c553c7902e1e")
 #    yun_pian.send_sms('1111', '18829711180')
    





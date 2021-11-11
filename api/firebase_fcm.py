import requests
import json


class CustomFirebaseFcm:
    def __init__(self):
        self.key = 'YOUR-KEY'
        self.url = 'https://fcm.googleapis.com/fcm/send?'

    def sendFcm(self, title, body, imageUrl, data, token):
        objHeaders = {
            'Content-Type': 'application/json',
            'Authorization': self.key
        }
        objMessage = {
            'to': token,
            'notification': {
                'title': title,
                'body': body,
                'image': imageUrl
            },
            'android': {
                'priority': 'high'
            },
            'data': data
        }
        req = requests.post(self.url, data=json.dumps(
            objMessage), headers=objHeaders)

        return req.text

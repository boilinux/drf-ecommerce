import vonage


class VonageApi:
    def __init__(self):
        self.key = 'KEY'
        self.secret = 'SECRET'
        self.title = 'marketplace'

    def sendMessage(self, phoneNumber, message):
        client = vonage.Client(key=self.key, secret=self.secret)
        sms = vonage.Sms(client)

        responseData = sms.send_message(
            {
                "from": self.title,
                "to": "63" + phoneNumber[1:],
                "text": message,
            }
        )

        isSend = ''
        if responseData["messages"][0]["status"] == "0":
            isSend = "Message sent successfully."
        else:
            isSend = f"Message failed with error: {responseData['messages'][0]['error-text']}"

        return isSend

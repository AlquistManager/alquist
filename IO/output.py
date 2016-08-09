import json
import requests
import sys

# Handles sending messages to webhook
class Output:
    # Webhook's URL taken from program argument
    webhookUrl = str(sys.argv[2])

    # Sends output to webhook
    @classmethod
    def response(cls, text, user_id):
        payload = {'text': text, 'user_id': user_id}
        headers = {'content-type': 'application/json'}
        requests.post(cls.webhookUrl, data=json.dumps(payload), headers=headers)

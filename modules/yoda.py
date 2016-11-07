#!/usr/bin/env python3
import requests
import time
url = "http://cloud.ailao.eu:4576/q"

def process_question(text):
    yoda_qid = requests.post(url, data={'text': text}).json()['id']
    while True:
        time.sleep(0.5)
        data = requests.get(url + '/' + yoda_qid).json()
        if data["finished"]:
            break
    return data['answers'][0]['text']

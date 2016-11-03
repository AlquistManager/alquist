#!/usr/bin/env python3
import requests
url = "http://cloud.ailao.eu:4578/q"

def process_question(text):
    yoda_qid = requests.post(URL, data={'text': text}).json()['id']
    while True:
        time.sleep(0.5)
        data = requests.get(URL + '/' + yoda_qid).json()
        if data["finished"]:
            break
    return data['answers'][0]['text']

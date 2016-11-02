#!/usr/bin/env python3
from states.state import State
from bs4 import BeautifulSoup
import requests


class get_explosm(State):
    def get_latest(self):
        url = "http://explosm.net/comics/latest"
        r = requests.get(url)
        parsed_page = BeautifulSoup(r.content, "html.parser")
        comic_block = parsed_page.find("div", {"id": "comic-container"})
        image_tag = comic_block.find("img")
        image_url = image_tag['src']
        return image_url

    def execute(self, request_data) -> dict:
        # test if there are some answers from previous states already
        old_response = request_data.get('response', False)
        image_url = self.get_latest()
        tag = "<img src={}>".format(image_url)
        # add response of this state to list of responses
        image = {'type': 'text', 'payload': {'text': tag}, 'delay': self.properties['delay']}
        if old_response:
            old_response.append(image)
        else:
            old_response = [image]
        # make dictionary with responses and name of next state of dialogue
        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False) })
        return request_data


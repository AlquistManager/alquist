#!/usr/bin/env python3
from states.state import State
from bs4 import BeautifulSoup
import requests


class get_explosm(State):
    def get_other(self, url_ending, next_prev):
        url = "http://explosm.net"+url_ending
        r = requests.get(url)
        parsed_page = BeautifulSoup(r.content, "html.parser")
        try:
            previous_url = parsed_page.find("a", {"class":next_prev})["href"]
        except KeyError:
            previous_url = url_ending
        return previous_url

    def get_current(self, url_ending):
        url = "http://explosm.net"+url_ending
        r = requests.get(url)
        parsed_page = BeautifulSoup(r.content, "html.parser")
        comic_block = parsed_page.find("div", {"id": "comic-container"})
        image_tag = comic_block.find("img")
        image_url = image_tag['src']
        return image_url

    def execute(self, request_data) -> dict:
        # test if there are some answers from previous states already
        context = request_data.get('context')
        old_response = request_data.get('response', False)
        url_ending = context.get('current_comic_exp')
        action = self.properties.get('action')
        if action == "get_previous":
            url_ending = self.get_other(url_ending, "previous-comic")
        elif action == "get_next":
            url_ending = self.get_other(url_ending, "next-comic")
        elif action == "get_random":
            url_ending = "/comics/random"
        image_url = self.get_current(url_ending)
        context.update({"current_comic_exp": url_ending})
        tag = "<img src={}>".format(image_url)
        # add response of this state to list of responses
        image = {'type': 'text', 'payload': {'text': tag}, 'delay': self.properties['delay']}
        if old_response:
            old_response.append(image)
        else:
            old_response = [image]
        # make dictionary with responses and name of next state of dialogue
        request_data.update({'context': context, 'response': old_response, 'next_state': self.transitions.get('next_state', False) })
        return request_data


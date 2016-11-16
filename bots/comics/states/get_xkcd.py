#!/usr/bin/env python3
from states.state import State
from bs4 import BeautifulSoup
import requests


class get_xkcd(State):
    def get_other(self, url_ending, next_prev):
        url = "http://xkcd.com"+url_ending
        r = requests.get(url)
        parsed_page = BeautifulSoup(r.content, "html.parser")
        try:
            previous_url = parsed_page.find("a", {"rel":next_prev})["href"]
        except KeyError:
            previous_url = url_ending
        return previous_url

    def get_current(self, url):
        r = requests.get(url)
        parsed_page = BeautifulSoup(r.content, "html.parser")
        comic_block = parsed_page.find("div", {"id": "comic"})
        image_tag = comic_block.find("img")
        image_url = image_tag['src']
        image_title = image_tag['title']
        return image_url, image_title

    def execute(self, request_data) -> dict:
        context = request_data.get('context')
        old_response = request_data.get('response', False)
        url_ending = context.get('current_comic_xkcd')
        action = self.properties.get('action')
        if action == "get_previous":
            url_ending = self.get_other(url_ending, "prev")
            url = "http://xkcd.com/"+url_ending
        elif action == "get_next":
            url_ending = self.get_other(url_ending, "next")
            url = "http://xkcd.com/"+url_ending
        elif action == "get_random":
            url_ending = ""
            url = "http://c.xkcd.com/random/comic" 
        elif action == "get_current":
            url = "http://xkcd.com/"+url_ending
        image_url, image_title = self.get_current(url)
        context.update({"current_comic_xkcd": url_ending})
        tag = "<img src={}> <br><p style=\"text-align:center;font-size:20px;\">{}</p>".format(image_url, image_title)
        # add response of this state to list of responses
        image = {'type': 'text', 'payload': {'text': tag}, 'delay': self.properties['delay']}
        if old_response:
            old_response.append(image)
        else:
            old_response = [image]
        # make dictionary with responses and name of next state of dialogue
        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False) })
        return request_data


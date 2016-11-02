import urllib.parse

import requests
from states.state import State
import re


class Carousel(State):
    # execute state
    def execute(self, request_data) -> dict:
        # load context
        context = request_data.get('context', {})
        old_response = request_data.get('response', False)

        message = {'type': 'carousel', 'payload': {'parts':[]}}

        if old_response:
            old_response.append(message)
        else:
            old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})

        # load next state
        return request_data

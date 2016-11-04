import urllib.parse as urlparse

import requests
from states.state import State
import re


class Carousel(State):
    # execute state
    def execute(self, request_data) -> dict:
        # load context
        context = request_data.get('context', {})
        iframes = []
        urls = []
        if 'suggested_phones_1' in context:
            iframes.append('<div style="position:absolute; z-index:-1; width:inherit;"><iframe src="' + context.get(
                'suggested_phones_1') + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>')
            parsed = urlparse.urlparse(context.get('suggested_phones_1'))
            urls.append(urlparse.parse_qs(parsed.query)['url'])

        if 'suggested_phones_2' in context:
            iframes.append('<div style="position:absolute; z-index:-1; width:inherit;"><iframe src="' + context.get(
                'suggested_phones_2') + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>')
            parsed = urlparse.urlparse(context.get('suggested_phones_2'))
            urls.append(urlparse.parse_qs(parsed.query)['url'])
        if 'suggested_phones_3' in context:
            iframes.append('<div style="position:absolute; z-index:-1; width:inherit;"><iframe src="' + context.get(
                'suggested_phones_3') + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>')
            parsed = urlparse.urlparse(context.get('suggested_phones_3'))
            urls.append(urlparse.parse_qs(parsed.query)['url'])
        if 'suggested_phones_4' in context:
            iframes.append('<div style="position:absolute; z-index:-1; width:inherit;"><iframe src="' + context.get(
                'suggested_phones_4') + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>')
            parsed = urlparse.urlparse(context.get('suggested_phones_4'))
            urls.append(urlparse.parse_qs(parsed.query)['url'])
        if 'suggested_phones_5' in context:
            iframes.append('<div style="position:absolute; z-index:-1; width:inherit;"><iframe src="' + context.get(
                'suggested_phones_5') + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>')
            parsed = urlparse.urlparse(context.get('suggested_phones_5'))
            urls.append(urlparse.parse_qs(parsed.query)['url'])
        old_response = request_data.get('response', False)

        message = {'type': 'carousel', 'payload': {'parts': iframes, 'urls': urls}}

        if old_response:
            old_response.append(message)
        else:
            old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})

        # load next state
        return request_data

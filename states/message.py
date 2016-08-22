from random import randint

from .state import State


class MessageText(State):
    def execute(self, request_data) -> dict:
        text = State.contextualize(request_data['context'], self.properties['text'])  # Add context
        request_data.update({'response': text, 'next_state': self.transitions.get('next_state', False)})
        return request_data


class MessageRandomText(State):
    def execute(self, request_data) -> dict:
        resp = self.properties['responses']
        i = randint(0, len(resp)-1)
        text = State.contextualize(request_data['context'], resp[i])
        request_data.update({'response': text, 'next_state': self.transitions.get('next_state', False)})
        return request_data

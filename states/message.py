from random import randint
from logger import state_logger
from .state import State


class MessageText(State):
    def execute(self, request_data) -> dict:
        state_logger.debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        text = State.contextualize(request_data['context'], self.properties['text'])  # Add context
        request_data.update({'response': text, 'next_state': self.transitions.get('next_state', False)})

        state_logger.debug('Response: ' + request_data.get('response'), extra={'uid': request_data.get('session', False)})
        state_logger.debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        state_logger.debug('Next state: ' + request_data.get('next_state'), extra={'uid': request_data.get('session', False)})

        return request_data


class MessageRandomText(State):
    def execute(self, request_data) -> dict:
        state_logger.debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        resp = self.properties['responses']
        i = randint(0, len(resp)-1)
        text = State.contextualize(request_data['context'], resp[i])
        request_data.update({'response': text, 'next_state': self.transitions.get('next_state', False)})

        state_logger.debug('Response: ' + request_data.get('response'), extra={'uid': request_data.get('session', False)})
        state_logger.debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        state_logger.debug('Next state: ' + request_data.get('next_state'), extra={'uid': request_data.get('session', False)})

        return request_data

from random import randint
from logger import state_logger
from .state import State


class MessageText(State):
    def execute(self, request_data) -> dict:
        state_logger.debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        text = State.contextualize(request_data['context'], self.properties['text'])  # Add context
        old_response = request_data.get('response', False)
        message = {'type': 'text', 'payload': {'text': text}, 'delay': self.properties['delay']}
        if old_response:
            old_response.append(message)
        else:
            old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})

        state_logger.debug('Response: ' + text, extra={'uid': request_data.get('session', False)})
        state_logger.debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        state_logger.debug('Next state: ' + str(request_data.get('next_state')), extra={'uid': request_data.get('session', False)})

        return request_data


class MessageRandomText(State):
    def execute(self, request_data) -> dict:
        state_logger.debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        resp = self.properties['responses']
        i = randint(0, len(resp)-1)
        text = State.contextualize(request_data['context'], resp[i])
        old_response = request_data.get('response', False)
        message = {'type': 'text', 'payload': {'text': text}, 'delay': self.properties['delay']}
        if old_response:
            old_response.append(message)
        else:
            old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})

        state_logger.debug('Response: ' + text, extra={'uid': request_data.get('session', False)})
        state_logger.debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        state_logger.debug('Next state: ' + str(request_data.get('next_state')), extra={'uid': request_data.get('session', False)})

        return request_data


class MessageButtons(State):
    def execute(self, request_data) -> dict:
        state_logger.debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})
        old_response = request_data.get('response', False)
        butts = self.properties['buttons']
        for butt in butts:
            butt['label'] = State.contextualize(request_data['context'], butt['label'])
            message = {'type': 'buttons', 'payload': butt, 'delay': self.properties['delay']}
            state_logger.debug('Button: ' + butt, extra={'uid': request_data.get('session', False)})

            if old_response:
                old_response.append(message)
            else:
                old_response = [message]
        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})
        state_logger.debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        state_logger.debug('Next state: ' + str(request_data.get('next_state')), extra={'uid': request_data.get('session', False)})
        return request_data

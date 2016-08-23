from logger import state_logger
from nlp import *
from .state import State


class InputUser(State):
    def execute(self, request_data) -> dict:
        state_logger.debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})
        state_logger.debug('User message: ' + request_data['text'], extra={'uid': request_data.get('session', False)})

        response = get_entities(request_data['text'])
        state_logger.debug('NLP output: ' + str(response), extra={'uid': request_data.get('session', False)})


        # Log latest user response to context
        if self.properties['log_json']:
            request_data['context'].update({'latest': response})

        # Require entity match check
        if self.properties['require_match']:
            state_logger.debug('Checking required entities: ' + str(self.properties.get('entities', False)), extra={'uid': request_data.get('session', False)})

            if self.check_response(response):
                state_logger.debug('PASS',
                                   extra={'uid': request_data.get('session', False)})
                state_logger.debug('Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
                                   extra={'uid': request_data.get('session', False)})
                self.update_context(request_data['context'], response)
                request_data.update({'next_state': self.transitions.get('match', False)})
                state_logger.debug('State ' + self.name + ' complete.',
                                   extra={'uid': request_data.get('session', False)})
                state_logger.debug('Next state: ' + request_data.get('next_state'),
                                   extra={'uid': request_data.get('session', False)})

                return request_data

            else:
                state_logger.debug('FAIL',
                                   extra={'uid': request_data.get('session', False)})
                request_data.update({'next_state': self.transitions.get('notmatch', False)})
                state_logger.debug('Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
                                   extra={'uid': request_data.get('session', False)})
                self.update_context(request_data['context'], response)
                state_logger.debug('State ' + self.name + ' complete.',
                                   extra={'uid': request_data.get('session', False)})
                state_logger.debug('Next state: ' + request_data.get('next_state'),
                                   extra={'uid': request_data.get('session', False)})

                return request_data
        state_logger.debug(
            'Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
            extra={'uid': request_data.get('session', False)})
        self.update_context(request_data['context'], response)
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        state_logger.debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        state_logger.debug('Next state: ' + request_data.get('next_state'), extra={'uid': request_data.get('session', False)})

        return request_data

    def check_response(self, response):  # Checks if all required entities are present
        for entity in self.properties['entities']:
            if self.properties['entities'][entity]in response:
                pass
            else:
                return False
        return True


class InputContext(State):
    def execute(self, request_data) -> dict:
        state_logger.debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        response = request_data['context']['latest']
        state_logger.debug('Latest user message: ' + str(response), extra={'uid': request_data.get('session', False)})

        state_logger.debug(
            'Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
            extra={'uid': request_data.get('session', False)})
        self.update_context(request_data['context'], response)
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        state_logger.debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        state_logger.debug('Next state: ' + request_data.get('next_state'), extra={'uid': request_data.get('session', False)})

        return request_data


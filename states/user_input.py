from nlp import *
from .state import State


class InputUser(State):
    def execute(self, request_data) -> dict:
        # TODO: Logging
        response = get_entities(request_data['text'])

        # Log latest user response to context
        if self.properties['log_json']:
            request_data['context'].update({'latest': response})

        # Require entity match check
        if self.properties['require_match']:

            if self.check_response(response):
                self.update_context(request_data['context'], response)
                request_data.update({'next_state': self.transitions.get('match', False)})
                return request_data

            else:
                request_data.update({'next_state': self.transitions.get('notmatch', False)})
                return request_data

        request_data.update({'next_state': self.transitions.get('next_state', False)})
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
        response = request_data['context']['latest']
        self.update_context(request_data['context'], response)
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data


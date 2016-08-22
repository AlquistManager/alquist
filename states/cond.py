import re

from .state import State


class ConditionalEquals(State):
    def execute(self, request_data) -> dict:
        val1 = State.contextualize(request_data['context'], self.properties['value1'])
        val2 = State.contextualize(request_data['context'], self.properties['value2'])

        if val1 == val2:
            request_data.update({'next_state': self.transitions.get('equal', False)})
            return request_data
        else:
            request_data.update({'next_state': self.transitions.get('notequal', False)})
            return request_data


class ConditionalExists(State):
    def execute(self, request_data) -> dict:
        m = re.search('(?<={{)(.*?)(?=}})', self.properties['key'])
        if m:
            entity = m.group(1)
            if request_data['context'].get(entity, False):
                request_data.update({'next_state': self.transitions.get('exists', False)})
                return request_data
        request_data.update({'next_state': self.transitions.get('notexists', False)})
        return request_data

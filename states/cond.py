import re

from loggers import loggers
from .state import State


class ConditionalEquals(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        val1 = State.contextualize(request_data['context'], self.properties['value1'])
        val2 = State.contextualize(request_data['context'], self.properties['value2'])
        loggers.get(self.bot).get("state_logger").debug('Comparing values: ' + str(self.properties['value1']) + '\rContext: ' + str(request_data.get('context', False)), extra={'uid': request_data.get('session', False)})

        if val1 == val2:
            loggers.get(self.bot).get("state_logger").debug('PASS',
                               extra={'uid': request_data.get('session', False)})
            request_data.update({'next_state': self.transitions.get('equal', False)})
            loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                               extra={'uid': request_data.get('session', False)})
            loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                               extra={'uid': request_data.get('session', False)})
            return request_data
        else:
            loggers.get(self.bot).get("state_logger").debug('FAIL',
                               extra={'uid': request_data.get('session', False)})
            request_data.update({'next_state': self.transitions.get('notequal', False)})
            loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                               extra={'uid': request_data.get('session', False)})
            loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                               extra={'uid': request_data.get('session', False)})
            return request_data


class ConditionalExists(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        m = re.search('(?<={{)(.*?)(?=}})', self.properties['key'])
        if m:
            entity = m.group(1)
            loggers.get(self.bot).get("state_logger").debug('Checking key' + entity + '\rContext: ' + str(request_data.get('context', False)),
                               extra={'uid': request_data.get('session', False)})

            if request_data['context'].get(entity, False):
                request_data.update({'next_state': self.transitions.get('exists', False)})
                loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                   extra={'uid': request_data.get('session', False)})
                loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                   extra={'uid': request_data.get('session', False)})
                return request_data
        request_data.update({'next_state': self.transitions.get('notexists', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                           extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                           extra={'uid': request_data.get('session', False)})
        return request_data

from loggers import loggers

from states.state import State


class InputSpecial(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')), extra={'uid': request_data.get('session', False)})

        return request_data
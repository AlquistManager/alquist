from states.state import State
import random


class PrintData(State):
    # execute state
    def execute(self, request_data) -> dict:
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        print(request_data)
        return request_data

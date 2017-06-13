from states.state import State

class Counter(State):
    # execute state
    def execute(self, request_data) -> dict:

        if 'counter' not in request_data['context']:
            request_data['context']['counter'] = 1
        else:
            request_data['context']['counter'] = int(request_data['context']['counter']) + 1

        if int(request_data['context']['counter'] > request_data['context']['maxcount']):
            request_data['context']['counter'] = 1

        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data

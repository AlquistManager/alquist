from states.state import State

class UpdateScore(State):
    # execute state
    def execute(self, request_data) -> dict:

        print(request_data)

        '''
        if 'right' not in request_data['context']:
            request_data['context']['right'] = 0
        else:
            request_data['context']['right'] = int(request_data['context']['right']) + 1

        if int(request_data['context']['right'] > request_data['context']['maxcount']):
            request_data['context']['counter'] = 1

        '''

        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data

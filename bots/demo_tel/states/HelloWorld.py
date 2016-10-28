from states.state import State


class HelloWorld(State):
    # execute state
    def execute(self, request_data) -> dict:
        # test if there are some answers from previous states already
        old_response = request_data.get('response', False)
        # add response of this state to list of responses
        if old_response:
            old_response.append("Hello world2")
        else:
            old_response = ["Hello world2"]
        # make dictionary with responses and name of next state of dialogue
        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})
        return request_data

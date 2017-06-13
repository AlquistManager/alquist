from states.state import State
import random


class GenerateNumbers(State):
    # execute state
    def execute(self, request_data) -> dict:
        number1 = random.randint(0,100)

        if request_data['context']['operation'] == '-':
            number2 = random.randint(0,number1)
        else:
            number2 = random.randint(0,100)

        request_data['context'].update({'number1': str(number1), 'number2': str(number2)})
        if request_data['context']['operation'] == '+':
            request_data['context'].update({'result': str(number1 + number2)})
        else:
            request_data['context'].update({'result': str(number1 - number2)})

        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data

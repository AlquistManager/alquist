from random import randint
from loggers import loggers
from .state import State


class MessageText(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self),
                                                        extra={'uid': request_data.get('session', False)})

        text = State.contextualize(request_data['context'], self.properties['text'])  # Add context
        old_response = request_data.get('response', False)
        message = {'type': 'text', 'payload': {'text': text}, 'delay': self.properties['delay']}
        if old_response:
            old_response.append(message)
        else:
            old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})

        loggers.get(self.bot).get("state_logger").debug('Response: ' + text,
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                                        extra={'uid': request_data.get('session', False)})

        return request_data


class MessageRandomText(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self),
                                                        extra={'uid': request_data.get('session', False)})

        resp = self.properties['responses']
        i = randint(0, len(resp) - 1)
        text = State.contextualize(request_data['context'], resp[i])
        old_response = request_data.get('response', False)
        message = {'type': 'text', 'payload': {'text': text}, 'delay': self.properties['delay']}
        if old_response:
            old_response.append(message)
        else:
            old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})

        loggers.get(self.bot).get("state_logger").debug('Response: ' + text,
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                                        extra={'uid': request_data.get('session', False)})

        return request_data


class MessageButtons(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self),
                                                        extra={'uid': request_data.get('session', False)})
        old_response = request_data.get('response', False)
        butts = self.properties['buttons']
        for butt in butts:
            new_butt = butt.copy()
            new_butt['label'] = State.contextualize(request_data['context'], new_butt['label'])
            message = {'type': 'button', 'payload': new_butt, 'delay': self.properties['delay']}
            loggers.get(self.bot).get("state_logger").debug('Button: ' + str(new_butt),
                                                            extra={'uid': request_data.get('session', False)})

            if old_response:
                old_response.append(message)
            else:
                old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                                        extra={'uid': request_data.get('session', False)})
        return request_data


class MessageCheckboxes(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self),
                                                        extra={'uid': request_data.get('session', False)})
        old_response = request_data.get('response', False)
        checkboxes = self.properties['checkboxes']
        for checkbox in checkboxes:
            new_checkbox = checkbox.copy()
            new_checkbox['label'] = State.contextualize(request_data['context'], new_checkbox['label'])
            message = {'type': 'checkbox', 'payload': new_checkbox, 'delay': self.properties['delay']}
            loggers.get(self.bot).get("state_logger").debug('Checkbox: ' + str(new_checkbox),
                                                            extra={'uid': request_data.get('session', False)})

            if old_response:
                old_response.append(message)
            else:
                old_response = [message]
        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                                        extra={'uid': request_data.get('session', False)})
        return request_data


class MessageIframe(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self),
                                                        extra={'uid': request_data.get('session', False)})
        old_response = request_data.get('response', False)
        url = State.contextualize(request_data['context'], self.properties['url'])
        width = State.contextualize(request_data['context'], self.properties['width'])
        height = State.contextualize(request_data['context'], self.properties['height'])
        scrolling = State.contextualize(request_data['context'], self.properties['scrolling'])
        align = State.contextualize(request_data['context'], self.properties['align'])
        message = {'type': 'iframe',
                   'payload': {'url': url, 'width': width, 'height': height, 'scrolling': scrolling, 'align': align},
                   'delay': self.properties['delay']}
        loggers.get(self.bot).get("state_logger").debug('Iframe: ' + str(url),
                                                        extra={'uid': request_data.get('session', False)})
        if old_response:
            old_response.append(message)
        else:
            old_response = [message]
        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                                        extra={'uid': request_data.get('session', False)})
        return request_data


class MessageSlider(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self),
                                                        extra={'uid': request_data.get('session', False)})
        old_response = request_data.get('response', False)

        entities = State.contextualize(request_data['context'], self.properties['entities'])
        max_value = State.contextualize(request_data['context'], self.properties['max_value'])
        min_value = State.contextualize(request_data['context'], self.properties['min_value'])
        default_values = State.contextualize(request_data['context'], self.properties['default_values'])
        connect = State.contextualize(request_data['context'], self.properties['connect'])
        step = State.contextualize(request_data['context'], self.properties['step'])
        tooltips = State.contextualize(request_data['context'], self.properties['tooltips'])
        tooltips_decimals = State.contextualize(request_data['context'], self.properties['tooltips_decimals'])
        tooltips_prefix = State.contextualize(request_data['context'], self.properties['tooltips_prefix'])
        tooltips_postfix = State.contextualize(request_data['context'], self.properties['tooltips_postfix'])

        message = {'type': 'slider',
                   'payload': {'entities': entities, 'max_value': max_value, 'min_value': min_value,
                               'default_values': default_values,
                               'step': step, 'connect': connect, 'tooltips': tooltips,
                               'tooltips_decimals': tooltips_decimals,
                               'tooltips_prefix': tooltips_prefix,
                               'tooltips_postfix': tooltips_postfix},
                   'delay': self.properties['delay']}

        loggers.get(self.bot).get("state_logger").debug('Slider', extra={'uid': request_data.get('session', False)})
        if old_response:
            old_response.append(message)
        else:
            old_response = [message]
        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                                        extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                                        extra={'uid': request_data.get('session', False)})
        return request_data

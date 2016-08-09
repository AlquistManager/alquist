from abc import ABC, abstractmethod
from random import randint
import re

from demo_npl import NPL

# State is an abstract class, from which all other state type classes inherit.
#
# TODO: Decide where to handle logging: here or in the IO?


class State(ABC):
    def __init__(self, name, properties, transitions):
        self.name = name
        self.properties = properties
        self.transitions = transitions

    @abstractmethod
    def execute(self, parent_session) -> str:
        pass

    @staticmethod
    def contextualize(context, text):
        pattern_clean = re.compile('(?<=\'{{)(.*?)(?=}}\')')
        for entity in re.findall(pattern_clean, text):
            text = text.replace('\'{{' + entity + '}}\'', context[entity])
        return text



class MessageText(State):
    def execute(self, parent_session) -> str:
        parent_session.session_io.send(self.properties['text'])
        return self.transitions.get('next_state', False)


# in the parser, MessageRandomText is handled so that the random responses are an array,
# that corresponds with the responses key
class MessageRandomText(State):
    def execute(self, parent_session) -> str:
        resp = self.properties['responses']
        i = randint(0, len(resp))
        parent_session.session_io.send(resp[i])
        return self.transitions.get('next_state', False)


class InputUser(State):
    def execute(self, parent_session) -> str:
        parent_session.session_io.send(self.properties['text'])
        raw_response = parent_session.session_io.recieve()
        # TODO: NLP
        response = NPL.get_entities(raw_response)
        # require entity match check
        if self.properties['require_match']:
            bad_response = True
            while bad_response:
                if self.check_response(response):
                    bad_response = False
                else:
                    parent_session.session_io.send(self.properties['error_text'])
                    response = parent_session.session_io.recieve()
        if self.properties['log_json']:
            parent_session.context.update({'latest': response})
        self.update_context(parent_session.context, response)
        return self.transitions.get('next_state', False)

    def check_response(self, response):
        for entity in self.properties['entities']:
            if entity in response:
                pass
            else:
                return False
        return True

    def update_context(self, context: dict, response: dict):
        for entity in response:
            if entity in self.properties['entities']:
                context.update({entity: response[entity]})

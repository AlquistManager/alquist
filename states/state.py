import re
from abc import ABC, abstractmethod


# State is an abstract class, from which all other state type classes inherit.
#


class State(ABC):
    def __init__(self, name, properties, transitions):
        self.name = name
        self.properties = properties
        self.transitions = transitions

    @abstractmethod
    def execute(self, request_data) -> dict:
        pass

    @staticmethod
    def contextualize(context, text):  # Replaces variable strings with context values

        pattern_clean = re.compile('(?<={{)(.*?)(?=}})')
        for entity in re.findall(pattern_clean, str(text)):
            text = text.replace('{{' + entity + '}}', context[entity])
        return text

    def update_context(self, context: dict, response: dict):
        for entity in self.properties['entities']:
            if self.properties['entities'][entity] in response:
                context.update({entity: response[self.properties['entities'][entity]]})

    def __str__(self):
        return 'Name: ' + self.name + '\rProperties: ' + str(self.properties) + '\rTransitions: ' + str(
            self.transitions)

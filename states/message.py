from random import randint

from . import State


class MessageText(State):
    def execute(self, parent_session) -> str:
        text = State.contextualize(parent_session.context, self.properties['text'])  # Add context
        parent_session.session_io.send(text)  # Send message
        parent_session.logger.debug('Robot says: ' + text)
        return self.transitions.get('next_state', False)


class MessageRandomText(State):
    def execute(self, parent_session) -> str:
        resp = self.properties['responses']
        i = randint(0, len(resp))
        text = State.contextualize(parent_session.context, resp[i])
        parent_session.session_io.send(text)
        parent_session.logger.debug('Robot says: ' + text)
        return self.transitions.get('next_state', False)

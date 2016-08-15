import re

from .state import State


class ConditionalEquals(State):
    def execute(self, parent_session) -> str:
        val1 = State.contextualize(parent_session.context, self.properties['value1'])
        val2 = State.contextualize(parent_session.context, self.properties['value2'])
        parent_session.logger.debug('Comparing ' + str(val1) + ' and ' + str(val2))

        if val1 == val2:
            parent_session.logger.debug('Values are equal')
            return self.transitions.get('equal', False)
        else:
            parent_session.logger.debug('Values are NOT equal')
            return self.transitions.get('notequal', False)


class ConditionalExists(State):
    def execute(self, parent_session) -> str:
        m = re.search('(?<={{)(.*?)(?=}})', self.properties['key'])
        if m:
            entity = m.group(1)
            parent_session.logger.debug('Checking, if ' + str(entity) + ' exists')
            if parent_session.context.get(entity, False):
                parent_session.logger.debug('Context entity ' + entity + ' found')
                return self.transitions.get('exists', False)
        parent_session.logger.debug('Context entity NOT found')
        return self.transitions.get('notexists', False)

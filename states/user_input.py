from demo_npl import NPL
from .state import State


class InputUser(State):
    def execute(self, parent_session) -> str:
        parent_session.send(self.properties['text'])
        parent_session.logger.debug('Robot says: ' + self.properties['text'])
        parent_session.logger.info('Robot is waiting for your response ... ')
        raw_response = parent_session.recieve()
        parent_session.logger.debug('Client says: ' + raw_response)

        # TODO: NLP
        response = NPL.get_entities(raw_response)
        # Require entity match check
        if self.properties['require_match']:
            bad_response = True
            parent_session.logger.debug('Checking required entities.')

            while bad_response:
                if self.check_response(response):
                    parent_session.logger.debug('Match successful.')
                    bad_response = False
                else:
                    parent_session.logger.debug('Match unsuccessful.')
                    parent_session.send(self.properties['error_text'])
                    parent_session.logger.debug('Robot says: ' + self.properties['error_text'])
                    response = parent_session.recieve()
                    parent_session.logger.info('Robot is waiting for your response ... ')

        # Log latest user response to context
        if self.properties['log_json']:
            parent_session.context.update({'latest': response})
            parent_session.logger.debug('Adding latest response to context.')

        # Context updates with our entities
        self.update_context(parent_session.context, response)
        return self.transitions.get('next_state', False)

    def check_response(self, response):  # Checks if all required entities are present
        for entity in self.properties['entities']:
            if entity in response:
                pass
            else:
                return False
        return True


class InputContext(State):
    def execute(self, parent_session) -> str:
        response = parent_session.context['latest']
        self.update_context(parent_session.context, response)
        return self.transitions.get('next_state', False)

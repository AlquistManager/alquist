from states.state import State


# This class allows the dialogue to update context independently on user input
#
# example YAML implementation
#
# example:
#   type: ChangeContext
#   properties:
#     del_keys:
#       - one
#       - two
#     update_keys:
#       three: thirteen
#       four: fourteen
#   transitions:
#     next_state: next


class ChangeContext(State):
    # execute state
    def execute(self, request_data) -> dict:
        # load context
        context = request_data.get('context', {})
        # delete keys marked for deletion
        for key in self.properties.get('del_keys', []):
            context.pop(key, False)
        # update keys marked for update
        for key in self.properties.get('update_keys', []):
            context.update({key: State.contextualize(context, self.properties.get('update_keys', [])[key])})
        request_data.update({'context': context})
        # load next state
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data

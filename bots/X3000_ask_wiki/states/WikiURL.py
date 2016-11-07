from states.state import State


class WikiURL(State):
    def execute(self, request_data) -> dict:
        query = request_data['context'].get('query', False)
        url = "https://cs.m.wikipedia.org/w/index.php?search=" + query
        request_data['context'].update({"query_url": url})
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data
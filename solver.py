from loaded_states import state_dict


# TODO: Add session IDs and figure out logging
def process_request(state_name, context, text):
    request_data = {'context': context, 'text': text}
    while True:
        current_state = build_state(state_name)
        request_data = current_state.execute(request_data)
        has_next = request_data.get('next_state', False)
        if has_next:
            next_type = str(state_dict['states'][has_next].get('type', lambda: "nothing"))
            if next_type == "InputUser":
                return request_data
            state_name = has_next

        else:
            request_data.update({'next_state': 'END'})
            return request_data


def build_state(state_name):
    next_st = state_dict['states'][state_name]
    func = next_st.get('type', lambda: "nothing")
    return func(state_name, next_st['properties'], next_st['transitions'])
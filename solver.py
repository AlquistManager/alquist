from loaded_states import state_dict
from logger import main_logger


def process_request(state_name, context, text, session):
    request_data = {'context': context, 'text': text, 'session': session}
    if text != '':
        main_logger.info("USER SAYS: "+request_data['text'], extra={'uid': session})
    while True:
        main_logger.debug("Entering State: "+state_name, extra={'uid': session})
        current_state = build_state(state_name)
        request_data = current_state.execute(request_data)
        has_next = request_data.get('next_state', False)
        if has_next:
            next_type = str(state_dict['states'][has_next].get('type', lambda: "nothing"))
            if next_type == str('<class \'states.user_input.InputUser\'>'):
                if request_data.get('response', '') != '':
                    main_logger.info("BOT SAYS: " + request_data['response'], extra={'uid': session})
                return request_data
            state_name = has_next
        else:
            request_data.update({'next_state': 'END'})
            if request_data.get('response', '') != '':
                main_logger.info("BOT SAYS: " + request_data['response'], extra={'uid': session})
            main_logger.info("===== SESSION END =====", extra={'uid': session})

            return request_data


def build_state(state_name):
    next_st = state_dict['states'][state_name]
    func = next_st.get('type', lambda: "nothing")
    return func(state_name, next_st['properties'], next_st['transitions'])
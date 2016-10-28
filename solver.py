import copy
import dialogue_logger

from loaded_states import state_dict
from logger import main_logger


def process_request(state_name, context, text, session):
    if text == '!undo':
        prev_context = context.get('previous_context', {})
        request_data = {'context': prev_context, 'text': prev_context.get('previous_text', ''), 'session': session,
                        'next_state': context.get('previous_request', 'init')}
        state_name = prev_context.get('previous_request', 'init')
        main_logger.info("UNDO", extra={'uid': session})
        dialogue_logger.log("UNDO", session)
        main_logger.info("GOTO: " + str(state_name), extra={'uid': session})
        dialogue_logger.log("GOTO: " + str(state_name), session)
    elif text == '!reset':
        prev_context = context.get('previous_context', {})
        request_data = {'context': {'prev_context': context.get('previous_context', {})}, 'text': context.get('previous_text', ''), 'session': session,
                        'next_state': 'init'}
        state_name = 'init'
        main_logger.info("RESET", extra={'uid': session})
        dialogue_logger.log("RESET", session)
        main_logger.info("GOTO: " + str(state_name), extra={'uid': session})
        dialogue_logger.log("GOTO: " + str(state_name), session)
    else:
        request_data = {'context': context, 'text': text, 'session': session}
    context.update({'previous_context': copy.deepcopy(context), 'previous_request': state_name, 'previous_text': text})
    if text != '' and text != '!undo':
        main_logger.info("USER SAYS: " + request_data['text'], extra={'uid': session})
        dialogue_logger.log("USER SAYS: " + request_data['text'], session)
    while True:
        main_logger.debug("Entering State: " + state_name, extra={'uid': session})
        current_state = build_state(state_name)
        dialogue_logger.log("Entering State: " + str(current_state), session)
        dialogue_logger.log("Actual context: " + str(context), session)
        request_data = current_state.execute(request_data)
        has_next = request_data.get('next_state', False)
        if has_next:
            next_type = str(state_dict['states'][has_next].get('type', lambda: "nothing"))
            if next_type == str('<class \'states.user_input.InputUser\'>') or next_type == str('<class \'states.user.InputSpecial.InputSpecial\'>'):
                if request_data.get('response', '') != '':
                    main_logger.info("BOT SAYS: " + str(request_data['response']), extra={'uid': session})
                    dialogue_logger.log("BOT SAYS: " + str(request_data['response']), session)
                return request_data
            state_name = has_next
        else:
            request_data.update({'next_state': 'END'})
            if request_data.get('response', '') != '':
                main_logger.info("BOT SAYS: " + str(request_data['response']), extra={'uid': session})
                dialogue_logger.log("BOT SAYS: " + str(request_data['response']), session)
            main_logger.info("===== SESSION END =====", extra={'uid': session})
            dialogue_logger.log("===== SESSION END =====", session)

            return request_data


def build_state(state_name):
    next_st = state_dict['states'][state_name]
    func = next_st.get('type', lambda: "nothing")
    return func(state_name, next_st['properties'], next_st['transitions'])

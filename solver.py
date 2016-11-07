import copy
import dialogue_logger
from modules.yoda import *
from loaded_states import state_dict
from loggers import loggers


def process_request(bot, state_name, context, text, session, payload):
    if text == '!undo':
        prev_context = context.get('previous_context', {})
        request_data = {'context': prev_context, 'text': prev_context.get('previous_text', ''), 'session': session,
                        'next_state': context.get('previous_request', 'init'),
                        'payload': prev_context.get('previous_payload', {})}
        state_name = prev_context.get('previous_request', 'init')
        loggers.get(bot).get("main_logger").info("UNDO", extra={'uid': session})
        dialogue_logger.log("UNDO", session)
        loggers.get(bot).get("main_logger").info("GOTO: " + str(state_name), extra={'uid': session})
        dialogue_logger.log("GOTO: " + str(state_name), session)
    elif text == '!reset':
        prev_context = context.get('previous_context', {})
        request_data = {'context': {'previous_context': context.get('previous_context', {})},
                        'text': context.get('previous_text', ''), 'session': session,
                        'next_state': 'init',
                        'payload': {}}
        state_name = 'init'
        loggers.get(bot).get("main_logger").info("RESET", extra={'uid': session})
        dialogue_logger.log("RESET", session)
        loggers.get(bot).get("main_logger").info("GOTO: " + str(state_name), extra={'uid': session})
        dialogue_logger.log("GOTO: " + str(state_name), session)
    elif "@YodaQA" in text:
        request_data = {'context': context, 'text': context.get('previous_text', ''), 'session': session}
        state_name = context.get('previous_request', 'init')
        text = process_question(text[8:])
        response = [{'type': 'text', 'payload': {'text': text}, 'delay': 0}]
        request_data.update({"response": response, 'next_state': context.get("previous_request", "init")})
    else:
        request_data = {'context': context, 'text': text, 'session': session, 'payload': payload}
    context.update({'previous_context': copy.deepcopy(context), 'previous_request': state_name, 'previous_text': text,
                    'previous_payload': copy.deepcopy(payload)})
    if text != '' and text != '!undo' and text != '!reset':
        loggers.get(bot).get("main_logger").info("USER SAYS: " + request_data['text'], extra={'uid': session})
        dialogue_logger.log("USER SAYS: " + request_data['text'], session)
    while True:
        loggers.get(bot).get("main_logger").debug("Entering State: " + state_name, extra={'uid': session})
        current_state = build_state(bot, state_name)
        dialogue_logger.log("Entering State: " + str(current_state), session)
        dialogue_logger.log("Actual context: " + str(context), session)
        request_data = current_state.execute(request_data)
        has_next = request_data.get('next_state', False)
        if has_next:
            next_type = str(state_dict.get(bot)['states'][has_next].get('type', lambda: "nothing"))
            if next_type == str('<class \'states.user_input.InputUser\'>') or next_type == str(
                    '<class \'states.user_input.InputSpecial\'>'):
                if request_data.get('response', '') != '':
                    loggers.get(bot).get("main_logger").info("BOT SAYS: " + str(request_data['response']),
                                                             extra={'uid': session})
                    dialogue_logger.log("BOT SAYS: " + str(request_data['response']), session)
                if next_type == str('<class \'states.user_input.InputSpecial\'>'):
                    show = str(state_dict.get(bot)['states'][has_next].get('properties').get("show_input", "both"))
                    request_data.update({"input": show})
                else:
                    request_data.update({"input": "both"})
                return request_data
            state_name = has_next
        else:
            request_data.update({'next_state': 'END'})
            if request_data.get('response', '') != '':
                loggers.get(bot).get("main_logger").info("BOT SAYS: " + str(request_data['response']),
                                                         extra={'uid': session})
                dialogue_logger.log("BOT SAYS: " + str(request_data['response']), session)
                loggers.get(bot).get("main_logger").info("===== SESSION END =====", extra={'uid': session})
            dialogue_logger.log("===== SESSION END =====", session)

            request_data.update({"input": "both"})
            return request_data


def build_state(bot, state_name):
    next_st = state_dict.get(bot)['states'][state_name]
    func = next_st.get('type', lambda: "nothing")
    return func(state_name, next_st['properties'], next_st['transitions'], bot)

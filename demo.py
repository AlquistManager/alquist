from states import *

state_dict = {'name': 'main',
              'states': {
                  'init': {'type': InputUser, 'properties': {'text': 'Hello, would you like to know your Horoscope?',
                                                             'require_match': True, 'log_json': False,
                                                             'error_text': 'Sorry, I don\'t understand, would you like to know your Horoscope?',
                                                             'entities': {'yes_no': 'yes_no'}},
                           'transitions': {'next_state': 'yes_no'}},

                  'acc_horo': {'type': InputUser, 'properties': {'text': 'What sign are you?',
                                                             'require_match': True, 'log_json': False,
                                                             'error_text': 'Sorry, I don\'t understand, what sign was that?',
                                                             'entities': {'sign': 'sign'}},
                                                             'transitions': {'next_state': 'give_horo'}},

                  'yes_no': {'type': MessageText, 'properties': {'text': 'Thank you, unfortunately, I don\'t know how to do that yet...'},
                             'transitions': {}}

              }
              }

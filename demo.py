from states import *

state_dict = {'name': 'main',
              'states': {
                  'init': {'type': InputUser, 'properties': {'text': 'Hi, nice to meet you. \nCan I ask you a question?',
                                                             'require_match': True, 'log_json': False,
                                                             'error_text': 'Sorry, I don\'t understand, yes or no?',
                                                             'entities': {'yes_no': 'yes_no'}},
                           'transitions': {'next_state': 'yes_no'}},

                  'ask_color': {'type': InputUser, 'properties': {'text': 'What is your favourite color?',
                                                             'require_match': True, 'log_json': True,
                                                             'error_text': 'I don\'t think that counts as a color... try another one?',
                                                             'entities': {'colour': 'color'}},
                                                             'transitions': {'next_state': 'debug_recent'}},

                  'yes_no': {'type': ConditionalEquals, 'properties': {'value1': '\'{{yes_no}}\'', 'value2': 'yes'},
                             'transitions': {'equal': 'ask_color', 'notequal': 'bye'}},

                  'bye': {'type': MessageRandomText, 'properties': {'responses': ['OK, bye', 'I see, it was nice talking to you anyway', 'Oh, that is a shame, bye then']},
                          'transitions': {}},

                  'debug_recent': {'type': InputContext, 'properties': {'entities': {'colour': 'color'}}, 'transitions': {'next_state': 'has_color'}},

                  'has_color': {'type': ConditionalExists, 'properties': {'key': '\'{{color}}\''},
                                'transitions': {'exists': 'color_echo', 'notexists': 'leave_in_shame'}},

                  'leave_in_shame': {'type': MessageText, 'properties': {'text': 'Well, this is awkward. \nI seem to have forgotten your favourite color. \nI am ... gonna ... go now. Bye'},
                                     'transitions': {}},

                  'color_echo': {'type': MessageText, 'properties': {'text': 'Wow, \'{{color}}\', really? That is super cool.'},
                                 'transitions': {}},



              }
              }

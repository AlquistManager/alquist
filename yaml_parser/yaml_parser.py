import glob
import importlib.util
import os
from collections import OrderedDict

import sys
import yaml
from loaded_states import state_dict, intent_transitions
from yaml_parser.yaml_ordered_dict import OrderedDictYAMLLoader
from states import *
from os import listdir
from os.path import isfile, join


# Parses yaml files containing description of dialogue
class YamlParser:
    modules = {}

    def __init__(self, bot_name=""):
        # clear all content in dictionary with loaded states
        # load only one bot if it is specified, otherwise load all bots
        if bot_name != "":
            self.initialize(bot_name)
        else:
            state_dict.clear()
            for bot_name in self.get_immediate_subdirectories("bots"):
                self.initialize(bot_name)

    def initialize(self, bot_name):
        # folder, where yaml files are stored
        bot_yaml_folder = "bots/" + bot_name + "/flows/"
        bot_states_folder = "bots/" + bot_name + "/states/"
        try:
            self.import_custom_states(bot_states_folder, bot_name)
            # create fields in state_dict and intent_transitions for bot
            state_dict.update({bot_name.lower(): {}})
            intent_transitions.update({bot_name.lower(): {}})
            # find all .yml and .yaml files
            files = [f for f in listdir(bot_yaml_folder)
                     if isfile(join(bot_yaml_folder, f)) if f.endswith(('.yml', '.yaml'))]
            # load all files
            for file_name in files:
                # checks if file size is not 0
                if os.stat(join(bot_yaml_folder, file_name)).st_size == 0:
                    print(file_name)
                    continue
                self.load_file(bot_yaml_folder, file_name, bot_name)
            # check if init state is present
            self.check_init_state(state_dict.get(bot_name.lower()), bot_name)
            # check if all states from intent_transitions exists
            self.check_intent_transitions_states_exist(bot_name)
            # check if all states mentioned in transitions really exist
            self.check_transition_states_exist(bot_name)
        except FileNotFoundError:
            print(
                bot_yaml_folder + " folder doesn't exist. Thus bot " + bot_name + " doesn't have correct folder structure.",
                file=sys.stderr)

    # load yaml file
    def load_file(self, bot_yaml_folder, file_name, bot_name):
        # add missing slash to directory path
        if not (bot_yaml_folder.endswith('/')):
            bot_yaml_folder += '/'
        with open(bot_yaml_folder + file_name, 'r', encoding="utf8") as stream:
            try:
                # load yaml to OrderedDict
                loaded_yaml = yaml.load(stream, OrderedDictYAMLLoader)
                # check unique names of states
                self.check_unique_names(bot_name, loaded_yaml, state_dict)
                # checks if all states has type
                self.check_types(loaded_yaml, bot_name)
                # add missing transitions
                self.modify_transitions(loaded_yaml, bot_yaml_folder)
                # changes representation of node types to intern objects
                self.types_to_intern_representation(loaded_yaml, bot_name)
                # sets default or missing properties
                self.set_default_properties(loaded_yaml, bot_name)
                self.check_delays(loaded_yaml, bot_name)
                if not ('states' in state_dict.get(bot_name.lower())):
                    # update whole dictionary
                    state_dict.get(bot_name.lower()).update(loaded_yaml)
                else:
                    # update only states, to not overwrite everything
                    state_dict.get(bot_name.lower())['states'].update(loaded_yaml['states'])
                # load intent_transitions field
                self.load_intent_transitions(loaded_yaml, bot_name)
            except yaml.YAMLError as exc:
                print(exc)

    # Modifies transitions to intern format
    def modify_transitions(self, loaded_yaml, bot_yaml_folder):
        i = 0
        states = list(loaded_yaml['states'].items())
        # Iterate through all states from loaded yaml
        for state_name, state_parameters in loaded_yaml['states'].items():
            self.add_transitions(state_parameters, states, i)
            self.modify_flow_transitions(state_parameters, bot_yaml_folder)
            self.modify_return_transitions(state_parameters)
            i += 1

    # Add transition to nodes, which has default value
    def add_transitions(self, state_parameters, states, i):
        if not ("transitions" in state_parameters) and not (state_parameters['type'] == 'message_buttons'):
            # If the transitions field is missing, add next state
            if i + 1 < len(states):
                state_parameters['transitions'] = {'next_state': states[i + 1][0]}
            else:
                # Leave it blank, if we are at the end of file
                state_parameters['transitions'] = {'next_state': ''}

    # changes transition from flow to the first state of flow
    def modify_flow_transitions(self, state_parameters, bot_yaml_folder):
        if "transitions" in state_parameters:
            if "flow" in state_parameters["transitions"]:
                flow_name = state_parameters["transitions"]["flow"]
                # find file with some extension and the right name
                with open(glob.glob(bot_yaml_folder + flow_name + '.*')[0], 'r', encoding="utf8") as stream:
                    try:
                        # load yaml to OrderedDict
                        loaded_yaml = yaml.load(stream, OrderedDictYAMLLoader)
                        for state_name, state_parameters_intern in loaded_yaml['states'].items():
                            # change to name of transition from flow to the first state of flow
                            state_parameters["transitions"].clear()
                            state_parameters["transitions"].update({"next_state": state_name})
                            break
                    except yaml.YAMLError as exc:
                        print(exc)

    # change transitions: return to transitions:''
    def modify_return_transitions(self, state_parameters):
        if "transitions" in state_parameters:
            if state_parameters["transitions"] == "return":
                state_parameters["transitions"] = {'next_state': ''}
                return
            if "equal" in state_parameters["transitions"]:
                if state_parameters["transitions"]["equal"] == "return":
                    state_parameters["transitions"]["equal"] = ""
            if "notequal" in state_parameters["transitions"]:
                if state_parameters["transitions"]["notequal"] == "return":
                    state_parameters["transitions"]["notequal"] = ""
            if "match" in state_parameters["transitions"]:
                if state_parameters["transitions"]["match"] == "return":
                    state_parameters["transitions"]["match"] = ""
            if "notmatch" in state_parameters["transitions"]:
                if state_parameters["transitions"]["notmatch"] == "return":
                    state_parameters["transitions"]["notmatch"] = ""
            if "exists" in state_parameters["transitions"]:
                if state_parameters["transitions"]["exists"] == "return":
                    state_parameters["transitions"]["exists"] = ""
            if "notexists" in state_parameters["transitions"]:
                if state_parameters["transitions"]["notexists"] == "return":
                    state_parameters["transitions"]["notexists"] = ""

    # Change string representation of states into inner representation of objects
    def types_to_intern_representation(self, loaded_yaml, bot_name):
        for state_name, state_properties in loaded_yaml['states'].items():
            if state_properties['type'].lower() == 'message_text':
                state_properties['type'] = MessageText
            elif state_properties['type'].lower() == 'message_text_random':
                state_properties['type'] = MessageRandomText
            elif state_properties['type'].lower() == 'input_user':
                state_properties['type'] = InputUser
            elif state_properties['type'].lower() == 'input_context':
                state_properties['type'] = InputContext
            elif state_properties['type'].lower() == 'conditional_equal':
                state_properties['type'] = ConditionalEquals
            elif state_properties['type'].lower() == 'conditional_exists':
                state_properties['type'] = ConditionalExists
            elif state_properties['type'].lower() == 'message_buttons':
                state_properties['type'] = MessageButtons
            elif state_properties['type'].lower() == 'change_context':
                state_properties['type'] = ChangeContext
            elif state_properties['type'].lower() == 'message_iframe':
                state_properties['type'] = MessageIframe
            elif state_properties['type'].lower() == 'message_checkboxes':
                state_properties['type'] = MessageCheckboxes
            elif state_properties['type'].lower() == 'input_special':
                state_properties['type'] = InputSpecial
            elif state_properties['type'].lower() == 'message_slider':
                state_properties['type'] = MessageSlider
            # custom action
            else:
                founded = False
                for module in self.modules.get(bot_name):
                    try:
                        state_properties['type'] = getattr(module, state_properties['type'])
                        founded = True
                        break
                    except:
                        pass
                # Unknown type of node founded
                if not founded:
                    raise ValueError(
                        'Unknown type ' + '"' + str(state_properties['type']) + '"' + ' of node ' + '"' + str(
                            state_name) + '" in bot "' + bot_name + '".')

    # check if init state is present
    def check_init_state(self, loaded_yaml, bot_name):
        init_state_existis = False
        for state_name, state_parameters in loaded_yaml['states'].items():
            # look for state with name init
            if state_name == 'init':
                init_state_existis = True
                break
        # rise exception, if no state with name init is not present
        if not init_state_existis:
            raise ValueError('There is no "init" state in the yaml files of bot "' + bot_name + '".')

    # checks if all stetes has type
    def check_types(self, loaded_yaml, bot_name):
        for state_name, state_parameters in loaded_yaml['states'].items():
            if state_parameters is None or not ("type" in state_parameters):
                raise ValueError('The node "' + state_name + '" has no type in the bot "' + bot_name + '".')

    # check unique names of states
    def check_unique_names(self, bot_name, loaded_yaml, state_dict):
        for state_name, state_parameters in loaded_yaml['states'].items():
            if 'states' in state_dict.get(bot_name.lower()):
                if state_name in state_dict.get(bot_name.lower())['states'].keys():
                    raise ValueError(
                        'There are nodes of the same name "' + state_name + '" in the bot "' + bot_name + '".')

    # sets missing or default properties
    def set_default_properties(self, loaded_yaml, bot_name):
        for state_name, state_properties in loaded_yaml['states'].items():
            if state_properties['type'] == MessageText:
                self.set_default_properties_message_text(state_properties)
            elif state_properties['type'] == MessageRandomText:
                self.set_default_properties_message_text_random(state_properties)
            elif state_properties['type'] == InputUser:
                self.set_default_properties_input_user(state_properties)
            elif state_properties['type'] == InputContext:
                self.set_default_properties_input_context(state_properties)
            elif state_properties['type'] == ConditionalEquals:
                self.set_default_properties_conditional_equal(state_name, state_properties, bot_name)
            elif state_properties['type'] == ConditionalExists:
                self.set_default_properties_conditional_exists(state_name, state_properties, bot_name)
            elif state_properties['type'] == MessageButtons:
                self.set_default_properties_message_buttons(state_name, state_properties, bot_name)
            elif state_properties['type'] == ChangeContext:
                self.set_default_properties_change_context(state_properties)
            elif state_properties['type'] == MessageIframe:
                self.set_default_properties_message_iframe(state_name, state_properties, bot_name)
            elif state_properties['type'] == MessageCheckboxes:
                self.set_default_properties_message_checkboxes(state_name, state_properties, bot_name)
            elif state_properties['type'] == InputSpecial:
                self.set_default_properties_input_special(state_properties)
            elif state_properties['type'] == MessageSlider:
                self.set_default_properties_message_slider(state_name, state_properties, bot_name)
            else:
                # custom state
                if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
                    state_properties.update({'properties': {}})

    # adds properties to message_text node
    def set_default_properties_message_text(self, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'text': 'Your message here.'}})
        elif not ('text' in state_properties['properties']):
            state_properties['properties'].update({'text': 'Your message here.'})

    # adds properties to message_text_random node
    def set_default_properties_message_text_random(self, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'responses': ['Your message here.']}})
        elif not ('responses' in state_properties['properties']):
            state_properties['properties'].update({'responses': ['Your message here.']})

    # adds properties to input_user node
    def set_default_properties_input_user(self, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'entities': {}, 'log_json': False,
                                                    'require_match': False,
                                                    }})
        if not ('entities' in state_properties['properties']):
            state_properties['properties'].update({'entities': {}})
        if not ('log_json' in state_properties['properties']):
            state_properties['properties'].update({'log_json': False})
        if not ('require_match' in state_properties['properties']):
            state_properties['properties'].update({'require_match': False})

    # adds properties to input_context node
    def set_default_properties_input_context(self, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'entities': {}}})
        if not ('entities' in state_properties['properties']):
            state_properties['properties'].update({'entities': {}})

    # adds properties to conditional_equal node
    def set_default_properties_conditional_equal(self, state_name, state_properties, bot_name):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            raise ValueError(
                'The "properties" field with "value1" and "value2" fields is missing in the state "' + state_name + '" of bot "' + bot_name + '".')
        if not ('value1' in state_properties['properties']):
            raise ValueError(
                'The "value1" field is missing in the properties of state "' + state_name + '" of bot "' + bot_name + '".')
        if not ('value2' in state_properties['properties']):
            raise ValueError(
                'The "value2" field is missing in the properties of state "' + state_name + '" of bot "' + bot_name + '".')

    # adds properties to conditional_exists node
    def set_default_properties_conditional_exists(self, state_name, state_properties, bot_name):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            raise ValueError(
                'The "properties" field with "key" field is missing in the state "' + state_name + '" of bot "' + bot_name + '".')
        if not ('key' in state_properties['properties']):
            raise ValueError(
                'The "key" field is missing in the properties of state "' + state_name + '" in the bot "' + bot_name + '".')

    # adds properties to message_buttons node
    def set_default_properties_message_buttons(self, state_name, state_properties, bot_name):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'buttons': []}})
        elif not ('buttons' in state_properties['properties']) or not (
                    type(state_properties['properties']['buttons']) is list):
            state_properties['properties'].update({'buttons': []})
        for button in state_properties['properties']['buttons']:
            if not (type(button) is OrderedDict):
                raise ValueError(
                    'Button defined in the buttons field of state "' + state_name + '" is not dictionary int bot "' + bot_name + '".')
            if not ('next_state' in button):
                raise ValueError(
                    'The "next_state" field is missing in the buttons of state "' + state_name + '" in the bot "' + bot_name + '".')
            if not ('label' in button):
                button.update({'label': "Label"})
            if not ('type' in button):
                button.update({'type': ""})

    # adds properties to change_context node
    def set_default_properties_change_context(self, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'del_keys': [], 'update_keys': {}}})
        else:
            if not ('del_keys' in state_properties['properties']) or not (
                    isinstance(state_properties['properties']['del_keys'], list)):
                state_properties['properties'].update({'del_keys': []})
            if not ('update_keys' in state_properties['properties']) or not (
                    isinstance(state_properties['properties']['update_keys'], OrderedDict)):
                state_properties['properties'].update({'update_keys': {}})

    # adds properties to message_iframe node
    def set_default_properties_message_iframe(self, state_name, state_properties, bot_name):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            raise ValueError(
                'The "properties" field with "url" field is missing in the state "' + state_name + '" of bot "' + bot_name + '".')
        elif not ('url' in state_properties['properties']):
            raise ValueError(
                'The "url" field is missing in the state "' + state_name + '" of bot "' + bot_name + '".')
        else:
            if not ('height' in state_properties['properties']):
                state_properties['properties'].update({'height': 150})
            elif not (type(state_properties['properties']['height']) is int):
                raise ValueError(
                    'The "height" field is not integer in the state "' + state_name + '" of bot "' + bot_name + '".')
            if not ('scrolling' in state_properties['properties']):
                state_properties['properties'].update({'scrolling': 'yes'})
            if state_properties['properties']['scrolling'] is True:
                state_properties['properties']['scrolling'] = 'yes'
            if state_properties['properties']['scrolling'] is False:
                state_properties['properties']['scrolling'] = 'no'
            if not (state_properties['properties'][
                        'scrolling'].lower() == 'yes' or state_properties['properties'][
                'scrolling'].lower() == 'no'):
                raise ValueError(
                    'The "scrolling" field can be only "yes" or "no" in the state "' + state_name + '" of bot "' + bot_name + '".')
            if not ('width' in state_properties['properties']):
                state_properties['properties'].update({'width': 100})
            elif not (type(state_properties['properties']['width']) is int):
                raise ValueError(
                    'The "width" field is not integer in the state "' + state_name + '" of bot "' + bot_name + '".')
            if not ('align' in state_properties['properties']):
                state_properties['properties'].update({'align': 'left'})
            elif not (state_properties['properties'][
                          'align'].lower() == 'right' or state_properties['properties'][
                'align'].lower() == 'left' or state_properties['properties'][
                'align'].lower() == 'center'):
                raise ValueError(
                    'The "align" field can be only "left", "right" or "center" in the state "' + state_name + '" of bot "' + bot_name + '".')

    # adds properties to message_buttons node
    def set_default_properties_message_checkboxes(self, state_name, state_properties, bot_name):
        if not ('properties' in state_properties) or not (
                    type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'checkboxes': []}})
        elif not ('checkboxes' in state_properties['properties']) or not (
                    type(state_properties['properties']['checkboxes']) is list):
            state_properties['properties'].update({'checkboxes': []})
        for button in state_properties['properties']['checkboxes']:
            if not (type(button) is OrderedDict):
                raise ValueError(
                    'Checkbox defined in the checkboxes field of state "' + state_name + '" is not dictionary in bot "' + bot_name + '".')
            if not ('update_keys' in button):
                button.update({'update_keys': ""})
            if not ('label' in button):
                button.update({'label': "Label"})
            if not ('type' in button):
                button.update({'type': ""})

                # adds properties to change_context node

    def set_default_properties_input_special(self, state_properties):
        if not ('properties' in state_properties) or not (
                    type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'show_input': "both"}})
        else:
            if not ('show_input' in state_properties['properties']):
                state_properties['properties'].update({'show_input': "both"})

    def set_default_properties_message_slider(self, state_name, state_properties, bot_name):
        if not ('properties' in state_properties) or not (
                    type(state_properties['properties']) is OrderedDict):
            raise ValueError(
                'You have to specify at least one entity in the slider state "' + state_name + '" of the bot "' + bot_name + '".')
        else:
            if not ('entities' in state_properties['properties']) or not (
                        type(state_properties['properties']['entities']) is list):
                raise ValueError(
                    'You have to specify at least one entity as list in the slider state "' + state_name + '" of the bot "' + bot_name + '".')
            if not ('max_value' in state_properties['properties']):
                state_properties['properties'].update({'max_value': 100})
            if not ('min_value' in state_properties['properties']):
                state_properties['properties'].update({'min_value': 0})
            if not ('default_values' in state_properties['properties']) or not (
                        type(state_properties['properties']['default_values']) is list):
                defaults = []
                for i in range(0, len(state_properties['properties']['entities'])):
                    defaults.append(0)
                state_properties['properties']['default_values'] = defaults
            elif len(state_properties['properties']['default_values']) != len(
                    state_properties['properties']['entities']):
                raise ValueError(
                    'You specified different number of default values than you specified entites in the slider state "' + state_name + '" of the bot "' + bot_name + '".')
            if not ('step' in state_properties['properties']):
                state_properties['properties'].update({'step': 1})
            if not ('connect' in state_properties['properties']):
                state_properties['properties'].update({'connect': True})
            if not ('tooltips' in state_properties['properties']):
                state_properties['properties'].update({'tooltips': False})
            if not ('tooltips_decimals' in state_properties['properties']):
                state_properties['properties'].update({'tooltips_decimals': 0})
            if not ('tooltips_prefix' in state_properties['properties']):
                state_properties['properties'].update({'tooltips_prefix': ""})
            if not ('tooltips_postfix' in state_properties['properties']):
                state_properties['properties'].update({'tooltips_postfix': ""})

    # check and modifies delays
    def check_delays(self, loaded_yaml, bot_name):
        for state_name, state_properties in loaded_yaml['states'].items():
            if 'delay' not in state_properties['properties']:
                state_properties['properties'].update({'delay': 0})
            elif state_properties['properties']['delay'] is None:
                state_properties['properties'].update({'delay': 0})
            elif not isinstance(state_properties['properties']['delay'], int):
                raise ValueError(
                    'Delay in the node "' + state_name + '" is not not an integer in bot "' + bot_name + '".')

    # loads intent_transitions field from yaml to memory
    def load_intent_transitions(self, loaded_yaml, bot_name):
        if "intent_transitions" in loaded_yaml:
            intent_transitions.get(bot_name.lower()).update(loaded_yaml["intent_transitions"])

    # checks if all states mentioned in intent_transitions exists
    def check_intent_transitions_states_exist(self, bot_name):
        for key in intent_transitions.get(bot_name.lower()):
            intent_state = intent_transitions.get(bot_name.lower())[key]
            if not (intent_state in state_dict.get(bot_name.lower())["states"]):
                raise ValueError(
                    'State "' + intent_state + '" mentioned in intent_transitions doesn\'t exist in bot "' + bot_name + '".')

    # check if all stated defined in transitions really exist
    def check_transition_states_exist(self, bot_name):
        # iterate through all loaded states and check states mentioned in all possible transitions fields
        for state_name, state_content in state_dict.get(bot_name.lower())['states'].items():
            if 'transitions' in state_content:
                if 'match' in state_content['transitions']:
                    reference_state = state_content['transitions']['match']
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist in bot "' + bot_name + '".')
                if 'notmatch' in state_content['transitions']:
                    reference_state = state_content['transitions']['notmatch']
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist in bot "' + bot_name + '".')
                if 'equal' in state_content['transitions']:
                    reference_state = state_content['transitions']['equal']
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist in bot "' + bot_name + '".')
                if 'notequal' in state_content['transitions']:
                    reference_state = state_content['transitions']['notequal']
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist in bot "' + bot_name + '".')
                if 'exists' in state_content['transitions']:
                    reference_state = state_content['transitions']['exists']
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist in bot "' + bot_name + '".')
                if 'notexists' in state_content['transitions']:
                    reference_state = state_content['transitions']['notexists']
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist in bot "' + bot_name + '".')
                if 'next_state' in state_content['transitions']:
                    reference_state = state_content['transitions']['next_state']
                    # next state can be empty
                    if reference_state == "" or reference_state is None:
                        continue
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist in bot "' + bot_name + '".')
            # testing of button transitions, special case
            if 'buttons' in state_content['properties']:
                for button in state_content['properties']['buttons']:
                    reference_state = button['next_state']
                    if reference_state not in state_dict.get(bot_name.lower())['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" buttons field doesn\'t exist in bot "' + bot_name + '".')

    # import custom states from states folder of bot
    def import_custom_states(self, bot_states_folder, bot_name):
        self.modules.update({bot_name: []})
        for path, subdirs, files in os.walk(bot_states_folder):
            for name in files:
                if name.endswith(".py"):
                    file = os.path.join(path, name)
                    spec = importlib.util.spec_from_file_location(name, file)
                    module = importlib.util.module_from_spec(spec)
                    self.modules.get(bot_name).append(module)
                    spec.loader.exec_module(module)

    # return all subdirectories directly in directory
    def get_immediate_subdirectories(self, a_dir):
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name)) and name != "__pycache__"]

import glob
import importlib
from collections import OrderedDict

import yaml
from config import config
from loaded_states import state_dict, intent_transitions
from yaml_parser.yaml_ordered_dict import OrderedDictYAMLLoader
from states import *
from os import listdir
from os.path import isfile, join


# Parses yaml files containing description of dialogue
class YamlParser:
    # folder, where yaml files are stored
    path = config["yaml_files_path"]

    def __init__(self):
        # clear all content in dictionary with loaded states
        state_dict.clear()
        # find all .yml and .yaml files
        files = [f for f in listdir(self.path)
                 if isfile(join(self.path, f)) if f.endswith(('.yml', '.yaml'))]
        # load all files
        for file_name in files:
            self.load_file(file_name)
        # check if init state is present
        self.check_init_state(state_dict)
        # check if all states from intent_transitions exists
        self.check_intent_transitions_states_exist()
        # check if all states mentioned in transitions really exist
        self.check_transition_states_exist()

    # load yaml file
    def load_file(self, file_name):
        # add missing slash to directory path
        if not (self.path.endswith('/')):
            self.path += '/'
        with open(self.path + file_name, 'r', encoding="utf8") as stream:
            try:
                # load yaml to OrderedDict
                loaded_yaml = yaml.load(stream, OrderedDictYAMLLoader)
                # check unique names of states
                self.check_unique_names(loaded_yaml, state_dict)
                # checks if all states has type
                self.check_types(loaded_yaml)
                # add missing transitions
                self.modify_transitions(loaded_yaml)
                # changes representation of node types to intern objects
                self.types_to_intern_representation(loaded_yaml)
                # sets default or missing properties
                self.set_default_properties(loaded_yaml)
                self.check_delays(loaded_yaml)
                if not ('states' in state_dict):
                    # update whole dictionary
                    state_dict.update(loaded_yaml)
                else:
                    # update only states, to not overwrite everything
                    state_dict['states'].update(loaded_yaml['states'])
                # load intent_transitions field
                self.load_intent_transitions(loaded_yaml)
            except yaml.YAMLError as exc:
                print(exc)

    # Modifies transitions to intern format
    def modify_transitions(self, loaded_yaml):
        i = 0
        states = list(loaded_yaml['states'].items())
        # Iterate through all states from loaded yaml
        for state_name, state_parameters in loaded_yaml['states'].items():
            self.add_transitions(state_parameters, states, i)
            self.modify_flow_transitions(state_parameters)
            self.modify_return_transitions(state_parameters)
            i += 1

    # Add transition to nodes, which has default value
    def add_transitions(self, state_parameters, states, i):
        if not ("transitions" in state_parameters):
            # If the transitions field is missing, add next state
            if i + 1 < len(states):
                state_parameters['transitions'] = {'next_state': states[i + 1][0]}
            else:
                # Leave it blank, if we are at the end of file
                state_parameters['transitions'] = {'next_state': ''}

    # changes transition from flow to the first state of flow
    def modify_flow_transitions(self, state_parameters):
        if "transitions" in state_parameters:
            if "flow" in state_parameters["transitions"]:
                flow_name = state_parameters["transitions"]["flow"]
                # find file with some extension and the right name
                with open(glob.glob(self.path + flow_name + '.*')[0], 'r', encoding="utf8") as stream:
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
    def types_to_intern_representation(self, loaded_yaml):
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
            # custom action
            else:
                try:
                    state_properties['type'] = getattr(
                        importlib.import_module("." + state_properties['type'], "states.user"),
                        state_properties['type'])
                # Unknown type of node founded
                except:
                    raise ValueError(
                        'Unknown type ' + '"' + state_properties['type'] + '"' + ' of node ' + '"' + state_name + '"')

    # check if init state is present
    def check_init_state(self, loaded_yaml):
        init_state_existis = False
        for state_name, state_parameters in loaded_yaml['states'].items():
            # look for state with name init
            if state_name == 'init':
                init_state_existis = True
                break
        # rise exception, if no state with name init is not present
        if not init_state_existis:
            raise ValueError('There is no "init" state in the yaml files.')

    # checks if all stetes has type
    def check_types(self, loaded_yaml):
        for state_name, state_parameters in loaded_yaml['states'].items():
            if state_parameters is None or not ("type" in state_parameters):
                raise ValueError('The node "' + state_name + '" has no type.')

    # check unique names of states
    def check_unique_names(self, loaded_yaml, state_dict):
        for state_name, state_parameters in loaded_yaml['states'].items():
            if 'states' in state_dict:
                if state_name in state_dict['states'].keys():
                    raise ValueError('There are nodes of the same name "' + state_name + '".')

    # sets missing or default properties
    def set_default_properties(self, loaded_yaml):
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
                self.set_default_properties_conditional_equal(state_name, state_properties)
            elif state_properties['type'] == ConditionalExists:
                self.set_default_properties_conditional_exists(state_name, state_properties)
            elif state_properties['type'] == MessageButtons:
                self.set_default_properties_message_buttons(state_name, state_properties)
            elif state_properties['type'] == ChangeContext:
                self.set_default_properties_change_context(state_properties)
            elif state_properties['type'] == MessageIframe:
                self.set_default_properties_message_iframe(state_name, state_properties)
            elif state_properties['type'] == MessageCheckboxes:
                self.set_default_properties_message_checkboxes(state_name, state_properties)
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
    def set_default_properties_conditional_equal(self, state_name, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            raise ValueError(
                'The "properties" field with "value1" and "value2" fields is missing in the state "' + state_name + '".')
        if not ('value1' in state_properties['properties']):
            raise ValueError(
                'The "value1" field is missing in the properties of state "' + state_name + '".')
        if not ('value2' in state_properties['properties']):
            raise ValueError(
                'The "value2" field is missing in the properties of state "' + state_name + '".')

    # adds properties to conditional_exists node
    def set_default_properties_conditional_exists(self, state_name, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            raise ValueError(
                'The "properties" field with "key" field is missing in the state "' + state_name + '".')
        if not ('key' in state_properties['properties']):
            raise ValueError(
                'The "key" field is missing in the properties of state "' + state_name + '".')

    # adds properties to message_buttons node
    def set_default_properties_message_buttons(self, state_name, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'buttons': []}})
        elif not ('buttons' in state_properties['properties']) or not (
                    type(state_properties['properties']['buttons']) is list):
            state_properties['properties'].update({'buttons': []})
        for button in state_properties['properties']['buttons']:
            if not (type(button) is OrderedDict):
                raise ValueError(
                    'Button defined in the buttons field of state "' + state_name + '" is not dictionary.')
            if not ('next_state' in button):
                raise ValueError(
                    'The "next_state" field is missing in the buttons of state "' + state_name + '".')
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
    def set_default_properties_message_iframe(self, state_name, state_properties):
        if not ('properties' in state_properties) or not (type(state_properties['properties']) is OrderedDict):
            raise ValueError(
                'The "properties" field with "url" field is missing in the state "' + state_name + '".')
        elif not ('url' in state_properties['properties']):
            raise ValueError(
                'The "url" field is missing in the state "' + state_name + '".')
        else:
            if not ('height' in state_properties['properties']):
                state_properties['properties'].update({'height': 150})
            elif not (type(state_properties['properties']['height']) is int):
                raise ValueError(
                    'The "height" field is not integer in the state "' + state_name + '".')
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
                    'The "scrolling" field can be only "yes" or "no" in the state "' + state_name + '".')
            if not ('width' in state_properties['properties']):
                state_properties['properties'].update({'width': 100})
            elif not (type(state_properties['properties']['width']) is int):
                raise ValueError(
                    'The "width" field is not integer in the state "' + state_name + '".')
            if not ('align' in state_properties['properties']):
                state_properties['properties'].update({'align': 'left'})
            elif not (state_properties['properties'][
                          'align'].lower() == 'right' or state_properties['properties'][
                'align'].lower() == 'left' or state_properties['properties'][
                'align'].lower() == 'center'):
                raise ValueError(
                    'The "align" field can be only "left", "right" or "center" in the state "' + state_name + '".')

    # adds properties to message_buttons node
    def set_default_properties_message_checkboxes(self, state_name, state_properties):
        if not ('properties' in state_properties) or not (
                    type(state_properties['properties']) is OrderedDict):
            state_properties.update({'properties': {'checkboxes': []}})
        elif not ('checkboxes' in state_properties['properties']) or not (
                    type(state_properties['properties']['checkboxes']) is list):
            state_properties['properties'].update({'checkboxes': []})
        for button in state_properties['properties']['checkboxes']:
            if not (type(button) is OrderedDict):
                raise ValueError(
                    'Checkbox defined in the checkboxes field of state "' + state_name + '" is not dictionary.')
            if not ('update_keys' in button):
                button.update({'update_keys': ""})
            if not ('label' in button):
                button.update({'label': "Label"})
            if not ('type' in button):
                button.update({'type': ""})

    # check and modifies delays
    def check_delays(self, loaded_yaml):
        for state_name, state_properties in loaded_yaml['states'].items():
            if 'delay' not in state_properties['properties']:
                state_properties['properties'].update({'delay': 0})
            elif state_properties['properties']['delay'] is None:
                state_properties['properties'].update({'delay': 0})
            elif not isinstance(state_properties['properties']['delay'], int):
                raise ValueError('Delay in the node "' + state_name + '" is not not an integer.')

    # loads intent_transitions field from yaml to memory
    def load_intent_transitions(self, loaded_yaml):
        if "intent_transitions" in loaded_yaml:
            intent_transitions.update(loaded_yaml["intent_transitions"])

    # checks if all states mentioned in intent_transitions exists
    def check_intent_transitions_states_exist(self):
        for key in intent_transitions:
            intent_state = intent_transitions[key]
            if not (intent_state in state_dict["states"]):
                raise ValueError('State "' + intent_state + '" mentioned in intent_transitions doesn\'t exist.')

    # check if all stated defined in transitions really exist
    def check_transition_states_exist(self):
        # iterate through all loaded states and check states mentioned in all possible transitions fields
        for state_name, state_content in state_dict['states'].items():
            if 'match' in state_content['transitions']:
                reference_state = state_content['transitions']['match']
                if reference_state not in state_dict['states']:
                    raise ValueError(
                        'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist.')
            if 'notmatch' in state_content['transitions']:
                reference_state = state_content['transitions']['notmatch']
                if reference_state not in state_dict['states']:
                    raise ValueError(
                        'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist.')
            if 'equal' in state_content['transitions']:
                reference_state = state_content['transitions']['equal']
                if reference_state not in state_dict['states']:
                    raise ValueError(
                        'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist.')
            if 'notequal' in state_content['transitions']:
                reference_state = state_content['transitions']['notequal']
                if reference_state not in state_dict['states']:
                    raise ValueError(
                        'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist.')
            if 'exists' in state_content['transitions']:
                reference_state = state_content['transitions']['exists']
                if reference_state not in state_dict['states']:
                    raise ValueError(
                        'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist.')
            if 'notexists' in state_content['transitions']:
                reference_state = state_content['transitions']['notexists']
                if reference_state not in state_dict['states']:
                    raise ValueError(
                        'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist.')
            if 'next_state' in state_content['transitions']:
                reference_state = state_content['transitions']['next_state']
                # next state can be empty
                if reference_state == "" or reference_state is None:
                    continue
                if reference_state not in state_dict['states']:
                    raise ValueError(
                        'State "' + reference_state + '" mentioned in "' + state_name + '" transitions field doesn\'t exist.')
            # testing of button transitions, special case
            if 'buttons' in state_content['properties']:
                for button in state_content['properties']['buttons']:
                    reference_state = button['next_state']
                    if reference_state not in state_dict['states']:
                        raise ValueError(
                            'State "' + reference_state + '" mentioned in "' + state_name + '" buttons field doesn\'t exist.')

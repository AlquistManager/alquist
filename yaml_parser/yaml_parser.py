import glob
import sys
from collections import OrderedDict

import yaml
from loaded_states import state_dict
from yaml_parser.yaml_ordered_dict import OrderedDictYAMLLoader
from states import *
from os import listdir
from os.path import isfile, join


# Parses yaml files containing description of dialogue
class YamlParser:
    # folder, where yaml files are stored
    path = sys.argv[4]

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

    # load yaml file
    def load_file(self, file_name):
        # add missing slash to directory path
        if not (self.path.endswith('/')):
            self.path += '/'
        with open(self.path + file_name, 'r') as stream:
            try:
                # load yaml to OrderedDict
                loaded_yaml = yaml.load(stream, OrderedDictYAMLLoader)
                # check unique names of states
                self.check_unique_names(loaded_yaml, state_dict)
                # checks if all stetes has type
                self.check_types(loaded_yaml)
                # add missing transitions
                self.modify_transitions(loaded_yaml)
                # changes representation of node types to intern objects
                self.types_to_intern_representation(loaded_yaml)
                # sets default or missing properties
                self.set_default_properties(loaded_yaml)
                if not ('states' in state_dict):
                    # update whole dictionary
                    state_dict.update(loaded_yaml)
                else:
                    # update only states, to not overwrite everything
                    state_dict['states'].update(loaded_yaml['states'])
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
                with open(glob.glob(self.path + flow_name + '.*')[0], 'r') as stream:
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
                # TODO add custom actions
            else:
                # Unknown type of node founded
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
                # TODO add custom actions

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

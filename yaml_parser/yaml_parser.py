import glob
import sys
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
        # check correctness of yaml's syntax
        self.check_structure(state_dict)

    # load yaml file
    def load_file(self, file_name):
        with open(self.path + file_name, 'r') as stream:
            try:
                # load yaml to OrderedDict
                loaded_yaml = yaml.load(stream, OrderedDictYAMLLoader)
                # add missing transitions
                self.modify_transitions(loaded_yaml)
                # changes representation of node types to intern objects
                self.types_to_intern_representation(loaded_yaml)
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
                        for state_name, state_parameters in loaded_yaml['states'].items():
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
                state_parameters["transitions"] = ''

    # Change string representation of states into inner representation of objects
    def types_to_intern_representation(self, loaded_yaml):
        for key, value in loaded_yaml['states'].items():
            if value['type'].lower() == 'message_text':
                value['type'] = MessageText
            elif value['type'].lower() == 'message_text_random':
                value['type'] = MessageRandomText
            elif value['type'].lower() == 'input_user':
                value['type'] = InputUser
            elif value['type'].lower() == 'input_context':
                value['type'] = InputContext
            elif value['type'].lower() == 'conditional_equal':
                value['type'] = ConditionalEquals
            elif value['type'].lower() == 'conditional_exists':
                value['type'] = ConditionalExists
                # TODO add custom actions
            else:
                # Unknown type of node founded
                raise ValueError('Unknown type ' + '"' + value['type'] + '"' + ' of node ' + '"' + key + '"')

    # check structure of yaml files
    def check_structure(self, loaded_yaml):
        init_state_existis = False
        for key, value in loaded_yaml['states'].items():
            # look for state with name init
            if key == 'init':
                init_state_existis = True
                break
        # rise exception, if no state with name init is not present
        if not init_state_existis:
            raise ValueError('There is no "init" state in the yaml files.')

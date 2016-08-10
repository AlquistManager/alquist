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
                 if isfile(join(self.path, f)) if f.endswith( ('.yml','.yaml') )]
        # load all files
        for file_name in files:
            self.load_file(file_name)

    # load yaml file
    def load_file(self, file_name):
        with open(self.path + file_name, 'r') as stream:
            try:
                # load yaml to OrderedDict
                loaded_yaml = yaml.load(stream, OrderedDictYAMLLoader)
                # add missing transitions
                self.add_transitions(loaded_yaml)
                # changes representation of node types to intern objects
                self.types_to_intern_representation(loaded_yaml)
                state_dict.update(loaded_yaml)
            except yaml.YAMLError as exc:
                print(exc)

    # Add transition to nodes, which has default value
    def add_transitions(self, loaded_yaml):
        i = 0
        states = list(loaded_yaml['states'].items())
        # Iterate through all states from loaded yaml
        for key, value in loaded_yaml['states'].items():
            if not ("transitions" in value):
                # If the transitions field is missing, add next state
                if i + 1 < len(states):
                    value['transitions'] = {'next_state': states[i + 1][0]}
                else:
                    # Leave it blank, if we are at the end of file
                    value['transitions'] = {'next_state': ''}
            i += 1

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

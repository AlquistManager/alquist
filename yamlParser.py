import yaml
from yaml_ordered_dict import OrderedDictYAMLLoader


class YamlParser:
    def __init__(self):
        with open("C:/Users/ermrk/PycharmProjects/alquist/yaml/example/weather.yml", 'r') as stream:
            try:
                loadedYaml = yaml.load(stream, OrderedDictYAMLLoader)
                self.addTransitions(loadedYaml)
                return
            except yaml.YAMLError as exc:
                print(exc)

    def addTransitions(self, loadedYaml):
        for key, value in loadedYaml['states'].items():
           if not("transitions" in value):
               #TODO add transition to next state
               value['transitions'] = "ADDED"

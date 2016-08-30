from IO.input import *
from config import config
from yaml_parser.yaml_parser import YamlParser

if __name__ == '__main__':
    # Load and parse yaml files
    flask.before_first_request(YamlParser)
    # Start flask
    flask.run(port=int(config["port"]), debug=False, threaded=True)

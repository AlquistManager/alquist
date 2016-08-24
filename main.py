import sys

from IO.input import *
from yaml_parser.yaml_parser import YamlParser

if __name__ == '__main__':
    # Load and parse yaml files
    YamlParser()
    # Start flask
    flask.run(port=int(sys.argv[1]), debug=False, threaded=True)

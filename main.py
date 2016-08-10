import sys

from IO.input import *

# Start with parameters:
#   Port - port to run
#   Webhook URL - url where the responses will be returned

# How to test:
#   Create webhook in ngrok
#   Start Main.py with parameters: [port] [webhook URL]
#   example of parameters: 5000 http://2891e08c.ngrok.io
#
#   To register new user: curl -X POST "http://127.0.0.1:5000/start"
#
#   To send message: curl -H "Content-Type: application/json; charset=\"utf-8\"" -X POST
#                    -d "{\"id\":\"5e7f82f3-cdfd-40f4-9008-4e0247c774a7\", \"text\":\"yes\"}" "http://127.0.0.1:5000/"
from yaml_parser.yaml_parser import YamlParser

if __name__ == '__main__':
    #Load and parse yaml files
    YamlParser()
    # Start flask
    flask.run(port=int(sys.argv[1]), debug=True)

# Handles input from the user by Flask
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS

from solver import process_request
from yaml_parser.yaml_parser import YamlParser

flask = Flask(__name__)
cors = CORS(flask)


# Load and parse yaml files
@flask.before_first_request
def load_yamls():
    YamlParser()


# Used for sending messages to the bot
@flask.route("/", methods=['POST'])
def get_input():
    try:
        text = request.json['text']
        state = request.json['state']
        context = request.json['context']
        session = request.json['session']
    except KeyError:
        # Missing 'session_id' or 'text'
        return jsonify(ok=False, message="Missing parameters.")

        # create UUID for session if it does't exist
    if session is "":
        session = str(uuid.uuid4())

        # try:
        # execute states
        response = process_request(state, context, text, session)
        return jsonify(text=response['response'], state=response['next_state'], context=response['context'],
                       session=session)
        # except:
        # Error in execution
        #   return jsonify(ok=False, message="Error during execution.")

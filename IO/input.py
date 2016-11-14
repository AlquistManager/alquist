# Handles input from the user by Flask
import uuid

import loaded_states
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from loggers import create_loggers
from solver import process_request
from yaml_parser.yaml_parser import YamlParser

flask = Flask(__name__)
cors = CORS(flask)


# Load and parse yaml files
@flask.before_first_request
def load_yamls():
    YamlParser()
    create_loggers()


# Used for sending messages to the bot
@flask.route("/", methods=['POST'])
def get_input():
    try:
        text = request.json['text']
        state = request.json['state']
        context = request.json['context']
        session = request.json['session']
        bot = request.json['bot']
        payload = request.json['payload']
        loaded_states.actual_bot = bot
    except KeyError:
        # Missing 'session_id' or 'text'
        return jsonify(ok=False, message="Missing parameters.")

        # create UUID for session if it does't exist
    if session is "":
        session = str(uuid.uuid4())

        # try:
        # execute states
    if loaded_states.state_dict.get(bot) is None:
        return jsonify(ok=False, message="Bot with this name '" + bot + "' doesn't exist.")
    response = process_request(bot, state, context, text, session, payload)
    return jsonify(messages=response['response'], state=response['next_state'], context=response['context'],
                   session=session, input=response['input'])
    # except:  # Error in execution
    #    return jsonify(ok=False, message="Error during execution.")

# Methods to show client
@flask.route('/client/')
def get_bot1():
    return send_from_directory("../client/", "index.html")

@flask.route('/client/<file>', defaults={'path': ''})
@flask.route('/client/<path:path>/<file>')
def get_bot2(path, file):
    return send_from_directory("../client/" + path, file)

@flask.route('/<bot>/')
def get_bot3(bot):
    return send_from_directory("../client/", "index.html")


@flask.route('/<bot>/<file>', defaults={'path': ''})
@flask.route('/<bot>/<path:path>/<file>')
def get_bot4(bot, path, file):
    return send_from_directory("../client/" + path, file)

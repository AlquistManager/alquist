# Handles input from the user by Flask

from flask import Flask, request, jsonify
from flask_cors import CORS

import sessions

flask = Flask(__name__)
cors = CORS(flask)


# Used for sending messages to the bot
@flask.route("/", methods=['POST'])
def get_input():
    try:
        state_name = request.json['state_name']
        context = request.json['context']
        text = request.json['text']
        #TODO call state execute
        #TODO make some response
        return jsonify(text=None,state_name=None,context=None)
    except KeyError:
        # Missing 'session_id' or 'text'
        return jsonify(ok=False, message="Missing parameters.")

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
        text = request.json['text']
        state = request.json['state']
        context = request.json['context']
        # TODO call state execute
        # TODO make some response
        return jsonify(text=text, state=state, context=context)
    except KeyError:
        # Missing 'session_id' or 'text'
        return jsonify(ok=False, message="Missing parameters.")

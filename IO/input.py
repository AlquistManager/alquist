# Handles input from the user by Flask

from flask import Flask, request, jsonify
from flask_cors import CORS

import sessions

flask = Flask(__name__)
cors = CORS(flask)


# Used for registration of new users
@flask.route("/start", methods=['POST'])
def create_new_session():
    session_id = sessions.register_user()
    return jsonify(session_id=session_id)


# Used for sending messages to the bot
@flask.route("/", methods=['POST'])
def get_input():
    try:
        session_id = request.json['session_id']
        if session_id in sessions.sessions:
            # user with session_id has been created already
            session = sessions.sessions[session_id]
            text = request.json['text']
            session.input_buffer.put(text)
            return jsonify(ok=True)
        else:
            # wrong user id
            return jsonify(ok=False, message="User with given id doesn't exist.")
    except KeyError:
        # Missing 'session_id' or 'text'
        return jsonify(ok=False, message="Missing parameters.")


@flask.route("/session", methods=['POST'])
def get_session_history():
    try:
        session_id = request.json['session_id']
        if session_id in sessions.sessions:
            # user with session_id has been created already
            session_history = sessions.sessions[session_id].session_history
            return jsonify(ok=True, session_history=session_history)
        else:
            # wrong user id
            return jsonify(ok=False, message="User with given id doesn't exist.")
    except KeyError:
        # Missing 'session_id' or 'text'
        return jsonify(ok=False, message="Missing parameters.")

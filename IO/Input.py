# Handles input from the user by Flask

from flask import Flask, request, jsonify

import sessions

flask = Flask(__name__)


# Used for registration of new users
@flask.route("/start", methods=['POST'])
def register_new_user():
    user_id = sessions.register_user()
    return jsonify(user_id=user_id)


# Used for sending messages to the bot
@flask.route("/", methods=['POST'])
def get_input():
    try:
        user_id = request.json['user_id']
        if user_id in sessions.sessions:
            # user with user_id has been created already
            session = sessions.sessions[user_id]
            text = request.json['text']
            session.session_io.input_buffer.put(text)
            return jsonify(ok=True)
        else:
            # wrong user id
            return jsonify(ok=False, message="User with given id doesn't exist.")
    except KeyError:
        # Missing 'user_id' or 'text'
        return jsonify(ok=False, message="Missing parameters.")

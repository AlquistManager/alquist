# Handling sessions for users
import uuid

from session import Session

sessions = {}


# Register new user, create session for him, put both into dictionary and return id of new user
def register_user():
    # create UUID for user
    session_id = str(uuid.uuid4())
    # create new session
    session = Session(session_id)
    session.start()
    # save session to dictionary
    sessions[session_id] = session
    return session_id

# Input output class for session
from queue import Queue

from IO.output import Output


class SessionIO:
    def __init__(self, user_id):
        self.user_id = user_id
        # buffer for saving user's input
        self.input_buffer = Queue()

    def send(self, text):
        Output.response(text + "\n", self.user_id)

    def recieve(self) -> str:
        # waits for the buffer to contain something
        while self.input_buffer.empty():
            pass
        return self.input_buffer.get()

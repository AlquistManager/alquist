# Demo input output class


class SessionIO:
    def __init__(self, session_id):
        self.session_id = session_id

    def send(self, text):
        print(text+"\n")

    def recieve(self) -> str:
        return input()

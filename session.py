import logging
import threading

from demo import state_dict
from sessionIO import SessionIO


# Session is a class representing a conversation that user has with the bot after activating it.
# Its instance is created upon activating the bot and it is destroyed after the user finishes
# the conversation or upon prolonged inactivity.

# It contains the clients ID, current session context, current state (class state) and next state (name)

# Each session runs on own thread

class Session(threading.Thread):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.context = dict(user_id=user_id)
        self.next_state = "init"
        self.session_io = SessionIO(user_id)
        self.current_state = None
        self.log_console = None


    # start thread
    def run(self):
        self.execute()

    def execute(self):
        self.setup_log()
        # TODO: determine exact place for build_state() function, clear_context function atd...
        while self.next_state:
            self.current_state = self.build_state()  # TODO: determine what is state_dict and where it is
            self.next_state = self.current_state.execute(self)
        self.log_console.info('Successfully Finished Conversation')

    def setup_log(self):
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='test.log',
                            filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        self.log_console = logging.getLogger('DM.user:' + str(self.user_id))

    def build_state(self):
        next_st = state_dict['states'][self.next_state]
        func = next_st.get('type', lambda: "nothing")
        return func(self.next_state, next_st['properties'], next_st['transitions'])

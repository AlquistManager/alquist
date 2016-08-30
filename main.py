from IO.input import *
from config import config

if __name__ == '__main__':
    # Start flask
    flask.run(port=int(config["port"]), debug=False, threaded=True)

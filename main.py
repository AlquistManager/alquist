from IO.input import *
from config import config

if __name__ == '__main__':
    print("Alquist: http://127.0.0.1:5000/")
    print("Client: http://127.0.0.1:5000/client/index.html")
    # Start flask
    flask.run(port=int(config["port"]), debug=False, threaded=True, host="0.0.0.0")


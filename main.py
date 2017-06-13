import os

from IO.input import *
from config import config

if __name__ == '__main__':
    print("Alquist: http://127.0.0.1:5000/")
    for bot_name in [name for name in os.listdir("bots")
                if os.path.isdir(os.path.join("bots", name)) and name!="__pycache__"]:
        print(bot_name.capitalize()+" client: http://127.0.0.1:5000/"+bot_name+"/")
    print("editor: http://127.0.0.1:5000/editor/")
    # Start flask
    flask.run(port=int(config["port"]), debug=False, threaded=True, host="0.0.0.0")


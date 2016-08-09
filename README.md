Alquist
=======
Alquist is dialogue manager created by Jakub Konrád and Petr Marek.

## Installation
You need Python 3. To run Alquist use command

	py -3 main.py [port] [webhook URL]
``Port`` field defines the port on which the Alquist will run.
``Webhook URL`` field defines the URL of webhoook, where responses will be send.
For example

	py -3 main.py 5000 http://964bdc06.ngrok.io
You can use ngrok to run webhook on your localhost.

## API
### Register new session
To begin with dialogue, you have to register new user. You register new user by POST request to 

	http://127.0.0.1:5000/start
You can test it by CURL

	curl -X POST "http://127.0.0.1:5000/start"
The answer is JSON containing ``session_id`` of new user. Use this ``session_id`` for further communication with the dialogue manager.

### Sending input
To send input send POST with JSON containing fields ``session_id`` and ``text`` request to

	http://127.0.0.1:5000/
Obtaining of ``session_id`` is described in ``Register new user`` section. The ``text`` field contains text, which you want to send to the dialogue manager.
You can test it by CURL

    curl -H "Content-Type: application/json; charset=\"utf-8\"" -X POST -d "{\"session_id\":\"INSTERT_SESSION_ID\", \"text\":\"text\"}" "http://127.0.0.1:5000/"
The answer is JSON with field ``OK`` containing value ``true`` or ``false``. Dialogue's manager response is send to webhook defined during start of dialogue manager.

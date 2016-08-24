Alquist
=======
Alquist is dialogue manager created by Jakub Konrád and Petr Marek.

You can use HTML client https://github.com/konrajak/alquist-client for workig with Alquist.

## Installation
You need Python 3. 

We use WIT.ai as our npl service currently so you will need to install WIT as well

	pip install wit
	
We use PyYaml. You need to install it by

    pip install PyYaml

We use Flask-Cors. You need to install it by

    pip install -U flask-cors

To run Alquist use command

	py -3 main.py [port] [webhook URL] [wit server access token] [Folder containing yamls]
``Port`` field defines the port on which the Alquist will run.
``Webhook URL`` field defines the URL of webhoook, where responses will be send. (--- NOT USED CURRENTLY, BUT INSERT SOME VALUE ---)
``WIT server access token`` defines which wit.ai app will you use. For our demo use ``NXOFXMBCIA6YAIXNNWYXJIJPC22AK35V``
``Folder containing yamls`` path to folder, where yaml files are located.
For example

	py -3 main.py 5000 http://964bdc06.ngrok.io NXOFXMBCIA6YAIXNNWYXJIJPC22AK35V C:\Users\user\yaml\

## API

###Request
To communicate with Alquist use POST requests to url, on which the Alquist is running. POST have to contains JSON with fields:

- text
    Contains user's input text. You can leave it blank, if user has nothing to say (when the Alquist starts a dialogue and we need to prompt
    it to start for example).
- state
    Name of state, where we currently are. The state is "init" at the start of dialogue usually. Must contain something every time.
- context
    Json object representing context. There must be empty Json object at least every time.
- session
    ID of session used during logging. Can be empty at the start of dialogue.
    
###Response
Response contains JSON with fields:

- text
    List of Alquist's answers. This is the field, which you want to show to user somehow probably.
- state
    Name of new state, where we get to. Use this name in the next request (state field).
- context
    Json object containing updated context. Use this object in the next request (context field).
- session
    Generated ID of session used during logging. Use this ID in the next request (session field).
    
###Example
####Request
    curl -H "Content-Type: application/json; charset=\"utf-8\"" -X POST -d "{\"text\":\"INSERT_INPUT_TEXT\", \"state\":\"INSERT_STATE_NAME\", \"context\":\"INSERT_CONTEXT_OBJECT\", \"session\":\"INSERT_SESSION_ID\"}" "INSERT_ALQUIST_URL"

Specific example:

    curl -H "Content-Type: application/json; charset=\"utf-8\"" -X POST -d "{\"text\":\"Hello world!\", \"state\":\"init\", \"context\":{}, \"session\":\"\"}" "http://127.0.0.1:5000/"
Alquist
=======
http://www.alquistai.com/

Alquist is dialogue manager created by Jakub Konrád and Petr Marek.

You can test current demo at https://alquistmanager.github.io/alquist-client/?e=https://alquist.herokuapp.com&bot=demo_tel

You can use HTML client https://github.com/konrajak/alquist-client for workig with Alquist.

All information about writing your bot is here https://github.com/AlquistManager/alquist-yaml-editor/blob/master/How%20to%20write%20your%20bot.md

## Installation
You need Python 3. 


We use PyYaml. You need to install it by

    pip install PyYaml

We use Flask-Cors. You need to install it by

    pip install -U flask-cors
    
We currently use WIT.ai as our nlp service so you will need to install WIT as well

	pip install wit
	
Alternatively we are testing nlp created using [MorphoDiTa tool](http://ufal.mff.cuni.cz/morphodita) ([Mozilla Public License 2.0](http://www.mozilla.org/MPL/2.0/)) and [MorfFlex Czech models](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1674) ([Attribution-NonCommercial-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-nc-sa/3.0/)). You will need to install the MorphoDiTa tool package.
	
	pip install ufal.morphodita
	
Additional required packages can be found in requirements.txt file.

## Run
To run Alquist use command

	py -3 main.py
	
You can change Alquist's parameters. They are stored in the ``config.py``.

``port`` field defines the port on which the Alquist will run.

``wit_token`` defines which Wit.ai app will you use. For our demo use ``NXOFXMBCIA6YAIXNNWYXJIJPC22AK35V``

``debug`` displays contents of context while bot is running, useful for debugging, values ``True`` or ``False``

For example:

	config = {"port": 5000,
          "wit_token": "NXOFXMBCIA6YAIXNNWYXJIJPC22AK35V",
          "debug": True}

## API

###Request
To communicate with Alquist use POST requests to url, on which the Alquist is running. POST have to contains JSON with fields:

- ``text``
    Contains user's input text. You can leave it blank, if user has nothing to say (when the Alquist starts a dialogue and we need to prompt
    it to start for example).
- ``state``
    Name of state, where we currently are. The state is "init" at the start of dialogue usually. Must contain something every time.
- ``context``
    Json object representing context. There must be empty Json object at least every time.
- ``session``
    ID of session used during logging. Can be empty at the start of dialogue.
- ``bot``
    Name of bot.
- ``payload``
    Additional information for states in the form of JSON object.
    
###Response
Response contains JSON with fields:

- messages
    List of Alquist's answers. Each answer is object.
    - type
        Type of message. It can be ``text``, ``button``, ``iframe`` or ``slider``.
    - payload
        Information about message. It differs according to type of message:
        - ``text`` type
            - text
                Text to show
        - ``button`` type
            - label
                Button's label
            - next_state
                State to transform to after button click
            - type
                Type of button. This field doesn't have any specific values. You can send some string and implement button according to it in client.
        - ``iframe`` type
            - url
                Iframe's url
            - width
                Iframe's width (in the percents)
            - height
                Iframe's width (in the pixels)
            - scrolling
                Will be scrollbar visible?
            - align
                Iframe's align
        - ``slider`` type
            - entities
                List of entities to save values into context
            - default_values
                List of default values of sliders
            - min_value
                Minimal value of slider
            - max_value
                Maximal value of slider
            - step
                Size of step of one slider
            - connect
                Should be sliders connected by color line?
            - tooltips
                Should be tooltips shown above the sliders?
            - tooltips_decimals
                Number of decimal numbers of tooltips
            - tooltips_prefix
                Prefix of tooltips
            - tooltips_postfix
                Postfix of tooltips
            
    - delay
        Delay of massage in the milliseconds.        
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

## Docker
Alquist is prepared to be run in a Docker container. The setup process is quite straightforward.
###Building an image
Dockerfile is already present in the main directory. Run ``docker build -t alquist .`` to build the Docker image for Alquist. Alternatively, you can obtain pre-built image from Docker Hub with the ``docker pull alquistmanager/alquist`` command.
###Launching a container
Once the image is built, run the ``run-docker-container.sh`` bash script. There are two parameters required: First is a port you want Alquist to run on and the second is absolute path to your ``.yml`` files.

How to write your bot using ALQUIST
===================================
Alquist is dialogue manager created by Jakub Konrád and Petr Marek.

## General tips
### Start of the dialogue
When writing yaml representation of your bot, keep in mind that the initial state for your bot should be called ``init``
Ihere always needs to be ``init`` state in your yaml representation.

For example:

	init:
        type: message_text
        properties:
            text: Hello, my name is Talkatron 3000
        transitions: 
            next_state: state2

### Transitions
Each state must have transitions field, since it is used in constructor. If the transitions field is empty,
conversation ends after executing current state.

For example:

	state1:
        type: message_text
        properties:
            text: Hello World!
        transitions: 
            
            


### State construction
States have UNIQUE ``name`` across all your flows. There can't be two states with the same name.

Each state declaration must contain fields ``type`` declaring the state type,
``properties`` containing the state parameters, and ``transitions`` which holds information about next state

	[name]:
        type: [state_type]
        properties:
            [state_properties]
        transitions:
            [state_transitions]
            
     
### Invoking session context        
To use a variable from the session context, use ``'{{variable}}'``
Examples:

	state1:
        type: message_text
        properties:
            text: My name is '{{name}}'
        transitions:

Bot replaces ``'{{name}}'`` with value of the ``name`` key saved in the session context and sends ie. "My name is Max"

	state1:
        type: conditional_equal
        properties:
            value1: '{{ intent }}'
            value2: greeting
        transitions:
            equal: positive_case
            notequal: negative_case

Bot replaces ``'{{intent}}'`` with value of the ``intent`` key saved in the session context and compares it with string "greeting".



## State descriptions
### message_text
message_text sends a message to user.

Example:

	[name]:
        type: message_text
        properties:
            text: [message_text]
        transitions:
            next_state: [next_state_name]
``text`` field contains a string, **REQUIRED**

``next_state`` field contains name of the next state

Default property values:
* ``text``: *Your message here.*


### message_text_random
message_text_random sends a message from the list at random to user.

Example:

	[name]:
        type: message_text_random
        properties:
            responses:
                - [response1]
                - [response2]
        transitions:
            next_state: [next_state_name]
``responses`` field contains strings with responses to be selected at random, **REQUIRED**

``next_state`` field contains name of the next state

Default property values:
* ``responses``: *Your messages here.* 


### input_user
input_user sends user a prompt, waits for user response and saves entities from the response to the context. 

Example:

	[name]:
        type: input_user
        properties:
            text: [prompt]
            entities:
                entity1: [nlp_entity_name]
            log_json: true
            require_match: true
            error_text: [error_prompt]
        transitions:
            next_state: [next_state_name]
``text`` string containing prompt for user, **REQUIRED**

``entities`` this field contains entities to save to context, **REQUIRED**

> ``entity1`` context key, under which the value is saved,
> ``nlp_entity_name`` name of the entity in the nlp

``log_json`` true/false, determines if latest user response should be saved in context for later use

``require_match`` true/false, determines if entities from the entity field need to be present in order to continue
> *we recommend to use* ``require_match`` *only for matching single entity, for multiple entities sequence of conditional states is preferred*

``error_text`` text to display in case ``require_match`` is ``True`` and entities are missing

``next_state`` field contains name of the next state


Default property values:

* ``text``: *Your question here*
* ``log_json``: *false*
* ``require_match``: *false*
* ``error_text``: *Sorry I don’t understand. Please try again.*


### input_context
input_context from the last user response saved to context via ``log_json: true`` and loads its entities.

Example:

	[name]:
        type: input_context
        properties:
            entities:
                entity1: [nlp_entity_name]
        transitions:
            next_state: [next_state_name]
``entities`` this field contains entities to save to context, **REQUIRED**
> ``entity1`` context key under which the value is saved
> ``nlp_entity_name`` name of the entity in the nlp

``next_state`` field contains name of the next state



### conditional_equal
conditional_equal branches dialog according to the equality of two values.

Example:

	[name]:
        type: conditional_equal
        properties:
            value1: [val1]
            value2: [val2]
        transitions: 
            equal: [positive_case]
            notequal: [negative_case]
``value1`` field contains first value to compare, **REQUIRED**

``value2`` field contains second value to compare, **REQUIRED**

``equal`` field contains a name of state to transition into in case values are equal, **REQUIRED**

``notequal`` field contains a name of state to transition into in case values are NOT equal, **REQUIRED**

### conditional_exists
conditional_exists branches dialog according to the existence of a value in context.

Example:

	[name]:
        type: conditional_exists
        properties:
            key: '{{context_key}}'
        transitions: 
            exists: [positive_case]
            notexists: [negative_case]
``key`` contains a key to search for in context in special format, **REQUIRED**

``exists`` field contains a name of state to transition into in case key exists, **REQUIRED**

``notexists`` field contains a name of state to transition into in case the key does NOT exist, **REQUIRED**

### UserDefinedState
You can define our own state. Keep in mind, that the name of your state type should be the same as name of your class, defining the state.

from loggers import loggers
from nlp import *
from .state import State
from loaded_states import intent_transitions


class InputUser(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('User message: ' + request_data['text'], extra={'uid': request_data.get('session', False)})

        response = get_entities(request_data['text'])
        loggers.get(self.bot).get("state_logger").debug('NLP output: ' + str(response), extra={'uid': request_data.get('session', False)})


        # Log latest user response to context
        if self.properties['log_json']:
            request_data['context'].update({'latest': response})

        # Switch intent according to user response
        response_intent = response.get('intent', False)
        if response_intent:
            if intent_transitions.get(response_intent, False) and response_intent != request_data['context'].get('intent', False):
                loggers.get(self.bot).get("state_logger").debug('Switching intent: current intent: ' + str(request_data['context'].get('intent', False)) + ', user intent: ' + str(response_intent),
                                   extra={'uid': request_data.get('session', False)})
                loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                   extra={'uid': request_data.get('session', False)})
                request_data['context'].update(response)
                request_data.update({'next_state': intent_transitions.get(response_intent, False)})

                loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                   extra={'uid': request_data.get('session', False)})
                return request_data


        # Require entity match check
        if self.properties['require_match']:
            loggers.get(self.bot).get("state_logger").debug('Checking required entities: ' + str(self.properties.get('entities', False)), extra={'uid': request_data.get('session', False)})

            if self.check_response(response):
                loggers.get(self.bot).get("state_logger").debug('PASS',
                                   extra={'uid': request_data.get('session', False)})
                loggers.get(self.bot).get("state_logger").debug('Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
                                   extra={'uid': request_data.get('session', False)})
                self.update_context(request_data['context'], response)
                request_data.update({'next_state': self.transitions.get('match', False)})
                loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                   extra={'uid': request_data.get('session', False)})
                loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                   extra={'uid': request_data.get('session', False)})

                return request_data

            else:
                loggers.get(self.bot).get("state_logger").debug('FAIL',
                                   extra={'uid': request_data.get('session', False)})
                request_data.update({'next_state': self.transitions.get('notmatch', False)})
                loggers.get(self.bot).get("state_logger").debug('Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
                                   extra={'uid': request_data.get('session', False)})
                self.update_context(request_data['context'], response)
                loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                   extra={'uid': request_data.get('session', False)})
                loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                   extra={'uid': request_data.get('session', False)})

                return request_data
        loggers.get(self.bot).get("state_logger").debug(
            'Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
            extra={'uid': request_data.get('session', False)})
        self.update_context(request_data['context'], response)
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')), extra={'uid': request_data.get('session', False)})

        return request_data

    def check_response(self, response):  # Checks if all required entities are present
        for entity in self.properties['entities']:
            if self.properties['entities'][entity]in response:
                pass
            else:
                return False
        return True



class InputContext(State):
    def execute(self, request_data) -> dict:
        loggers.get(self.bot).get("state_logger").debug('Executing state: ' + str(self), extra={'uid': request_data.get('session', False)})

        response = request_data['context'].get('latest', {})
        loggers.get(self.bot).get("state_logger").debug('Latest user message: ' + str(response), extra={'uid': request_data.get('session', False)})

        # Switch intent according to user response
        response_intent = response.get('intent', False)
        if response_intent:
            if intent_transitions.get(response_intent, False) and response_intent != request_data['context'].get('intent', False):
                loggers.get(self.bot).get("state_logger").debug('Switching intent: current intent: ' + str(request_data['context'].get('intent', False)) + ', user intent: ' + str(response_intent),
                                   extra={'uid': request_data.get('session', False)})
                loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.',
                                   extra={'uid': request_data.get('session', False)})
                request_data['context'].update(response)
                request_data.update({'next_state': intent_transitions.get(response_intent, False)})

                loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')),
                                   extra={'uid': request_data.get('session', False)})
                return request_data

        loggers.get(self.bot).get("state_logger").debug(
            'Updating context...\rContext: ' + str(request_data.get('context', False)) + '\rUpdate: ' + str(response),
            extra={'uid': request_data.get('session', False)})
        self.update_context(request_data['context'], response)
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        loggers.get(self.bot).get("state_logger").debug('State ' + self.name + ' complete.', extra={'uid': request_data.get('session', False)})
        loggers.get(self.bot).get("state_logger").debug('Next state: ' + str(request_data.get('next_state')), extra={'uid': request_data.get('session', False)})

        return request_data

class EntityRecognizer(State):
"""
requires:
link to czech-morfflex-160310.dict: https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1674
phone_brands.txt are in slack chat
pip install ufal.morphodita

possible alternatives to a lemmatizer would be edit distance
"""
    def load_entity_dict(self, filename="phone_brands.txt"):
        self.entity_dict = set()
        with open(filename) as f:
            for line in f:
                self.entity_dict.add(line.strip().lower())

    def init_lemmatizer(self, morph_filename="czech-morfflex-160310.dict"):
        from ufal.morphodita import *
        self.morpho = Morpho.load(morph_filename)

    def lemmatize(self, token):
        lemmas = TaggedLemmas() # container for the result
        result = self.morpho.analyze(token, morpho.GUESSER, lemmas) # result is int
        if result != 0: 
            # sometimes uppercasing the first character helps
            result = self.morpho.analyze(token.title(), morpho.GUESSER, lemmas)
        return morpho.rawLemma(lemmas[0].lemma)

    def find_entity(self, token):
        lemma = self.lemmatize(token)
        if lemma in self.entity_dict:
            return lemma
        elif token in self.entity_dict:
            return token
        else:
            return ""

    def tokenize(self, sentence):
        return (tok.lower() for tok in sentence.split(" ")) # generator

    def execute(self, request_data) -> dict:
        sentence = request_data['text']
        sentence_tokenized = self.tokenize(sentence)
        found_entities = []
        for token in sentence_tokenized:
            entity = self.find_entity(token)
            if entity != "":
                # should log this
                found_entities.append(entity)
        request_data.update({'response' : found_entities, 'next_state': self.transitions.get('next_state', False)})
        return request_data

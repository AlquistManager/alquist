from config import config
import requests

wit_client = None
lemma_class = None


def get_entities(text, nlp_type): #get_entities(text, nlp_type="lemma")
    if nlp_type is None:
        nlp_type = "empty"

    ent_out = {}
    if nlp_type == "wit":
        global wit_client
        if wit_client is None:
            wit_client = WitClient()
        else:
            ent_out = wit_client.get_entities(text)
    elif nlp_type == "lemma":
        global lemma_class
        if lemma_class is None:
            lemma_class = Lemma()
        else:
            ent_out = lemma_class.get_entities(text)
    elif nlp_type == "empty":
        ent_out.update({'raw_text': str(text)})
    elif nlp_type == "tfidf":
        req = requests.post("http://127.0.0.1:5678/", json={'text': text})
        print(req.json()['command'])
        ent_out.update({'intent': req.json()['command']})
    return ent_out


class WitClient:
    client = None

    def __init__(self):
        from wit import Wit

        access_token = config["wit_token"]
        actions = {}
        global client
        client = Wit(access_token, actions)

    def get_entities(self, text):
        ent_out = {}
        if not text == "":
            resp = client.message(text)
            for key in resp['entities']:
                if resp['entities'][key][0]['confidence'] > 0:
                    ent_out.update({key: resp['entities'][key][0]['value']})
            intent = resp.get('intent', False)
            if intent:
                if intent[0]['confidence'] > 0:
                    ent_out.update({'intent': intent[0]['value']})
        return ent_out


class Lemma:
    entity_dict = None
    morpho = None

    def __init__(self):
        import json
        from ufal.morphodita import Morpho
        import glob

        def load_entity_dict(filenames):
            result_dict = {}
            for filename in filenames:
                ent = json.load(open(filename))
                ent_type = ent['entity-type']
                result_dict.update({entity: ent_type for entity in ent['entities']})
                # entity overlap
            return result_dict

        def init_lemmatizer(morph_filename="czech-morfflex-160310.dict"):
            return Morpho.load(morph_filename)


        global entity_dict
        global morpho
        entity_dict = load_entity_dict(glob.glob('./modules/nlp/*.json'))
        morpho = init_lemmatizer()

    def lemmatize(self, token):
        from ufal.morphodita import TaggedLemmas
        lemmas = TaggedLemmas()  # container for the result
        result = morpho.analyze(token, morpho.GUESSER, lemmas)  # result is int
        if result != 0:
            # sometimes uppercasing the first character helps
            result = morpho.analyze(token.title(), morpho.GUESSER, lemmas)
        return morpho.rawLemma(lemmas[0].lemma).lower()

    def tokenize(self, sentence):
        return (tok.lower() for tok in sentence.split(" "))  # generator

    def find_entity(self, token):
        lemma = self.lemmatize(token)
        if lemma in entity_dict:
            return entity_dict[lemma], lemma
        elif token in entity_dict:
            return entity_dict[token], token
        else:
            return "", ""

    def get_entities(self, text):
        ent_out = {}
        tokens = self.tokenize(text)
        for token in tokens:
            entity = self.find_entity(token)
            if entity[0] != "":
                ent_out.update({entity[0]: entity[1]})
        return ent_out

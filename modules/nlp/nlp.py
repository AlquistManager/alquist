from config import config

nlp_type = config["nlp_type"]

if nlp_type == "lemma":
    import json
    from ufal.morphodita import *
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


    entity_dict = load_entity_dict(glob.glob('./modules/nlp/*.json'))
    morpho = init_lemmatizer()

elif nlp_type == "wit":
    from wit import Wit

    access_token = config["wit_token"]
    actions = {}
    client = Wit(access_token, actions)


def lemmatize(token):
    lemmas = TaggedLemmas() # container for the result
    result = morpho.analyze(token, morpho.GUESSER, lemmas) # result is int
    if result != 0: 
        # sometimes uppercasing the first character helps
        result = morpho.analyze(token.title(), morpho.GUESSER, lemmas)
    return morpho.rawLemma(lemmas[0].lemma).lower()


def tokenize(sentence):
    return (tok.lower() for tok in sentence.split(" ")) # generator


def find_entity(token):
    lemma = lemmatize(token)
    if lemma in entity_dict:
        return entity_dict[lemma], lemma
    elif token in entity_dict:
        return entity_dict[token], token
    else:
        return "", ""


def get_entities(text, nlp_type="lemma"):
    ent_out = {}
    if nlp_type=="wit":
        if not text == "":
            resp = client.message(text)
            for key in resp['entities']:
                if resp['entities'][key][0]['confidence'] > 0:
                    ent_out.update({key: resp['entities'][key][0]['value']})
            intent = resp.get('intent', False)
            if intent:
                if intent[0]['confidence'] > 0:
                    ent_out.update({'intent': intent[0]['value']})
    elif nlp_type=="lemma":
        tokens = tokenize(text)
        for token in tokens:
            entity = find_entity(token)
            if entity[0] != "":
                ent_out.update({entity[0]: entity[1]})
    return ent_out



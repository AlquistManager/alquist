from yaml_parser.yaml_parser import YamlParser
import solver
import loaded_states

YamlParser()
request_data = {"context": {}, "state_name": "init", "text": ''}
while request_data.get('state_name')!="END":
    request_data = solver.process_request(request_data.get('state_name'), request_data.get('context'), request_data.get('text'), "TEST")
    request_data['state_name'] = request_data['next_state']
    print(request_data)
    if request_data.get('next_state') != 'END' and str(loaded_states.state_dict['states'][request_data.get('next_state')]['type'])==str('<class \'states.user_input.InputUser\'>'):
        request_data['text'] = input()


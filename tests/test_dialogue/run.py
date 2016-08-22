from yaml_parser.yaml_parser import YamlParser
import solver

YamlParser()
request_data = {"context": {}, "state_name": "init", "text": ''}
while request_data.get('state_name')!="END":
    request_data = solver.process_request(request_data.get('state_name'), request_data.get('context'), request_data.get('text'))
    request_data['state_name'] = request_data['next_state']
    print(request_data)
    if request_data.get('state_name')!="END":
        request_data['text'] = input()


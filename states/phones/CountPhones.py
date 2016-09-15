import requests
import ast
from states.state import State
import re




class CountPhones(State):
    # execute state
    def execute(self, request_data) -> dict:
        # load context
        context = request_data.get('context', {})
        query = """
            PREFIX : <http://54.186.96.246/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>

            Select (COUNT(?phone) AS ?count)
            WHERE {
              ?phone :name ?name .
              ?phone :ratingValue ?p .
              ?phone a :MobilePhone .
              """
        phone_type = context.get('phone_type', False)
        if phone_type:
            if phone_type == 'smart':
                query = query + "?phone a :SmartPhone .\n"
            elif phone_type == 'simple':
                query = query + "?phone a :BasicPhone .\n"
            elif phone_type == 'senior':
                query = query + "?phone a :SeniorsPhone .\n"


        phone_os = context.get('phone_os', False)
        if phone_os:
            if phone_os == 'android':
                query = query + "?phone :platform ?platform .\nfilter( ?platform = :Google_Android ) .\n"
            elif phone_os == 'all':
                pass
            elif phone_os == 'win':
                query = query + "?phone :platform ?platform .\nfilter( ?platform = :Windows_Phone ) .\n"
            elif phone_os == 'iOS':
                query = query + "?phone :platform ?platform .\nfilter( ?platform = :Apple_IOS ) .\n"

        brand = context.get('brand', False)
        if brand:
            query = query + "?phone :brand ?brand .\n"
            query = query + "filter( ?brand = :" + brand.upper() + " ) .\n"


        query = query + "?phone :price ?price .\n"
        price_from = context.get('price_from', False)
        if price_from:
            query = query + "filter( ?price >= " + price_from + " ) .\n"

        price_to = context.get('price_to', False)
        if price_to:
            query = query + "filter( ?price <= " + price_to + " ) .\n"

        display_size = context.get('display_size', False)
        if display_size:
            query = query + "?phone :displaySize ?displaySize .\n"
            if display_size == '3.4 - 5':
                query = query + "filter( ?displaySize >= 3.4 ) .\nfilter( ?displaySize < 5 ) .\n"
            elif display_size == 'any':
                pass
            elif display_size == '3.4':
                query = query + "filter( ?displaySize <= 3.4 ) .\n"
            elif display_size == '5+':
                query = query + "filter( ?displaySize >= 5 ) .\n"
            else:
                query = query + "filter( ?displaySize >= " + display_size + " ) .\n"

        processor = context.get('processor', False)
        if processor:
            query = query + "?phone :processor ?processor .\n?processor :processorFrequency ?value .\n"
            if processor == 'strong':
                query = query + "filter( ?value >= 1.5 ) .\n"
            elif processor == 'any':
                pass
            else:
                query = query + "filter( ?value >= " + processor + " ) .\n"

        ram = context.get('ram', False)
        if ram:
            query = query + "?phone :ramSize ?ram .\n"
            if ram == '2 gb':
                query = query + "filter( ?ram >= 2 ) .\n"
            elif ram == 'any':
                pass
            else:
                query = query + "filter( ?ram >= " + ram + " ) .\n"

        memory = context.get('memory', False)
        if memory:
            query = query + "?phone :storageSize ?storage .\n"
            if memory == '0 - 8 GB':
                query = query + "filter( ?storage <= 8 ) .\n"
            elif memory == '8+ GB':
                query = query + "filter( ?storage >= 8 ) .\n"
            elif memory == 'memory card':
                query = query + "?phone :memoryCardSlot ?mc .\n"
            elif memory == 'any':
                pass
            else:
                query = query + "filter( ?storage >= " + memory + " ) .\n"


        resolution = context.get('resolution', False)

        if resolution:
            p = re.compile('\S*')
            resolution = re.search(p, resolution)
            query = query + "?phone :pixelResolutionWidth ?res .\n"
            if resolution == 'any':
                pass
            else:
                query = query + "filter( ?res >= " + resolution.group(0) + " ) .\n"

        url = "http://54.186.96.246:3030/AlzaPhones/sparql"
        query = query + "}"
        r = requests.post(url, data={"query": query})

        results = ast.literal_eval(r.text)['results']['bindings'][0]['count']['value']
        request_data['context'].update({'phone_count': results})
        print(r.text)
        print(query)

        # load next state
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data

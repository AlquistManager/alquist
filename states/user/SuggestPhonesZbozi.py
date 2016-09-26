import requests
import ast
from states.state import State
import re


class SuggestPhones(State):
    # execute state
    def execute(self, request_data) -> dict:
        # load context
        context = request_data.get('context', {})
        query = "http://www.zbozi.cz/api/v1/search?categoryLoadOffers=1&" \
                "categoryPath=telefony-navigace%2Fmobilni-telefony&forceListProductsAndOffers=1&groupByCategory=0&" \
                "loadTopProducts=false&page=1"
        phone_type = context.get('phone_type', False)
        if phone_type:
            if phone_type == 'smart':
                pass
            elif phone_type == 'simple':
                query += "&operacni-system=bez-operacniho-systemu"
            elif phone_type == 'senior':
                query += "&pro-seniory=ano"
            elif phone_type == 'all':
                pass

        phone_os = context.get('phone_os', False)
        if phone_os:
            if phone_os == 'android':
                query += "&operacni-system=android-6-0,android-5-1,android-5-0,android-4-4,android-4-3,android-4-2," \
                         "android-4-1,android-4-0,android-2-x,android-1-x"
            elif phone_os == 'all':
                pass
            elif phone_os == 'win':
                query += "&operacni-system=wp-7-x,wp-8-x,windows-10,windows-10-mobile,windows-8-1"
            elif phone_os == 'iOS':
                query += "&operacni-system=ios"

        brand = context.get('brand', False)
        if brand and brand.upper() != 'SKIP':
            query += "&vyrobce=" + brand

        query = query + "?phone :price ?price .\n"
        price_from = context.get('price_from', False)
        price_to = context.get('price_to', False)
        price = context.get('price', False)
        trait_price = context.get('trait_price', False)
        if price_from and price_to:
            query += "&minPrice=" + price_from.replace(" ", "")
            query += "&maxPrice=" + price_to.replace(" ", "")

        elif trait_price:
            if trait_price == 'price_from':
                if price:
                    query += "&minPrice=" + price.replace(" ", "")
                elif price_from:
                    query += "&minPrice=" + price_from.replace(" ", "")
                elif price_to:
                    query += "&maxPrice=" + price_to.replace(" ", "")
            elif trait_price == 'price_to':
                if price:
                    query += "&maxPrice=" + price.replace(" ", "")
                elif price_to:
                    query += "&maxPrice=" + price_to.replace(" ", "")
                elif price_from:
                    query += "&minPrice=" + price_from.replace(" ", "")
            elif trait_price == 'price_around':
                if price:
                    query += "&minPrice=" + str(int(price.replace(" ", "")) - 500)
                    query += "&maxPrice=" + str(int(price.replace(" ", "")) + 500)

                elif price_to:
                    query += "&minPrice=" + str(int(price_to.replace(" ", "")) - 500)
                    query += "&maxPrice=" + str(int(price_to.replace(" ", "")) + 500)

                elif price_from:
                    query += "&minPrice=" + str(int(price_from.replace(" ", "")) - 500)
                    query += "&maxPrice=" + str(int(price_from.replace(" ", "")) + 500)
        elif price_from:
            query += "&minPrice=" + price_from.replace(" ", "")
        elif price_to:
            query += "&maxPrice=" + price_to.replace(" ", "")
        elif price:
            query += "&minPrice=" + str(int(price.replace(" ", "")) - 500)
            query += "&maxPrice=" + str(int(price.replace(" ", "")) + 500)

        display_size = context.get('display_size', False)
        if display_size:
            if display_size == '3.4 - 5':
                query += "&uhlopricka-displeje-od=3.4&uhlopricka-displeje-do=5.0"
            elif display_size == 'any':
                pass
            elif display_size == '3.4':
                query += "&uhlopricka-displeje-do=3.4"
            elif display_size == '5+':
                query += "&uhlopricka-displeje-od=5.0"
            else:
                query += "&uhlopricka-displeje-od="+display_size

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
                query = query + "filter( ?res >= " + resolution.group(0).replace(" ", "") + " ) .\n"

        url = "http://54.186.96.246:3030/AlzaPhones/sparql"
        query = query + """}
                    order by desc(?p)
                    limit 5"""
        r = requests.post(url, data={"query": query})
        phones = []
        results = ast.literal_eval(r.text)['results']['bindings']
        # for result in results:
        #     tmp = result['name']['value']
        #     if tmp:
        #         phones.append(tmp)
        # request_data['context'].update({'suggested_phones': phones})
        print(query)
        # TMP
        i = 1
        for result in results:
            tmp = result['phone']['value']
            if tmp:
                request_data['context'].update({'suggested_phones_' + str(i): tmp.replace("www", "m")})
                i += 1

        # load next state
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data

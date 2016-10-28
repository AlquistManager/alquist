import urllib.parse

import requests
from states.state import State
import re


class SuggestPhonesZbozi(State):
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
            query += "&vyrobce=" + brand.lower()

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
                query += "&uhlopricka-displeje-od=" + display_size

        processor = context.get('processor', False)
        if processor:
            if processor == 'strong':
                query += "&frekvence-procesoru-od=1.5"
            elif processor == 'any':
                pass
            else:
                query += "&frekvence-procesoru-od=" + processor

        ram = context.get('ram', False)
        if ram:
            if ram == '2 gb':
                query += "&operacni-pamet-od=2048"
            elif ram == 'any':
                pass
            else:
                query += "&operacni-pamet-od=" + ram

        memory = context.get('memory', False)
        if memory:
            if memory == '8 - 16 GB':
                query += "&interni-pamet-od=8"
                query += "&interni-pamet-do=16"
            elif memory == '16+ GB':
                query += "&interni-pamet-od=16"
            elif memory == 'memory card':
                query += "?phone :memoryCardSlot ?mc .\n"
            elif memory == 'any':
                pass
            else:
                query += "&slot-na-pametovou-kartu=ano"

        resolution = context.get('resolution', False)

        if resolution:
            p = re.compile('\S*')
            resolution = re.search(p, resolution)
            resolution = re.split('x', resolution.group(0))
            width = resolution[0]
            if resolution == 'any':
                pass
            elif width >= 1920:
                query += "&rozliseni=2048-x-1152-qwxga,1920-x-1080-fhd,2-592-x-1944,2048-x-1536-qxga,2560-x-1080," \
                         "2560-x-1440-wqhd,3200-x-1800-wqxgaplus,3840-x-2160-uhd-4k"
            elif width >= 1280:
                query += "&rozliseni=2048-x-1152-qwxga,1920-x-1080-fhd,2-592-x-1944,2048-x-1536-qxga,2560-x-1080," \
                         "2560-x-1440-wqhd,3200-x-1800-wqxgaplus,3840-x-2160-uhd-4k,1280-x-720-hd-wxga,1280-x-768-wxga," \
                         "1280-x-800-wxga,1334-x-750,1366-x-768-wxga,1600-x-1200-uxga"

        r = requests.get(query)
        results = r.json()
        products = results['categories'][0]['products']
        i = 1
        if phone_os == 'iOS':
            m_name = "Apple iPhone " + context.get('generation', False)
            if context.get('model', False)=='plus':
                m_name += " Plus"
            if context.get('model', False)=='C':
                m_name = "Apple iPhone 5C"
            print(m_name)


            for product in products:
                print(product['displayName'])
                if product['displayName'] == m_name:
                    url = "https://alquistmanager.github.io/alquist-tel-result/?"
                    url += "price=" + urllib.parse.quote(str(int(product['minPrice'] / 100)))
                    url += "&name=" + urllib.parse.quote(product['displayName'])
                    url += "&image=" + "https:" + product['images'][0]['imageUrl']
                    url += "&url=" + "https://www.zbozi.cz/vyrobek/" + product['normalizedName'] + "/"
                    url += "&param0=" + urllib.parse.quote(product['parameters'][0]['displayName'] + " " + product['parameters'][0]['values'][0][
                        'displayValue'] + product['parameters'][0]['values'][0]['displayUnit'])
                    url += "&param1=" + urllib.parse.quote(product['parameters'][1]['displayName'] + " " + product['parameters'][1]['values'][0][
                        'displayValue'] + product['parameters'][1]['values'][0]['displayUnit'])
                    url += "&param2=" + urllib.parse.quote(product['parameters'][2]['displayName'] + " " + product['parameters'][2]['values'][0][
                        'displayValue'] + product['parameters'][2]['values'][0]['displayUnit'])
                    request_data['context'].update(
                        {'suggested_phones_' + str(i): url})
                    i += 1
        else:
            for product in products:
                if i > 5:
                    break
                url = "https://alquistmanager.github.io/alquist-tel-result/?"
                url += "price=" + urllib.parse.quote(str(int(product['minPrice'] / 100)))
                url += "&name=" + urllib.parse.quote(product['displayName'])
                url += "&image=" + "https:" + product['images'][0]['imageUrl']
                url += "&url=" + "https://www.zbozi.cz/vyrobek/" + product['normalizedName'] + "/"
                url += "&param0=" + urllib.parse.quote(product['parameters'][0]['displayName'] + " " + product['parameters'][0]['values'][0][
                    'displayValue'] + product['parameters'][0]['values'][0]['displayUnit'])
                url += "&param1=" + urllib.parse.quote(product['parameters'][1]['displayName'] + " " + product['parameters'][1]['values'][0][
                    'displayValue'] + product['parameters'][1]['values'][0]['displayUnit'])
                url += "&param2=" + urllib.parse.quote(product['parameters'][2]['displayName'] + " " + product['parameters'][2]['values'][0][
                    'displayValue'] + product['parameters'][2]['values'][0]['displayUnit'])
                request_data['context'].update(
                    {'suggested_phones_' + str(i): url})
                i += 1

        # load next state
        request_data.update({'next_state': self.transitions.get('next_state', False)})
        return request_data

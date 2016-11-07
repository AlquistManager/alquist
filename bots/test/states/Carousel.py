import urllib.parse

import requests
from states.state import State
import re


class Carousel(State):
    # execute state
    def execute(self, request_data) -> dict:
        # load context
        context = request_data.get('context', {})
        sugested_url_one = context.get('suggested_phones_1')
        sugested_url_two = context.get('suggested_phones_2')
        sugested_url_three = context.get('suggested_phones_3')
        sugested_url_four = context.get('suggested_phones_4')
        sugested_url_five = context.get('suggested_phones_5')
        #sugested_url_one = "https://alquistmanager.github.io/alquist-tel-result/?price=5950&name=Huawei%20P9%20Lite%20Dual%20SIM&image=https://d25-a.sdn.szn.cz/d_25/c_B_b/SkQBKgt.png&url=https://www.zbozi.cz/vyrobek/huawei-p9-lite-dual-sim/&param0=opera%C4%8Dn%C3%AD%20syst%C3%A9m%20Android%206.0&param1=%C3%BAhlop%C5%99%C3%AD%C4%8Dka%20displeje%205.2%22&param2=rozli%C5%A1en%C3%AD%20%201920%20x%201080%20%28FHD%29"
        #sugested_url_two = "https://alquistmanager.github.io/alquist-tel-result/?price=5000&name=Huawei%20P8%20Lite%20Dual%20SIM&image=https://d25-a.sdn.szn.cz/d_25/d_15051451/img/29/275x279_h1xIyd.jpg&url=https://www.zbozi.cz/vyrobek/huawei-p8-lite-dual-sim/&param0=opera%C4%8Dn%C3%AD%20syst%C3%A9m%20Android%205.0&param1=%C3%BAhlop%C5%99%C3%AD%C4%8Dka%20displeje%205%22&param2=technologie%20displeje%20IPS%20LCD"
        #sugested_url_three = "https://alquistmanager.github.io/alquist-tel-result/?price=5347&name=Samsung%20Galaxy%20A3%20%28A310F%29&image=https://d25-a.sdn.szn.cz/d_25/d_16021298/img/1/399x809_MeHsM3.jpg&url=https://www.zbozi.cz/vyrobek/samsung-galaxy-a3-a310f/&param0=opera%C4%8Dn%C3%AD%20syst%C3%A9m%20Android%205.1&param1=%C3%BAhlop%C5%99%C3%AD%C4%8Dka%20displeje%204.7%22&param2=jemnost%20displeje%20312ppi"
        #sugested_url_four = "https://alquistmanager.github.io/alquist-tel-result/?price=5000&name=Huawei%20Y6%20II&image=https://d25-a.sdn.szn.cz/d_25/c_C_BF/33KNdq.jpeg&url=https://www.zbozi.cz/vyrobek/huawei-y6-ii/&param0=opera%C4%8Dn%C3%AD%20syst%C3%A9m%20Android%206.0&param1=%C3%BAhlop%C5%99%C3%AD%C4%8Dka%20displeje%205.5%22&param2=jemnost%20displeje%20267ppi"
        #sugested_url_five = "https://alquistmanager.github.io/alquist-tel-result/?price=9600&name=Samsung%20Galaxy%20S6%20%28G920F%29&image=https://d25-a.sdn.szn.cz/d_25/d_15082836/img/82/176x470_i3Jk6_.jpg&url=https://www.zbozi.cz/vyrobek/samsung-galaxy-s6-g920f/&param0=opera%C4%8Dn%C3%AD%20syst%C3%A9m%20Android%205.0&param1=%C3%BAhlop%C5%99%C3%AD%C4%8Dka%20displeje%205.1%22&param2=technologie%20displeje%20Quad%20HD%20Super%20AMOLED"
        old_response = request_data.get('response', False)

        phone_one = '<div style="position:absolute; z-index:-1; width:inherit;"><iframe src="' + sugested_url_one + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>'
        phone_two = '<div style="position:absolute; z-index:-1;width:inherit;"><iframe src="' + sugested_url_two + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>'
        phone_three = '<div style="position:absolute; z-index:-1;width:inherit;"><iframe src="' + sugested_url_three + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>'
        phone_four = '<div style="position:absolute; z-index:-1;width:inherit;"><iframe src="' + sugested_url_four + '" height="600px" style="width:inherit; border-color:gray;border-style:solid;" scrolling="no"></iframe></div>'
        phone_five = '<div style="position:absolute; z-index:-1;width:inherit;"><iframe src="' + sugested_url_five + '" height="600px" style="width:inherit; border-color:gray; border-style:solid;" scrolling="no"></iframe></div>'

        message = {'type': 'carousel', 'payload': {'parts': [phone_one, phone_two, phone_three, phone_four, phone_five],
                                                   'urls': ["http://seznam.cz", "http://seznam.cz", "http://seznam.cz",
                                                            "http://seznam.cz", "http://seznam.cz"]}}

        if old_response:
            old_response.append(message)
        else:
            old_response = [message]

        request_data.update({'response': old_response, 'next_state': self.transitions.get('next_state', False)})

        # load next state
        return request_data

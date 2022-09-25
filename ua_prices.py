import requests
from typing import List, Dict


class United_Air:
    def __init__(self, flight_number: str, origin_airport: str, destination_airport: str, date_str :str) -> None:
        self.flight_number = flight_number
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.date_str = date_str
        self.list_of_prices_and_codes = []
        self.headers = {
            'authority': 'www.united.com',
            'accept': 'application/json',
            'accept-language': 'en-US',
            'cache-control': 'no-cache',
            # Requests sorts cookies= alphabetically
            # 'cookie': f"newHP=true; bm_sz=1280B41A68E3C41B012CDA912B61A512~YAAQJfV0aGT0bQCDAQAACKlAOxHg5UvKaY3Tibcx6Z5HgQNhdaP1cdJplUe2lJ82/o3ynmrE7icp/DkO3ZQH2Q2aCIWHK3S+Fp37qmU+sCI0C3OGXR1N+4ZRu9oSphBFASnXbu1LA1McpShP2iDh1q2dJ7kIalPw1txy6OT+tR9kV1wMoxZzGw8ZnGoiY5SY8umZcAJUUyyMIbVehsAW82T8RqpRkzjXQJOdkEXpfY0ruGXmNynXiDUR8UCD0RD+MPqrr2fYqBYthLdAEoNIrb8hHJcdkCAFTqMnaqq3ctrzbjw=~3487544~4342342; akacd_NS_AB=3840599235~rv=64~id=795e546c74463f81606d3660a6a144d7; PROrigin=origin_a; optimizely_id=1663146441.63672081; ak_bmsc=223C40F794CCF2CE482575008852972B~000000000000000000000000000000~YAAQJfV0aDr1bQCDAQAANNtAOxEeFkELrsfG5FEyXyRrD+9TFOEBa2PAcdN+vk3y/y70CsvptDNSTvwOvexQetBCN7+oLk7/428q2pCX1ylEOBk4uzCemFGrGAD2QiF7tJunWM6ctO+W+hhJFCW7VEQrnMhcoshV2Exkvrjd0iun6M8nb1cTx+Sd/H3KCN0fmjOa1Zv4S4j0YkPRmmtu2Hp/1EyDSa6Zjj5K11R6w3I7OJ+qdEgM2+sIZNtEbU0hFQ4ADHbXWk1iVu4nQBe63z/LE8x6nVPeeRVTGwBy4HdYfUjVZ6Dr7XxPlkwYiVaGtEXFkqQ+264kqYbSQ1LQkK4+uRPVAdmvsW4aJh8aVwmzw9nxR9sSodiO0cpHqcfBVl+/e0Df7RRp7Nf0O9Z/4Y4KUEY2TKlTEhnZgrkBoXhcSogyk+FFqPTF2JW6IFcIdvB+Mgl/hVpeyksDuVdO/tZdLLvkmSlvLiHL1x1hp4dR/4mHnd5+N75AgQ==; akacd_ABdeployment=3840599248~rv=94~id=e37e182c41f311dac4236853ab1b4dd2; QuantumMetricSessionID=0aacafe81b0a620da3b26afaf179ed43; QuantumMetricUserID=d7b3b83f2b4d641c40e85912fab4f978; LPVID=FkYTI4ODM2ZDFkMGFhZmM2; LPSID-84608747=TFRdEX_jSjeP8xnD6ggdfw; _abck=6AC9B8230B7B92B2B9960F040023D8DC~0~YAAQJfV0aE/8bQCDAQAAZXNCOwj1KFPM6aqtMVE2kAkYc2qBC5IP10zS4OzNPF58BIuEgKe+PJJ7e87EYXijFoeMUqCJuejgrKtWI6ALJO89qkoqCYBd/ZXbDWRwR8sU9i5SSRIpSdHyRe+huS+m4i+dmEZi3pWu+/4oI3zwtep/DKxuZo+ybT2YwLuQiakdk+kLbsGuJSRaKqehcb3o3p+ruz1dYst0AV+8s5QGHIwcc2uE54IGMP+6acxWvDMbZGzbByXE+cLamjKHdOmt/pvhRZEH9c6TiaeWaCUcKFYkE08Ff98DBJeUkdd2rp8dNKAWuzO5gAj7UqIDwJqstPCQFoHkFmsDCFh3k4Bx9BKXBLPLs4KEBD9Uws8itUwv915hKegWPxMX+0kErodMOtzXgQy6~-1~||-1||~-1; Locale=UMID=0fb2dff5-cfbb-475d-a379-ab2866e23cbd&Lang=en&POS=US; _pin_unauth=dWlkPVlqWTBabVJsTUdZdE1tRmlNUzAwTWpabUxXRTJORFl0TnpneE1UTXdZV014TldRMA; _tt_enable_cookie=1; _ttp=92414ebb-aff9-4b4c-a8dd-d4e3511f6ad1; ORA_FPC=id=2a9785c3-978f-4556-8c92-015e3dfe451e; WTPERSIST=; _gcl_au=1.1.1908695860.1663146934; Session=AuthToken=oJRTFASLhgJlNPbuxcJ%2f6bUcvgAn6CyJoCOn%2fqlLqkwQEgsEyaNsNzY%2bKd0h52%2b8S0r%2bjwuH35VFWzL7JqaJug%3d%3d; mmcore.tst=0.106; mmapi.store.p.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%22pd%22%3A%221694686642265%7C%5C%226JEtueLSRmSug1UsTRHZHOqxnyfZZK-Oy1DM6X4TTVc%3D%7CEwAAAApDH4sIAAAAAAAEAGNhcOKYU5Au5qfIwJxWlMgoxMDoxBAwc0kQE8PRvykeVtNuebwviZ1qAKQZgOA_FDCwuWQWpSaXMKaLMYHEwcBMnIEBhhkZVjozMsw7afvNL12MYe5zBgbWdLF0sf__WRgYGEGqGd9xMDNMzWdhYARp4YSYABR2BQCyFJEGkgAAAA%3D%3D%5C%22%22%2C%22bid%22%3A%221663151241887%7C%5C%22prodfracgus01%5C%22%22%2C%22srv%22%3A%221694686642277%7C%5C%22prodfracgus01%5C%22%22%7D%7D; mmapi.store.s.0=%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%7D%7D; utag_main=v_id:01833b40df48002377d19678bf0e05081001c0790086e{_sn:1$_se:383$_ss:0$_st:1663154633218$dc_visit:1$ses_id:1663146450762%3Bexp-session$_pn:11%3Bexp-session;} akavpau_ualwww=1663154125~id=f3bda3bea6cb709697e18d470fedb6c1; bm_sv=BF7F23AEE7AC7FB531CF523654DEF1AB~YAAQ5VCMT0NB3/KCAQAAP9OsOxHUFb5t3WnAaLUG3TJhJQGidYbLSirtVlrOHFhytWtK+C3WpuPYoBkEQ5+5RyUXjFevo5BT4nawcZcQQsMRaIEy3l1HM76HBobiXagtEmk1Uf91DGWJbsVstie1h1p9UNKkBYPX0rVt56gRUzQI6YmWjtXSa8IJevnStxbdfZzSP1kN+kEoRfHvPLJAi40TixQnFLl6uzKrGlG8PlAqOsiMxMtZTPjuLCAHoQ1uezo=~1",
            'pragma': 'no-cache',
            'referer': f'https://www.united.com/en/us/fsr/choose-flights?f={origin_airport}&t={destination_airport}&d={date_str}&r={date_str}&sc=7%2C7&st=bestmatches&cbm=-1&cbm2=-1&ft=0&cp=0&ct=0&cs=Y%2CB%2CM&px=1&taxng=1&clm=7&EditSearchCartId=DA38186E-58B2-4B04-A0D8-9B1FDC0581DD&tqp=R2',
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
        }

    def get_bearer_token(self) -> str:
        response = requests.get('https://www.united.com/api/token/anonymous', headers=self.headers).json()
        return response["data"]["token"]["hash"]

    def get_price_and_text(self, prices: list) -> str:
        r_price = ""
        r_tax = ""
        for price in prices:
            if price["PricingType"] == "Fare":
                r_price = price["Amount"]
            elif price["PricingType"] == "Taxes":
                r_tax = price["Amount"]
        return r_price, r_tax
                
            
    def get_flight_prices(self) -> List[Dict[str, str]]:
        token = self.get_bearer_token()
        copy_header = self.headers.copy()
        copy_header['x-authorization-api'] = f'bearer {token}'



        json_data = {
            'SearchTypeSelection': 1,
            'SortType': 'bestmatches',
            'SortTypeDescending': False,
            'Trips': [
                {
                    'Origin': f'{self.origin_airport}',
                    'Destination': f'{self.destination_airport}',
                    'DepartDate': f'{self.date_str}',
                    'Index': 1,
                    'TripIndex': 1,
                    'SearchRadiusMilesOrigin': '-1',
                    'SearchRadiusMilesDestination': '-1',
                    'DepartTimeApprox': 0,
                    'SearchFiltersIn': {
                        'FareFamily': 'ECONOMY',
                        'AirportsStop': None,
                        'AirportsStopToAvoid': None,
                        'StopCountMin': 0,
                        'StopCountMax': 0,
                    },
                },
            ],
            'CabinPreferenceMain': 'economy',
            'PaxInfoList': [
                {
                    'PaxType': 1,
                },
            ],
            'AwardTravel': False,
            'NGRP': False,
            'BookingCodesSpecified': 'Y,B,M',
            'ClassofService': 'Y,B,M',
            'CalendarLengthOfStay': 0,
            'PetCount': 0,
            'RecentSearchKey': 'LGALAX11/19/2022',
            'CalendarFilters': {
                'Filters': {
                    'PriceScheduleOptions': {
                        'Stops': 0,
                    },
                },
            },
            'Characteristics': [
                {
                    'Code': 'SOFT_LOGGED_IN',
                    'Value': False,
                },
                {
                    'Code': 'UsePassedCartId',
                    'Value': False,
                },
            ],
            'FareType': 'Refundable',
        }
        response = requests.post('https://www.united.com/api/flight/FetchFlights', headers=copy_header, json=json_data).json()
        trips = response["data"]["Trips"]
       
        for trip in trips:
            flights = trip["Flights"]
            for flight in flights:
                if self.flight_number == flight["OperatingCarrier"] + flight["FlightNumber"] and len(flight["Connections"]) == 0:
                    products = flight["Products"]
                    for product in products:
                        if product["BookingCode"] != "":
                            price, tax = self.get_price_and_text(product["Prices"])
                            self.list_of_prices_and_codes.append({
                                "price": price,
                                "tax": tax,
                                "booking_class": product["BookingCode"],
                            })
                            
        return self.list_of_prices_and_codes



import requests
import json
from typing import List, Dict


class Ryan_Air:
    def __init__(self, flight_number: str, origin_airport: str, destination_airport: str, date_str :str) -> None:
        self.flight_number = flight_number
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.date_str = date_str
        self.list_of_prices_and_codes = []
        self.headers = {
        'authority': 'www.ryanair.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'fr-correlation-id=20a905b5-a14d-45b6-ad23-1a8cf0617128; rid=59626a30-585c-4afa-9f7a-10c91e01a4cc; rid.sig=OCBtG/WF9HO7H4S44kdr0dQ68UsPvQb5Cn+VjU077lbP0LXI1IuqdqPDi+HdQnI6pxoiHvk/68BgcxyVX/1shxHUHhK7deVBDaQ9C+0qYUHNBb2H9zRo2DWUQf207xz88MqzxpO0TFvcV+YK3Iiu2KppooVZJWjMo4nIeBoInzcVJa+OL4xnAouHtOt+b/4YuSDOy6H/26YyCQdwOeKINDe+kaqzeIJ4afLD7jjGoG8CLmymbUcUgAzNq/0ZHA0WVNZWGn3rJAGkrLitgFNX0R/V1DVo0qbusUzpg/Xi1tY=; myRyanairID=; STORAGE_PREFERENCES={"STRICTLY_NECESSARY":true,"PERFORMANCE":true,"FUNCTIONAL":true,"TARGETING":true,"SOCIAL_MEDIA":true,"PIXEL":true,"GANALYTICS":true,"__VERSION":2}; RY_COOKIE_CONSENT=true; bid_FRwdAp7a9G2cnLnTsgyBNeduseKcPcRy=700a13e3-d50f-44fe-b334-f6df3fa03588; mkt=/us/en/; RYANSESSION=YyM5tAqhAv0AAAuXjHYAAAAI; agso=ARZJtHYBAOkvT3Aol9pIOm5db37EwFY.; agsd=ZEJwi6RBP_PNdiAtj_QEeUvDjPIZw5UH10bDyP7cB6VpnIxz; agsn=-GoPnX_yEjPZQOHKiKRrGUvTF_iG2PU9rMpDzKTiU4s.; agssn=AUzsyhQBAExOb9Ipl9pIGJH8LQ..; agsy=ASkLoMUBAAm9FH44l9pIZOB0qQ..',
        'pragma': 'no-cache',
        'referer': f'https://www.ryanair.com/us/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut={date_str}&dateIn=&isConnectedFlight=false&isReturn=false&discount=0&promoCode=&originIata={origin_airport}&destinationIata={destination_airport}&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate={date_str}&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata={origin_airport}&tpDestinationIata={destination_airport}',
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
        }


    def get_price_and_code(self, flight_key: str, outbound_fare_key: str) -> str:
        response = requests.get(f'https://www.ryanair.com/api/booking/v5/en-us/FareOptions?OutboundFlightKey={flight_key}&OutboundFareKey={outbound_fare_key}&AdultsCount=1&ChildrenCount=0&InfantCount=0&TeensCount=0', headers=self.headers).json()
        return [(price["total"], price["code"]) for price in response]
            

    def get_flight_prices(self) -> List[Dict[str, str]]:   
        params = {
            'ADT': '1',
            'CHD': '0',
            'DateIn': '',
            'DateOut': f'{self.date_str}',
            'Destination': f'{self.destination_airport}',
            'Disc': '0',
            'INF': '0',
            'Origin': f'{self.origin_airport}',
            'TEEN': '0',
            'promoCode': '',
            'IncludeConnectingFlights': 'false',
            'FlexDaysBeforeOut': '2',
            'FlexDaysOut': '2',
            'FlexDaysBeforeIn': '2',
            'FlexDaysIn': '2',
            'RoundTrip': 'false',
            'ToUs': 'AGREED',
        }

        response = requests.get('https://www.ryanair.com/api/booking/v4/en-us/availability', params=params, headers=self.headers).json()

        trips = response["trips"]
        for trip in trips:
            dates = trip["dates"]
            for date in dates:
                if date["dateOut"][: len(self.date_str)] != self.date_str:
                    continue
                flights = date["flights"]
                for flight in flights:
                    if flight["flightNumber"].replace(" ", "") == self.flight_number:
                        fare = flight["regularFare"]
                        fare_class = fare["fareClass"]
                        for f in fare["fares"]:
                            if f["type"] == "ADT":
                                self.list_of_prices_and_codes.append(
                                    {
                                        "price" : f["publishedFare"],
                                        "booking_class" : fare_class,
                                        "code" : "VALUE"
                                    }
                                )  
                        price_codes = self.get_price_and_code(flight["flightKey"], fare["fareKey"])
                        for price_code in price_codes:
                            self.list_of_prices_and_codes.append(
                                {
                                    "price" : price_code[0],
                                    "booking_class" : fare_class,
                                    "code" : price_code[1]
                                }
                            )

        return self.list_of_prices_and_codes



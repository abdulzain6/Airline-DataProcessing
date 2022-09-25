from urllib.parse import urlencode
from bs4 import BeautifulSoup
from typing import List, Dict
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import contextlib, selenium, time


class SouthWest:
    def __init__(self, driver):
        self.driver = driver

    def safe_click(self, element):
        while True:
            with contextlib.suppress(selenium.common.exceptions.NoSuchElementException,selenium.common.exceptions.StaleElementReferenceException, selenium.common.exceptions.ElementNotInteractableException):
                element.click()
                return 
            time.sleep(0.5)

    def safe_find(self, by, by_what):
        while True:
            with contextlib.suppress(selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException):
                return self.driver.find_element(by, by_what)
            time.sleep(0.5)

    def make_url(self, src: str, dst: str, outDate: str) -> str:
        endpoint = "https://www.southwest.com/air/booking/select.html"

        context = {'adultPassengersCount': '1',
                'departureDate': outDate , #format '2019-02-04'
                'departureTimeOfDay': 'ALL_DAY',
                'destinationAirportCode': dst,
                'fareType': 'USD',
                'originationAirportCode': src,
                'passengerType': 'ADULT',
                'reset': 'true',
                'returnDate': "",
                'returnTimeOfDay': 'ALL_DAY',
                'seniorPassengersCount': '0',
                'tripType': 'oneway'}

        qstr = urlencode(context)
        return f"{endpoint}?int=HOMEQBOMAIR&{qstr}"


    def get_flight_prices(self, flight_number, origin_airport: str, destination_airport: str , datestr) -> List[Dict[str, str]]:
        list_of_prices_and_codes = []
        url = self.make_url(origin_airport, destination_airport, datestr)
        self.driver.get("https://www.southwest.com")
        self.driver.execute_script('window.sessionStorage.clear()')
        self.driver.execute_script('window.localStorage.clear()')
        time.sleep(5)
        self.driver.get(url)
        source = self.get_source()
        soup = BeautifulSoup(source, "html.parser")
        flights = soup.find_all("li", class_="air-booking-select-detail")
        for flight in flights:
            stops = flight.find("div", class_="flight-stops-badge select-detail--flight-stops-badge").text
            flight_numbers = flight.find("button", class_="actionable actionable_button actionable_light button flight-numbers--flight-number").text
            flight_numbers = flight_numbers.replace(" ", "").replace("#", "").replace("\xa0Opensflyout.","").strip().split("/")

            if str(flight_number[2:]) not in flight_numbers:
                continue
            if stops != "Nonstop":
                continue

            fares_list = flight.find_all("span", class_="currency currency_dollars")
            prices = []
            booking_classes = ["business_select", "anytime", "wanna-get-away-plus", "wanna-get-away"]
            for fare in fares_list:
                price = fare.find("span", class_="swa-g-screen-reader-only").text.replace(" Dollars", "")
                prices.append(price)

            list_of_prices_and_codes.extend({"price": price, "booking_class": booking_class,} for price, booking_class in zip(prices, booking_classes))

        return list_of_prices_and_codes


    def get_source(self) -> str:
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "price-matrix--stops")))
        except selenium.common.exceptions.TimeoutException:
            retry = 0
            while "Sorry, we found some errors" in self.driver.page_source:
                btn = self.safe_find(By.ID, "form-mixin--submit-button")
                self.safe_click(btn)
                time.sleep(3)
                retry += 1
                if retry > 6:
                    return ""
        return self.driver.page_source








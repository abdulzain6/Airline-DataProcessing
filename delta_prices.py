from urllib.parse import urlencode
from bs4 import BeautifulSoup
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time, random, selenium, contextlib



class Delta:
    def __init__(self, driver) -> None:
        self.main_url = "https://www.delta.com/apac/en"
        self.driver = driver


    def choose_one_way(self, flight_type_list) -> None:
        self.safe_click(flight_type_list)
        one_way = self.driver.find_element(By.ID, "ui-list-selectTripType1")
        self.safe_click(one_way)


    def safe_click(self, element) -> None:
        retry = 0
        while True:
            with contextlib.suppress(selenium.common.exceptions.NoSuchElementException,selenium.common.exceptions.StaleElementReferenceException, selenium.common.exceptions.ElementNotInteractableException):
                element.click()
                return 
            time.sleep(0.5)
            retry += 1
            if retry > 10:
                break

    def safe_find(self, by, by_what) -> None:
        retry = 0
        while True:
            with contextlib.suppress(selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException):
                return self.driver.find_element(by, by_what)
            time.sleep(0.5)
            retry += 1
            if retry > 10:
                break

    def safe_find_multiple(self, by, by_what, element) -> None:
        retry = 0
        while True:
            with contextlib.suppress(selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException):
                return element.find_elements(by, by_what)
            time.sleep(0.5)
            retry += 1
            if retry > 10:
                break

    def search_elements_by_text(self, elements, text):
        return next((element for element in elements if element.text == text), None)

    def fill_from_and_to(self, destination_button, origin_button, origin_airport, destination_airport) -> None:
        self.safe_click(destination_button)
        input_box = self.safe_find(By.ID, "search_input")
        self.safe_click(input_box)
        for _ in range(7):
            input_box.send_keys(Keys.BACKSPACE)

        input_box.send_keys(destination_airport)
        close_btn = self.safe_find(By.CLASS_NAME, "search-flyout-close.float-right.d-none.d-lg-block.circle-outline.icon-moreoptionsclose")
        self.safe_click(close_btn)

        self.safe_click(origin_button)
        input_box = self.safe_find(By.ID, "search_input")
        self.safe_click(input_box)
        for _ in range(7):
            input_box.send_keys(Keys.BACKSPACE)
        input_box.send_keys(origin_airport)
        close_btn = self.safe_find(By.CLASS_NAME, "search-flyout-close.float-right.d-none.d-lg-block.circle-outline.icon-moreoptionsclose")
        
        self.safe_click(close_btn)



    def choose_date(self, date_selector, datestr) -> None:
        parsed_date = datetime.strptime(datestr, '%Y-%m-%d')

        self.safe_click(date_selector)

        done = False
        full_month_format = "%B %Y"

        while not done:
            left_date_year = self.safe_find(By.CLASS_NAME, "dl-datepicker-year.dl-datepicker-year-0").text
            left_date_month = self.safe_find(By.CLASS_NAME, "dl-datepicker-month-0").text
            right_date_year = self.safe_find(By.CLASS_NAME, "dl-datepicker-year.dl-datepicker-year-1").text
            right_date_month = self.safe_find(By.CLASS_NAME, "dl-datepicker-month-1").text

            left_date = datetime.strptime(f"{left_date_month} {left_date_year}", full_month_format)
            right_date = datetime.strptime(f"{right_date_month} {right_date_year}", full_month_format)


            left_dates = self.safe_find(By.CLASS_NAME, "dl-datepicker-group.dl-datepicker-group-0")
            right_dates = self.safe_find(By.CLASS_NAME, "dl-datepicker-group.dl-datepicker-group-1")

            if parsed_date.month == right_date.month:
                rds = self.safe_find_multiple(By.CLASS_NAME, "dl-state-default", right_dates)
                element_to_click = self.search_elements_by_text(rds, str(parsed_date.day))
                done = True

            elif parsed_date.month == left_date.month:
                lds = self.safe_find_multiple(By.CLASS_NAME, "dl-state-default", left_dates)
                element_to_click = self.search_elements_by_text(lds, str(parsed_date.day))
                done = True

            elif parsed_date.month > right_date.month:
                ## click next button To select previous month
                btn = self.safe_find(By.XPATH, "//a[@title='To select next month']")
                self.safe_click(btn)
                done = False

            elif parsed_date.month < left_date.month:
                ## click next button To select previous month
                btn = self.safe_find(By.XPATH, "//a[@title='To select previous month']")
                self.safe_click(btn)
                done = False

        self.safe_click(element_to_click)
        done_btn = self.safe_find(By.CLASS_NAME, "donebutton")
        self.safe_click(done_btn)



    def get_flight_prices(self, flight_number, origin_airport: str , destination_airport: str , datestr: str) -> List[Dict[str, str]]:
        self.driver.get(self.main_url)
        self.driver.execute_script('window.sessionStorage.clear()')
        self.driver.execute_script('window.localStorage.clear()')
        with contextlib.suppress(Exception):
            element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.ID, "fsrFocusFirst")))
            time.sleep(3)
            self.click(element)
        retries = 0
        while "Book" not in self.driver.page_source:
            retries += 1
            if retries == 10:
                self.driver.refresh()
                retries = 0
            time.sleep(0.5)


        destination_button = self.safe_find(By.CLASS_NAME, "to-container")
        origin_button = self.safe_find(By.CLASS_NAME, "focusable-element.from-container")


        flight_type_list = self.driver.find_element(By.CLASS_NAME, "select-ui-wrapper")
        date_selector = self.safe_find(By.CLASS_NAME, "calDispValueCont.icon-Calendar")

        self.choose_one_way(flight_type_list)
        self.choose_date(date_selector, datestr)
        self.fill_from_and_to(destination_button, origin_button, origin_airport, destination_airport)
        time.sleep(2)
        button_submit = self.safe_find(By.ID, "btn-book-submit")

        self.safe_click(button_submit)

        return self.scrape_results( flight_number, origin_airport , destination_airport , datestr)



    def scrape_results(self, flight_number:str, origin_airport: str , destination_airport: str , datestr) -> List[Dict[str, str]]:
        list_of_prices_and_codes = []

        retry = 0
        while "Show Price In:" not in self.driver.page_source:
            if "Oh no! We're sorry, but there was a problem" in self.driver.page_source or "BOOK A FLIGHT" in self.driver.page_source or "Unfortunately, flights are unavailable for some" in self.driver.page_source or "We're sorry but this service is not available at this time." in self.driver.page_source:
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "nav-item.app-link-item.ng-star-inserted.active-menu")))
                    self.click(element)
                except selenium.common.exceptions.TimeoutException:
                    return []
                return []
            time.sleep(1)
            retry += 1
            if retry > 20:
                break

        for _ in range(3):
            with contextlib.suppress(selenium.common.exceptions.ElementClickInterceptedException, selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException, selenium.common.exceptions.StaleElementReferenceException):
                see_more_results = self.driver.find_element(By.CLASS_NAME, "see-more-btn.ng-star-inserted")
                see_more_results.click()
            time.sleep(1)

        retry = 0
        while "Basic" not in self.driver.page_source:
            retry += 1
            time.sleep(1)
            if retry > 5:
                break

        source = self.driver.page_source

        soup = BeautifulSoup(source, "html.parser")

        flights = soup.find_all("div", class_="row shadow-sm")
        for flight in flights:
            flight_numbers = flight.find_all("a", class_="upsellpopupanchor ng-star-inserted")
            flight_numbers = [flight_number.text.split("\n")[0].replace(" Flight Specific Detailsopens in new popup", "").replace(" 1Footnote","") for flight_number in flight_numbers]

            if flight_number not in flight_numbers:
                continue

            try:
                stops = flight.find("div", class_="nonstop ng-star-inserted").text
                if stops != "Nonstop":
                    continue
            except AttributeError:
                continue

            booking_classes = []
            classes = flight.find_all("div", class_="cabinContainer hidden-md-down")
            for c in classes:
                a = c.find("a", class_="lnkCabinName")
                booking_classes.append(a.find_all("span", class_="ng-star-inserted")[1].text[2:-2])

            p = flight.find_all("span", class_="priceBfrDec ng-star-inserted")

            list_of_prices_and_codes.extend({"price": price.text, "booking_class": booking_class} for price, booking_class in zip(p, booking_classes))

        return list_of_prices_and_codes




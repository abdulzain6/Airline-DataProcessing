from selenium import webdriver as uc
import time
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from twocaptcha import TwoCaptcha
import twocaptcha
from selenium.webdriver.chrome.options import Options
import selenium
from typing import List, Dict


class ExpertFlyer():
    def __init__(self, username: str = "viratkholi4762@gmail.com", password: str = "123456", api_key: str = "9a120a839601107e5820f35621665283") -> None:
        self.username = username
        self.password = password
        self.api_key = api_key

        self.BASE_URL = 'https://www.expertflyer.com/mobile/'

        options = Options()
        options.headless = False
        some_width = 1024
        some_height = 104
        options.add_argument(f"--width={some_width}")
        options.add_argument(f"--height={some_height}")
        self.chrome = uc.Chrome(options=options)

        self.login()

    def is_on_login_page(self) -> bool:
        return "Save My Email and Password" in self.chrome.page_source

    def safe_get(self, url: str) -> None:
        self.chrome.get(url)
        if "Incapsula" in self.chrome.page_source or "<title>[Error Title]</title>" in self.chrome.page_source or "Additional security" in self.chrome.page_source:
            self.handle_captcha(url)
            self.safe_get(url)

    def handle_captcha(self, url: str) -> None:
        time.sleep(10)
        WebDriverWait(self.chrome, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "main-iframe")))
        solver = TwoCaptcha(self.api_key)
        captcha = WebDriverWait(self.chrome, 200).until(EC.presence_of_element_located((By.CLASS_NAME, "g-recaptcha")))
        try:
            data_sitekey = captcha.get_attribute("data-sitekey")
            call_back_func = captcha.get_attribute("data-callback")
            result = solver.recaptcha(
                sitekey=data_sitekey,
                url=self.chrome.current_url)
        except twocaptcha.api.ApiException:
            self.safe_get(url)
            
        code = result["code"]
        while True:
            try:
                self.chrome.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{code}";')
                self.chrome.execute_script(f'{call_back_func}("{code}");')
                time.sleep(10)
                break
            except selenium.common.exceptions.JavascriptException:
                time.sleep(2)

    def login(self) -> None:
        self.safe_get(self.BASE_URL)

        # self.chrome.find_element(By.ID, "email-text").send_keys(self.username)
        email = WebDriverWait(self.chrome, 1000).until(
            EC.presence_of_element_located((By.ID, "email")))
        email.send_keys(self.username)
        time.sleep(2)
        # self.chrome.find_element(By.ID, "password-text").send_keys(self.password)
        password = WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.ID, "password")))
        password.send_keys(self.password)
        # self.chrome.find_element(By.ID, "password").send_keys(self.password)
        time.sleep(2)
        # self.chrome.find_element(
        #     By.XPATH, "//input[@id='login-button']"
        # ).click()
        self.chrome.find_element(
            By.XPATH, "//input[@name='login']"
        ).click()
        time.sleep(4)

    def flight_timetables_from_airport(self, airport: str) -> List[Dict]:
        SEC = 2
        if self .is_on_login_page():
            self.login()
        self.safe_get('https://www.expertflyer.com/mobile/flightTimetablesByCity.do')
        time.sleep(5)
        if self .is_on_login_page():
            self.login()
        if "You do not have access to perform this operation" in self.chrome.page_source:
            raise Exception("Subscription Error")

        airline = WebDriverWait(self.chrome, 30).until(EC.presence_of_element_located((By.NAME, "airportCode")))
        airline.send_keys(airport)
        time.sleep(SEC)
        search = WebDriverWait(self.chrome, 30).until(EC.presence_of_element_located((By.NAME, 'search')))
        search.click()
        time.sleep(10)
        tree = html.fromstring(self.chrome.page_source)
        path = tree.xpath('//form[@name="flightTimetablesResults"]/div[@class="form-result"]')
        schedules = []
        for p in path:
            deadline = p.xpath('./div[1]/table/tbody/tr/td[2]/text()')
            effective = ''
            ending = ''
            if deadline:
                deadline = re.sub(r'\s+', ' ', ''.join(deadline).strip())
                dates = re.findall(r'\d{2}\/\d{2}\/\d{2}', deadline)
                effective = dates[0]
                ending = dates[1]

            code = p.xpath('./div[3]/table/tbody/tr/td[1]/text()')
            flight = ''
            if code:
                code = re.sub(r'\s+', ' ', ''.join(code).strip())
                flight = code

            schedule = p.xpath('./div[3]/table/tbody/tr/td[2]/text()')
            # airport_code = re.findall(r'[A-Z]{3}', schedule)
            depart_code = airport
            arrive_code = ''
            depart_time = '00:00 AM'
            arrive_time = '00:00 AM'
            if schedule:
                schedule = re.sub(r'\s+', ' ', ''.join(schedule).strip())
                time_ = re.findall(r'\d{1,2}:\d{1,2} [A|P][M]', schedule)
                airport_code = re.findall(r'[A-Z]{3}', schedule)
                depart_code = airport_code[0]
                arrive_code = airport_code[1]
                depart_time = time_[0]
                arrive_time = time_[1]

            stops = p.xpath('./div[4]/table/tbody/tr[1]/td[2]/text()')
            if stops:
                stops = ''.join(stops)
            else:
                stops = ''.join(stops)

            aircraft = p.xpath('./div[4]/table/tbody/tr[2]/td[2]/text()')
            if aircraft:
                aircraft = re.sub(r'\s+', ' ', ''.join(aircraft).strip())
            else:
                aircraft = ''.join(aircraft)

            frequency = p.xpath('./div[2]/table/tbody/tr[1]/td[2]/text()')
            if frequency:
                frequency = re.sub(r'\s+', ' ', ''.join(frequency).strip())
            else:
                frequency = ''.join(frequency)

            duration = p.xpath('./div[2]/table/tbody/tr[2]/td[2]/text()')
            if duration:
                duration = re.sub(r'\s+', ' ', ''.join(duration).strip())
            else:
                duration = ''.join(duration)

            schedules.append({
                'depart_airport': depart_code,
                'depart_time': depart_time,
                'arriving_airport': arrive_code,
                'arrive_time': arrive_time,
                'schedule_start': effective,
                'schedule_stop': ending,
                'flight': flight,
                'stops': stops,
                'aircraft': aircraft,
                'frequency': frequency,
                'duration': duration
            })

        return schedules


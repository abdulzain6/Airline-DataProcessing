from south_west import SouthWest
from delta_prices import Delta
from ua_prices import United_Air
from ryan_air import Ryan_Air
from typing import List, Dict
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as webdriver
import selenium, time, os

class Get_Prices():
	def __init__(self, is_lamda=False):
		self.is_lamda = is_lamda
		options = webdriver.ChromeOptions()
		options.add_argument("--start-maximized")
		options.add_argument("--incognito")
		options.headless = False
		options.add_argument("--disable-popup-blocking")
		self.driver = self.make_driver()
		self.SW_obj =  SouthWest(self.driver)
		self.DL_obj = Delta(self.driver)
		

	def make_driver(self) -> webdriver:
		options = webdriver.ChromeOptions()
		options.add_argument("--start-maximized")
		options.add_argument("--incognito")
		options.headless = False
		options.add_argument("--disable-popup-blocking")
		if self.is_lamda:
			data_path = "/tmp/chrome_data"
			if not os.path.exists(data_path):
				os.mkdir(data_path)
		else:
			data_path = "None"

		driver = webdriver.Chrome(options=options, user_data_dir=data_path)
		driver.set_page_load_timeout(30)
		return driver

	def get_flight_prices_online_specific(self, airline: str, flight_number: str, origin_airport: str, destination_airport: str, date_str: str) -> List[Dict[str, str]]:
		if airline == "UA":
			return United_Air(flight_number, origin_airport, destination_airport, date_str).get_flight_prices()

		elif airline == "DL":
			return self.DL_obj.get_flight_prices(flight_number, origin_airport, destination_airport, date_str)

		elif airline == "WN":
			return self.SW_obj.get_flight_prices(flight_number, origin_airport, destination_airport, date_str)

		elif airline == "FR":
			return Ryan_Air(flight_number, origin_airport, destination_airport, date_str).get_flight_prices()
		else:
			return []



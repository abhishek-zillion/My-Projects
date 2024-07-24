import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from types import TracebackType
from typing import Type
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bot.constants import (
    BASE_URL
)
from selenium.webdriver.common.by import By
from bot.booking_filteration import BookingFilteration


class Booking(webdriver.Chrome):
    def __init__(self, options: Options = None, service: Service = None, keep_alive: bool = True,
                 teardown=False) -> None:
        self.teardown = teardown
        chrome_options = Options()
        chrome_options.add_argument('--incognito')
        super().__init__(options=chrome_options, service=service, keep_alive=keep_alive)
        self.implicitly_wait(10)
        self.maximize_window()

    def close_dialouge_box_if_appears(self):
        try:
            close_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.b02ceec9d7'))
            )
            close_button.click()
            print("Dialog box closed successfully.")
        except TimeoutException:
            # Dialog didn't appear, which is fine
            pass
        except Exception as e:
            print(
                f"An error occurred while trying to close the dialog box: {e}")

    def land_first_page(self):
        self.get(BASE_URL)
        self.close_dialouge_box_if_appears()

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        if self.teardown:
            self.quit()

    def change_curency(self, currency=None):
        currency_element = self.find_element(
            By.XPATH, '//button[@data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        selected_currency = self.find_element(
            By.CSS_SELECTOR, ".a2ce59f28d")
        selected_currency.click()
        self.close_dialouge_box_if_appears()

    def select_place_to_go(self, place_to_go):
        # self.close_dialouge_box_if_appears()

        try:
            search_field = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@placeholder="Where are you going?"]'))
            )
            search_field.clear()
            time.sleep(2)  # Wait for the dropdown to load
            search_field.send_keys(place_to_go)

            first_result = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.ID, 'autocomplete-result-0'))
            )
            first_result.click()
            # self.close_dialouge_box_if_appears()

        except TimeoutException:
            print(
                "The search field or the first result could not be found within the specified time.")
        except Exception as e:
            print(f"An error occurred while selecting the place to go: {e}")

    def select_dates(self, check_in_date=None, checkout_date=None):
        check_in_element = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[@data-date='{check_in_date}']"))
        )
        check_in_element.click()
        checkout_element = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[@data-date='{checkout_date}']"))
        )
        checkout_element.click()

    def select_guests(self, count=None):
        selction_element = self.find_element(
            By.XPATH, '//button[@data-testid="occupancy-config"]')
        selction_element.click()

        decreasing_element = self.find_element(
            By.CSS_SELECTOR, "button.e137a4dfeb:nth-child(1)")
        while True:
            input_element = self.find_element(By.ID, "group_adults")
            value = input_element.get_attribute("value")
            if str(value) == '1':
                break
            decreasing_element.click()

        increase_element = self.find_element(
            By.CSS_SELECTOR, "div.f340be2edd:nth-child(1) > div:nth-child(3) > button:nth-child(3)")

        while count > 1:
            increase_element.click()
            count -= 1

    def click_search(self):
        submit_element = self.find_element(
            By.XPATH, "//button[@type='submit']")
        submit_element.click()

    def apply_filteration(self):
        filteration = BookingFilteration(driver=self)
        filteration.apply_star_rating(3)
        filteration.apply_facilities()
        filteration.apply_reservation_policy([
            "Free cancellation",
            "Book without credit card",
            "No prepayment"
        ])
        filteration.display_filters_and_hotels()

from types import TracebackType
from typing import Type
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bot.constants import (
    BASE_URL
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lxml import html


class Booking(webdriver.Chrome):
    def __init__(self, options: Options = None, service: Service = None, keep_alive: bool = True,
                 teardown=False) -> None:
        self.teardown = teardown
        super().__init__(options, service, keep_alive)
        self.implicitly_wait(10)
        self.maximize_window()

    def land_first_page(self):
        self.get(BASE_URL)
        self.close_dialouge_box()
    def close_dialouge_box(self):
        try:
            close_button = self.find_element(By.CSS_SELECTOR, '.b02ceec9d7')
            close_button.click()
        except Exception as e:
            print("Dialog box not found or couldn't be closed:", e)

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        if self.teardown:
            self.quit()
        # return super().__exit__(exc_type, exc, traceback)

    def change_curency(self, currency=None):
        currency_element = self.find_element(
            By.XPATH, '//button[@data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        selected_currency = self.find_element(
            By.CSS_SELECTOR, ".a2ce59f28d")
        selected_currency.click()

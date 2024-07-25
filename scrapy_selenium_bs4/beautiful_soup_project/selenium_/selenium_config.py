from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Selenium(webdriver.Chrome):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        self.driver = webdriver.Chrome(options=chrome_options)

    def land_page(self, url=None):
        self.driver.get("https://www.imdb.com/chart/top/")
        return self.driver.page_source

    def get_movie_data(self):
        movie_element = WebDriverWait(self.__getattribute__driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "ipc-metadata-list"))
        )
        movies_list = movie_element.find_elements(
            By.CLASS_NAME, "ipc-metadata-list-summary-item")

        return movies_list

    def quit(self):
        self.driver.quit()

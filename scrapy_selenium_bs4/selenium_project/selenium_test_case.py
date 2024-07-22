import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_python(self):
        '''
        Testing search box for python
        '''
        driver = self.driver
        driver.get("https://www.python.org/")
        self.assertIn("Python", driver.title)

        elem = driver.find_element(By.NAME, 'q')
        elem.send_keys("pycon")
        elem.send_keys(Keys.ENTER)
        self.assertNotIn("No results found", driver.page_source)

    def tearDown(self):
        self.driver.close()


class AmazonSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_amazon(self):
        driver = self.driver
        driver.get("https://www.amazon.in/")
        elem = driver.find_element(By.ID, 'twotabsearchtextbox')

        elem.send_keys("laptop")
        elem.send_keys(Keys.ENTER)
        elems = driver.find_elements(By.CLASS_NAME, "puis-card-container")
        print(len(elems))

        for elem in elems:

            print(elem.text)


if __name__ == "__main__":
    unittest.main()

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException, StaleElementReferenceException,
    ElementClickInterceptedException)
import time


class BookingFilteration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)

    def click_element(self, element):
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def apply_star_rating(self, star):
        try:
            star_section = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[.//h3[contains(text(), 'Property rating')]]")
            ))
            self.scroll_to_element(star_section)
            star_options = star_section.find_elements(
                By.XPATH, ".//div[contains(@data-filters-item, 'class:class=')]")

            if 1 <= star <= len(star_options):
                checkbox = star_options[star -
                                        1].find_element(By.TAG_NAME, "input")
                self.click_element(checkbox)
                print(f"Applied {star} star rating filter")
            else:
                print(
                    f"Invalid star rating: {star}. Please choose a rating between 1 and {len(star_options)}.")
        except Exception as e:
            print(f"Error applying star rating: {e}")

    def apply_facilities(self):
        try:
            facilities_section = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[.//h3[contains(text(), 'Facilities')]]")
                ))
            self.scroll_to_element(facilities_section)
            facilities_options = facilities_section.find_elements(
                By.XPATH, ".//div[contains(@data-filters-item, 'hotelfacility')]"
            )
            for option in facilities_options[:2]:  # Select first two options
                checkbox = option.find_element(By.TAG_NAME, "input")
                self.click_element(checkbox)
            print("Applied facilities filters")
        except Exception as e:
            print(f"Error applying facilities: {e}")

    def apply_sorting_lowest_first(self):
        wait = WebDriverWait(self.driver, 10)
        sort_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="sorters-dropdown-trigger"]')
        ))
        sort_button.click()
        sort_button.click()
        time.sleep(1)
        lowest_price_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, ".//button[@data-id='price']")
        ))
        lowest_price_option.click()

    def apply_reservation_policy(self, options):
        try:
            wait = WebDriverWait(self.driver, 15)

            policy_section = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[.//h3[contains(text(), 'Reservation') or contains(text(), 'Cancellation') or contains(text(), 'Payment')]]")
            ))

            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", policy_section)
            time.sleep(1)

            for option in options:
                try:
                    option_xpath = f".//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{option.lower()}')]"
                    option_element = wait.until(
                        EC.element_to_be_clickable((By.XPATH, option_xpath)))

                    checkbox = option_element.find_element(
                        By.XPATH, ".//ancestor::div[1]//input[@type='checkbox']")
                    if not checkbox.is_selected():
                        self.driver.execute_script(
                            "arguments[0].click();", option_element)
                        print(f"Selected: {option}")
                        time.sleep(0.5)
                    else:
                        print(f"{option} is already selected.")

                except (TimeoutException, NoSuchElementException):
                    print(f"Option not found or not clickable: {option}")

            print("Reservation policy options applied successfully.")

        except TimeoutException:
            print("Timeout occurred: The reservation policy section was not found.")
        except Exception as e:
            print(
                f"An error occurred while applying reservation policy options: {e}")

    def display_filters_and_hotels(self):
        try:
            wait = WebDriverWait(self.driver, 15)

            print("\n" + "="*50)
            print("AVAILABLE FILTERS")
            print("="*50)

            # Display filters
            filter_groups = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-filters-group]")))
            for group in filter_groups:
                try:
                    group_name = WebDriverWait(group, 5).until(
                        EC.presence_of_element_located((By.XPATH, ".//h3"))).text
                    print(f"\n{group_name}:")
                    options = WebDriverWait(group, 5).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, ".//div[contains(@data-filters-item, ':')]")))
                    for option in options:
                        try:
                            option_text = option.text.replace("\n", ": ")
                            print(f"  - {option_text}")
                        except StaleElementReferenceException:
                            continue
                except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                    continue

            print("\n" + "="*50)
            print("HOTEL LISTINGS")
            print("="*50)

            # Display hotel listings
            hotel_listings = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-testid='property-card']")))
            for index, hotel in enumerate(hotel_listings, 1):
                try:
                    name = WebDriverWait(hotel, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//div[@data-testid='title']"))).text
                    price = WebDriverWait(hotel, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//span[@data-testid='price-and-discounted-price']"))).text
                    rating = WebDriverWait(hotel, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//div[@data-testid='review-score']"))).text

                    print(f"\n{index}. {name}")
                    print(f"   Price: {price}")
                    print(f"   Rating: {rating}")

                    try:
                        location = WebDriverWait(hotel, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, ".//span[@data-testid='address']"))).text
                        print(f"   Location: {location}")
                    except (NoSuchElementException,
                            StaleElementReferenceException, TimeoutException):
                        pass

                    try:
                        amenities = WebDriverWait(hotel, 5).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, ".//div[contains(@class, 'amenities')]//div")))
                        if amenities:
                            print("   Amenities:", ", ".join(
                                [a.text for a in amenities if a.text]))
                    except (NoSuchElementException,
                            StaleElementReferenceException, TimeoutException):
                        pass

                except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                    print(f"\n{index}. [Error retrieving hotel information]")

            print("\n" + "="*50)

        except TimeoutException:
            print("Timeout occurred: Unable to load the page or find elements.")
        except Exception as e:
            print(
                f"An error occurred while displaying filters and hotels: {e}")

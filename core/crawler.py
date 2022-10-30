from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from core.chrome_driver import ChromeDriver
from core.yaml_option import YamlOption
from util import randomized_sleep
from consts import crawler_consts


class Crawler:
    def __init__(self):
        self.__option = YamlOption()
        self.__driver = ChromeDriver().driver

    def get_option(self):
        return self.__option

    def page_height(self) -> dict:
        return self.__driver.execute_script(crawler_consts.PAGE_HEIGHT)

    def page_source(self) -> str:
        return self.__driver.page_source

    def get(self, url) -> None:
        self.__driver.get(url)

    def close(self) -> None:
        self.__driver.quit()

    @property
    def current_url(self) -> str:
        return self.__driver.current_url

    def implicitly_wait(self, t) -> None:
        self.__driver.implicitly_wait(t)

    def find_one(self, css_selector, elem=None, wait_time=0):
        obj = elem or self.__driver

        if wait_time:
            WebDriverWait(obj, wait_time).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def find_one_xpath(self, css_selector, elem=None, wait_time=0):
        obj = elem or self.__driver

        if wait_time:
            WebDriverWait(obj, wait_time).until(
                expected_conditions.presence_of_element_located((By.XPATH, css_selector))
            )

        try:
            return obj.find_element(By.XPATH, css_selector)
        except NoSuchElementException:
            return None

    def find_tag(self, css_selector, elem=None, wait_time=0):
        obj = elem or self.__driver

        if wait_time:
            WebDriverWait(obj, wait_time).until(
                expected_conditions.presence_of_element_located((By.TAG_NAME, css_selector))
            )

        try:
            return obj.find_elements(By.TAG_NAME, css_selector)
        except NoSuchElementException:
            return None

    def find_xpath(self, css_selector, elem=None, wait_time=0):
        obj = elem or self.__driver

        if wait_time:
            WebDriverWait(obj, wait_time).until(
                expected_conditions.presence_of_element_located((By.XPATH, css_selector))
            )

        try:
            return obj.find_elements(By.XPATH, css_selector)
        except NoSuchElementException:
            return None

    def find(self, css_selector, elem=None, wait_time=0):
        obj = elem or self.__driver

        try:
            if wait_time:
                WebDriverWait(obj, wait_time).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
        except TimeoutException:
            return None

        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def scroll_down(self, wait=0.3):
        self.__driver.execute_script(crawler_consts.SCROLL_DOWN)
        randomized_sleep(wait)

    def scroll_up(self, offset=-1, wait=2):
        if offset == -1:
            self.__driver.execute_script(crawler_consts.SCROLL_UP_TOP)
        else:
            self.__driver.execute_script(crawler_consts.SCROLL_UP_OFFSET % offset)
        randomized_sleep(wait)

    def js_click(self, elem):
        self.__driver.execute_script(crawler_consts.CLICK, elem)

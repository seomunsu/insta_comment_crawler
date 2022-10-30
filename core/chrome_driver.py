import os
import sys
import platform
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from util import create_logger

_thread_local = threading.local()


class ChromeDriver:
    def __init__(self):
        self.driver = getattr(_thread_local, 'driver', None)
        self.log = create_logger(self.__class__.__name__)

        if self.driver is None:
            self.log.info(f'Using System : {sys.platform}')
            self.log.info(f'Using platform : {platform.platform()}')
            self.log.info(f'Using processor : {platform.processor()}')
            # system, platform, processor 참고하여 chromedriver 파일 다운로드.

            self.driver = self.load_chrome_driver()
            setattr(_thread_local, 'driver', self.driver)
            self.driver.implicitly_wait(5)

    def close(self):
        self.driver.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def load_chrome_driver(self):
        service_args = ["--ignore-ssl-errors=true"]
        dir_path = self.__load_dir_path()
        chrome_option = self.__load_chrome_option()

        if 'linux' in sys.platform:
            driver = webdriver.Chrome(
                service_args=service_args,
                chrome_options=chrome_option
            )
        else:
            driver = webdriver.Chrome(
                executable_path='%s/bin/chromedriver' % dir_path,
                service_args=service_args,
                chrome_options=chrome_option
            )

        return driver

    @staticmethod
    def __load_dir_path() -> str:
        return os.path.dirname(os.path.realpath(__file__ + '/../'))

    @staticmethod
    def __load_chrome_option() -> Options:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')
        chrome_options.add_argument('lang=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7')
        chrome_options.add_experimental_option('prefs', {
            "profile.default_content_setting_values": {
                # "cookies": 2,
                "images": 2,
                "plugins": 2,
                "popups": 2,
                "geolocation": 2,
                "notifications": 2,
                "auto_select_certificate": 2,
                "fullscreen": 2,
                "mouselock": 2,
                "mixed_script": 2,
                "media_stream": 2,
                "media_stream_mic": 2,
                "media_stream_camera": 2,
                "protocol_handlers": 2,
                "ppapi_broker": 2,
                "automatic_downloads": 2,
                "midi_sysex": 2,
                "push_messaging": 2,
                "ssl_cert_decisions": 2,
                "metro_switch_to_desktop": 2,
                "protected_media_identifier": 2,
                "app_banner": 2,
                "site_engagement": 2,
                "durable_storage": 2
            }
        })

        return chrome_options

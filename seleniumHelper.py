import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumHelper:
    def __init__(self, driver_path):
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)
        self.start_time = datetime.now()

        # Создаем папку для логов, если она не существует
        log_dir = "seleniumRuns"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Настраиваем логирование
        log_file = os.path.join(log_dir, f"test_log_{self.start_time.strftime('%Y-%m-%d_%H-%M-%S')}.log")
        self.logger = logging.getLogger("SeleniumHelper")
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.info("WebDriver initialized.")

    def _log_action(self, action, by, value, elapsed_time, comment=None):
        log_message = f"{action} element: {by}={value} in {elapsed_time:.2f} ms"
        if comment:
            log_message += f" - Comment: {comment}"
        self.logger.info(log_message)

    def open_url(self, url):
        start_time = datetime.now()
        self.driver.get(url)
        elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
        self._log_action("Opened URL", "url", url, elapsed_time)

    def find_element(self, by, value, timeout=3, comment=None):
        try:
            start_time = datetime.now()
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
            self._log_action("Found element", by, value, elapsed_time, comment)
            return element
        except Exception as e:
            self.logger.error(f"Error finding element: {by}={value} - {str(e)}")
            self.driver.save_screenshot('error_screenshot.png')
            raise

    def click(self, by, value, timeout=3, comment=None):
        try:
            element = self.find_element(by, value, timeout, comment)
            start_time = datetime.now()
            element.click()
            elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
            self._log_action("Clicked", by, value, elapsed_time, comment)
        except Exception as e:
            self.logger.error(f"Error clicking element: {by}={value} - {str(e)}")
            raise

    def write(self, by, value, text, timeout=3, comment=None):
        try:
            element = self.find_element(by, value, timeout, comment)
            start_time = datetime.now()
            element.send_keys(text)
            elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
            self._log_action("Sent keys to", by, value, elapsed_time, comment)
        except Exception as e:
            self.logger.error(f"Error sending keys to element: {by}={value} - {str(e)}")
            raise

    def quit(self):
        start_time = datetime.now()
        self.driver.quit()
        elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
        self._log_action("WebDriver quit", "driver", "driver", elapsed_time)
        total_elapsed_time = (datetime.now() - self.start_time).total_seconds() * 1000
        self.logger.info(f"Total execution time: {total_elapsed_time:.2f} ms")


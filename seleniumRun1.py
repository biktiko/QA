# test_script.py

from seleniumHelper import SeleniumHelper
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    Selenium = SeleniumHelper('C:/WorkPlace/QA/chromedriver.exe')
    Selenium.open_url("https://www.google.com")
    Selenium.write(By.NAME, 'q', "Hello World", comment="Թեսթի համար սա")
    Selenium.click(By.NAME, "btnK")
    
    # Блокируем выполнение, чтобы программа не завершилась
    # input("Нажмите Enter для завершения программы и закрытия браузера...")
    Selenium.quit()

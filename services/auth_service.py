import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger_config import log_message


class AuthService:

    def __init__(self, browser, email, password):
        self.browser = browser
        self.email = email
        self.password = password

    def open_schedule(self):
        driver = self.browser.driver

        log_message("Авторизация в личном кабинете")

        driver.get("https://lk.sut.ru/")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "users"))
        ).send_keys(self.email)

        driver.find_element(By.ID, "parole").send_keys(self.password)
        driver.find_element(By.ID, "logButton").click()

        log_message("Открываем расписание")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "title_item"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "menu_li_6118"))
        ).click()

        time.sleep(3)
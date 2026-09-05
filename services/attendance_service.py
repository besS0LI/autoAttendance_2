import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger_config import log_message


class AttendanceService:

    def __init__(self, browser, auth_service):
        self.browser = browser
        self.auth_service = auth_service

    def mark_attendance(self, lesson):

        log_message(f"Начата обработка занятия: {lesson['name']}")

        self.browser.start()
        self.auth_service.open_schedule()

        driver = self.browser.driver

        try:

            start_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@onclick, 'open_zan')]")
                )
            )

            log_message("Кнопка Начать занятие найдена")

            start_button.click()

            log_message(f'Поставлена отметка на паре "{lesson["name"]}"')

        except:

            log_message("Кнопка Начать занятие отсутствует")

            while True:

                try:

                    refresh_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[contains(@onclick, 'update_zan')]")
                        )
                    )

                    log_message("Кнопка Обновить найдена")

                    refresh_button.click()

                    try:

                        start_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//a[contains(@onclick, 'open_zan')]")
                            )
                        )

                        start_button.click()

                        log_message(f'Поставлена отметка на паре "{lesson["name"]}"')

                        break

                    except:

                        log_message("Ожидание появления кнопки Начать занятие")

                        time.sleep(60)

                except:

                    log_message("Кнопка Обновить не найдена")

                    time.sleep(10)

        self.browser.stop()
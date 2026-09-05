import time

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logger_config import log_message


class AttendanceService:

    def __init__(self, browser, auth_service):
        self.browser = browser
        self.auth_service = auth_service

    def _find_start_button(self, driver, timeout=3):
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick, 'open_zan')]")
            )
        )

    def _find_refresh_button(self, driver, timeout=3):
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick, 'update_zan')]")
            )
        )

    def mark_attendance(self, lesson):
        log_message(f"Начата обработка занятия: {lesson['name']}")

        try:
            self.browser.start()
            self.auth_service.open_schedule()
            driver = self.browser.driver

            try:
                start_button = self._find_start_button(driver)
                log_message("Кнопка Начать занятие найдена")
                start_button.click()
                log_message(
                    f'Поставлена отметка на паре "{lesson["name"]}"'
                )
                return
            except TimeoutException:
                log_message("Кнопка Начать занятие пока отсутствует")

            while True:
                try:
                    refresh_button = self._find_refresh_button(driver)
                    log_message("Кнопка Обновить найдена")
                    refresh_button.click()
                except TimeoutException:
                    log_message("Кнопка Обновить не найдена")
                    time.sleep(10)
                    continue

                try:
                    start_button = self._find_start_button(driver)
                    log_message("Кнопка Начать занятие найдена")
                    start_button.click()
                    log_message(
                        f'Поставлена отметка на паре "{lesson["name"]}"'
                    )
                    return
                except TimeoutException:
                    log_message("Ожидание появления кнопки Начать занятие")
                    time.sleep(60)

        except WebDriverException as exc:
            log_message(f"Ошибка WebDriver при отметке: {exc}")
            raise
        except Exception as exc:
            log_message(f"Ошибка при отметке посещаемости: {exc}")
            raise
        finally:
            self.browser.stop()

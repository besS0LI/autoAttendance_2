from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logger_config import log_message


class ScheduleService:

    def __init__(self, browser, auth_service):
        self.browser = browser
        self.auth_service = auth_service

    def get_schedule(self):
        schedule_data = {}
        now_date = datetime.now().strftime("%d.%m.%Y")

        try:
            self.browser.start()
            self.auth_service.open_schedule()

            driver = self.browser.driver
            log_message("Получение расписания")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "simple-little-table")
                )
            )

            table = driver.find_element(By.CLASS_NAME, "simple-little-table")
            rows = table.find_elements(By.TAG_NAME, "tr")

            reading_today = False

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) == 1:
                    reading_today = now_date in cells[0].text
                    continue

                if not reading_today or len(cells) < 2:
                    continue

                try:
                    time_text = cells[0].text
                    start_time = time_text.split("(")[1].split("-")[0].zfill(5)

                    lesson_name = cells[1].find_element(
                        By.TAG_NAME, "b"
                    ).text.strip()

                    schedule_data[start_time] = {
                        "name": lesson_name
                    }
                except (IndexError, ValueError):
                    continue
                except Exception as exc:
                    log_message(f"Ошибка чтения строки расписания: {exc}")

            log_message(f"Расписание на {now_date}")

            for time_key, lesson in schedule_data.items():
                log_message(f"{time_key} — {lesson['name']}")

            return schedule_data

        finally:
            self.browser.stop()

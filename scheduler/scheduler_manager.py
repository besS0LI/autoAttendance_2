import time
from datetime import datetime, timedelta

import schedule

from logger_config import log_message


class SchedulerManager:

    def __init__(self, schedule_service, attendance_service):
        self.schedule_service = schedule_service
        self.attendance_service = attendance_service

    def _schedule_today(self):
        schedule.clear()

        schedule_data = self.schedule_service.get_schedule()

        if not schedule_data:
            log_message("Сегодня занятий нет")
            return False

        current_time = datetime.now().strftime("%H:%M")

        for lesson_time, lesson_data in schedule_data.items():
            if lesson_time < current_time:
                log_message(
                    f"Пропущено время занятия {lesson_time} — "
                    f"{lesson_data['name']}"
                )
                continue

            schedule.every().day.at(lesson_time).do(
                self.attendance_service.mark_attendance,
                lesson_data
            )

            log_message(
                f"Добавлена задача {lesson_time} — {lesson_data['name']}"
            )

        return bool(schedule.get_jobs())

    @staticmethod
    def _seconds_until_next_day():
        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        return max(1, int((tomorrow - now).total_seconds()))

    def run(self):
        log_message("Запущен постоянный планировщик")

        current_date = None

        while True:
            today = datetime.now().date()

            if today != current_date:
                current_date = today
                log_message(f"Обновление расписания на {today:%d.%m.%Y}")

                try:
                    has_jobs = self._schedule_today()
                except Exception as exc:
                    schedule.clear()
                    log_message(f"Ошибка получения расписания: {exc}")
                    has_jobs = False

                if not has_jobs:
                    sleep_seconds = min(self._seconds_until_next_day(), 300)
                    time.sleep(sleep_seconds)
                    continue

            try:
                schedule.run_pending()
            except Exception as exc:
                log_message(f"Ошибка выполнения задачи: {exc}")

            time.sleep(5)

import schedule
import time
from logger_config import log_message


class SchedulerManager:

    def __init__(self, schedule_service, attendance_service):

        self.schedule_service = schedule_service
        self.attendance_service = attendance_service

    def schedule_tasks(self):

        schedule_data = self.schedule_service.get_schedule()

        if not schedule_data:
            log_message("Сегодня занятий нет")
            return False

        for lesson_time, lesson_data in schedule_data.items():

            schedule.every().day.at(lesson_time).do(
                self.attendance_service.mark_attendance,
                lesson_data
            )

            log_message(f"Добавлена задача {lesson_time} — {lesson_data['name']}")

        return True

    def run(self):

        log_message("Ожидание наступления времени занятий")

        while schedule.get_jobs():

            schedule.run_pending()
            time.sleep(30)

        log_message("Все задания выполнены")
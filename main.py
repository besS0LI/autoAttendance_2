import os

from services.browser_service import BrowserService
from services.auth_service import AuthService
from services.schedule_service import ScheduleService
from services.attendance_service import AttendanceService
from scheduler.scheduler_manager import SchedulerManager
from logger_config import log_message


def start_program():
    log_message("Программа запущена")

    email = os.getenv("AUTOATTENDANCE_EMAIL")
    password = os.getenv("AUTOATTENDANCE_PASSWORD")

    if not email or not password:
        raise RuntimeError(
            "Не заданы AUTOATTENDANCE_EMAIL и AUTOATTENDANCE_PASSWORD"
        )

    browser = BrowserService()
    auth_service = AuthService(browser, email, password)
    schedule_service = ScheduleService(browser, auth_service)
    attendance_service = AttendanceService(browser, auth_service)

    scheduler = SchedulerManager(schedule_service, attendance_service)
    scheduler.run()


if __name__ == "__main__":
    start_program()

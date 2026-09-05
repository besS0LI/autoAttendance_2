from services.browser_service import BrowserService
from services.auth_service import AuthService
from services.schedule_service import ScheduleService
from services.attendance_service import AttendanceService
from scheduler.scheduler_manager import SchedulerManager
from logger_config import log_message


def start_program():

    log_message("Программа запущена")

    #email =
    #password =

    browser = BrowserService()

    auth_service = AuthService(browser, email, password)

    schedule_service = ScheduleService(browser, auth_service)

    attendance_service = AttendanceService(browser, auth_service)

    scheduler = SchedulerManager(schedule_service, attendance_service)

    if scheduler.schedule_tasks():
        scheduler.run()
from PIL import Image
import pystray
import threading

from main import start_program


def run_program():
    start_program()


def create_tray():

    image = Image.open("icon.ico")

    menu = pystray.Menu(
        pystray.MenuItem("Выход", lambda icon, item: icon.stop())
    )

    icon = pystray.Icon(
        "AutoAttendance",
        image,
        "Auto Attendance",
        menu
    )

    thread = threading.Thread(target=run_program)
    thread.daemon = True
    thread.start()

    icon.run()
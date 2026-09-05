from selenium import webdriver


class BrowserService:

    def __init__(self):
        self.driver = None

    def start(self):
        if self.driver is not None:
            return

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors=yes")

        self.driver = webdriver.Chrome(options=options)

    def stop(self):
        if self.driver:
            try:
                self.driver.quit()
            finally:
                self.driver = None

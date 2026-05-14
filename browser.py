from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Browser:
    def __init__(self, driver):
        self.driver = driver

    def criar_driver_primeiro_plano(self):
        browser_options = Options()
        browser_options.add_experimental_option("detach", True)
        browser_options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=browser_options)

    def criar_driver_segundo_plano(self):
        browser_options = Options()
        browser_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=browser_options)
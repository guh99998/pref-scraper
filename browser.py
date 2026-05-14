from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Browser:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def criar_driver_primeiro_plano():
        browser_options = Options()
        browser_options.add_experimental_option("detach", True)
        browser_options.page_load_strategy = 'eager'

        prefs = {
            "download.default_directory": "C:\\Users\\gusta\\Downloads\\",
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
        }
        browser_options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=browser_options)

    @staticmethod
    def criar_driver_segundo_plano():
        browser_options = Options()
        browser_options.add_argument("--headless=new")
        return webdriver.Chrome(options=browser_options)
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Browser:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def criar_driver_primeiro_plano(pasta_download):
        pasta_download = os.path.normpath(pasta_download)
        browser_options = Options()
        browser_options.add_experimental_option("detach", True)
        browser_options.page_load_strategy = 'eager'

        prefs = {
            "download.default_directory": pasta_download,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
        }
        browser_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=browser_options)
        driver.pasta_download = pasta_download
        return driver

    @staticmethod
    def criar_driver_segundo_plano(pasta_download):
        pasta_download = os.path.normpath(pasta_download)
        browser_options = Options()
        browser_options.add_argument("--headless=new")
        browser_options.add_argument("--window-size=1920,1080")
        browser_options.add_argument("--disable-gpu")
        browser_options.add_argument("--no-sandbox")
        browser_options.page_load_strategy = 'eager'
        prefs = {
            "download.default_directory": pasta_download,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
        }
        browser_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=browser_options)
        driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": pasta_download
        })
        driver.pasta_download = pasta_download
        return driver
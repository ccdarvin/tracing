from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium import webdriver


def init_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    stealth(driver,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
        languages=["es-PE", "es"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

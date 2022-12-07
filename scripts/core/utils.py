from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from .models import Website






def scroll_down(driver, selector, amount=10):
    elem = driver.find_element(By.CSS_SELECTOR, selector)
    scroll_origin = ScrollOrigin.from_element(elem)
    ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, amount)\
            .perform()

    
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from .models import Website
from .config import get_settings
import websockets


settings = get_settings()


def scroll_down(driver, selector, amount=10):
    elem = driver.find_element(By.CSS_SELECTOR, selector)
    scroll_origin = ScrollOrigin.from_element(elem)
    ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, amount)\
            .perform()
            
            
async def send_message_website(website: Website):
    uri = f'{settings.WS}/websites'
    await send_message(uri, website.json(exclude_unset=True))


async def send_message(uri:str, message: str):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        print(f">>>", message)

        greeting = await websocket.recv()
        print(f"<<< ", greeting)
    
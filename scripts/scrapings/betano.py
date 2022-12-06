from redis_om import Migrator, NotFoundError
from selenium.webdriver.common.by import By
from datetime import datetime, timezone
from core.webdriver import init_driver
from random import randint
from time import sleep
import logging


def page_data(page_url, driver):
    driver.get(page_url)
    sleep(randint(1, 10))
    for elm in driver.find_elements(By.CSS_SELECTOR, '.GTM-event-link.events-list__grid__info__main'):
        url = elm.get_attribute('href').replace('https://', '')
        try: 
            game = Game.get(url)
        except NotFoundError:
            text = elm.find_element(By.CSS_SELECTOR, '*>div').get_attribute('innerText').split('\n')
            game = Game(
                url=url, site='betano.com', sport='futebol',
                firstTeam = text[0],
                secoundTeam = text[1],
                game= ' vs '.join(text),
            )
        else:
            game.lastUpdate = datetime.now(timezone.utc)
        game.save()
        game.expire(60*60*24)
        logging.info(f'✅ {game.__dict__}')
        
        
async def scraping_games():
    driver = init_driver()
    url = 'https://pe.betano.com/sport/futbol/'
    driver.get(url)
    sleep(2)
    logging.info(f'🔗 {url}')
    urls = [elm.get_attribute('href') for elm in driver.find_elements(By.CSS_SELECTOR, '.sb-checkbox__link.sb-checkbox__link__section')]
    
    for url in urls:
        logging.info(f'🔗 {url}')
        page_data(url, driver)
    Migrator().run()
    # close driver
    sleep(5)
    driver.close()
    driver.quit()
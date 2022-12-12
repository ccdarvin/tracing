from selenium.webdriver.common.by import By
from datetime import datetime, timezone
from core.webdriver import init_driver
from core.utils import scroll_down
from core.models import Bet
from time import sleep
from core.models import Game, Website, save, delete, exists
from rich import print
import json



def get_pages(website_id, page_url, driver):
    driver.get(page_url)
    print(f'🔗 {page_url}')
    sleep(10)     
    for elm in driver.find_elements(By.CSS_SELECTOR, '.event-description'):
        first = elm.text.split('vs')[0].strip()
        secound = elm.text.split('vs')[1].strip()
        game = Game(
            id = elm.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'),
            websiteId=website_id,
            urlSource=page_url,
            sport='futbol',
            fullName=f'{first} vs {secound}',
            firstTeam=first,
            secoundTeam=secound
        )
        save(game)
        print(f'✅ {game.__dict__}')


def scraping(website_id):
    driver = init_driver()
    url= 'https://www.dafabet.com/es/dfgoal/sports/240-football'
    print(f'🔗 {url}')
    driver.get(url)
    sleep(10)
    urls = []
    for elm in driver.find_elements(By.CSS_SELECTOR, '.expand .subitems h4.parent a'):
        try:
            urls.append(elm.get_attribute('href'))
        except Exception as e:
           print(e)
    
    for url in urls:
        get_pages(website_id, url, driver)
     
    # close driver
    sleep(10)
    driver.close()
    driver.quit()
    

def get_bets(driver, game, ws):
   raise NotImplementedError
        

def scraping_game(game, ws, bets=False):
    driver = init_driver()
    driver.get(game.id)
    print(f'⚽ {game.id}')
    sleep(10)
    pass
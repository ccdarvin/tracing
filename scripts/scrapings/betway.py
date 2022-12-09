from selenium.webdriver.common.by import By
from datetime import datetime, timezone
from core.webdriver import init_driver
from core.utils import scroll_down
from time import sleep
from core.models import Game, Website, save, delete, exists
from rich import print
import json



def get_pages(website_id, page_url, driver):
    driver.get(page_url)
    print(f'🔗 {page_url}')
    sleep(10)
    
    for elm in driver.find_elements(By.CSS_SELECTOR, '.collapsablePanel'):
        try:
            header_elm = elm.find_element(By.CSS_SELECTOR, '.collapsableHeader')
        except:
            continue
        scroll_down(driver, 'body', 60)
        sleep(1)
        if header_elm.get_attribute('collapsed') == 'true':
            try:
                header_elm.click()
            except:
                pass
            else:
                sleep(3)
                height = (len(elm.find_elements(By.CSS_SELECTOR, '.scoreboardInfoNames')) + 1) * 30
                scroll_down(driver, 'body', height)
        
    
    for elm in driver.find_elements(By.CSS_SELECTOR, '.scoreboardInfoNames'):
        first = elm.text.split('-')[0].strip()
        secound = elm.text.split('-')[1].strip()
        game = Game(
            id = elm.get_attribute('href'),
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
    urls = [
        'https://betway.com/es/sports/ctl/soccer',
        'https://betway.com/es/sports/cpn/soccer/9',
        'https://betway.com/es/sports/cpn/soccer/90',
        'https://betway.com/es/sports/cpn/soccer/118',
        'https://betway.com/es/sports/cpn/soccer/291',
    ]
    for url in urls:
        try:
            get_pages(website_id, url, driver)
        except Exception as e:
            print(e)
     
    # close driver
    sleep(3)
    driver.close()
    driver.quit()
    

def scraping_game(webiste_id, game_id, ws):
    driver = init_driver()
    print(f'⚽ {game_id}')
    driver.get(game_id)
    for index in range(1, 80):
        sleep(1)
        ws.send(json.dumps({'type': 'game', 'data': {'id': game_id, 'index': index}}))
        print(ws.recv())
    driver.close()
    driver.quit()
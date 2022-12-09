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
    

def get_bets(driver, game, ws):
    for elm in driver.find_elements(By.CSS_SELECTOR, '.collapsablePanel'):
        collapsed_elm = elm.find_element(By.CSS_SELECTOR, '.collapsableContent')
        if 'empty' in collapsed_elm.get_attribute('class'):
            try:
                elm.click()
            except:
                pass
        try:
            header_elm = elm.find_element(By.CSS_SELECTOR, '.titleText>.title')
            cashout_elm = elm.find_element(By.CSS_SELECTOR, '.cashOutMarketIndicatorContainer')
        except:
            continue    
        try:
            labels_elms = elm.find_elements(By.CSS_SELECTOR, '.outcomeHeader, .outcomeItemHeader')
            odds_elms = elm.find_elements(By.CSS_SELECTOR, '.oddsDisplay')
        except:
            continue
        
        for labels_elm, odds_elm in zip(labels_elms, odds_elms):
            try:
                group = header_elm.text.strip()
                name = labels_elm.text.strip()
                bet = Bet(
                    id=f'{group}-{name}'.replace(' ', '-').lower(),
                    websiteId=game.websiteId,
                    gameId=game.id,
                    group=group, 
                    name=name, 
                    bet=float(odds_elm.text.replace(',', '.'))
                )
            except Exception as e:
                print('Error', e)
            else:
                ws.send(json.dumps({'type': 'bet', 'data': bet.__dict__}))
                print(ws.recv())
        scroll_down(driver, 'body', 500)
        sleep(10)
        

def scraping_game(game, ws):
    driver = init_driver()
    driver.get(game.id)
    print(f'⚽ {game.id}')
    sleep(5)
    status_code = driver.find_element(By.CSS_SELECTOR, 'meta[http-equiv="status"]').get_attribute('content')
    if status_code == '404':
        delete(game)
        print(f'❌ {game.id}')
        return
    for index in range(1, 20):
        sleep(1)
        ws.send(json.dumps({'type': 'game', 'data': {'id': game.id, 'index': index}}))
        print(ws.recv())
        get_bets(driver, game, ws)
    driver.close()
    driver.quit()
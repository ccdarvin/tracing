from selenium.webdriver.common.by import By
from core.models import Game, Bet, save, delete
from core.webdriver import init_driver
from core.utils import scroll_down
from bs4 import BeautifulSoup
from random import randint
from time import sleep


def get_pages(website_id, page_url, driver):
    driver.get(page_url)
    sleep(randint(2, 5))
    for elm in driver.find_elements(By.CSS_SELECTOR, '.GTM-event-link.events-list__grid__info__main'):
        url = elm.get_attribute('href')
        text = elm.find_element(By.CSS_SELECTOR, '*>div').get_attribute('innerText').split('\n')
        game = Game(
            id=url, 
            websiteId=website_id,
            urlSource=page_url,
            sport='futbol',
            fullName= ' vs '.join(text),
            firstTeam = text[0],
            secoundTeam = text[1],
        )
        save(game)
        print(f'✅ {game.__dict__}')
        
        
def scraping(website_id:str):
    driver = init_driver()
    url = 'https://pe.betano.com/sport/futbol/'
    driver.get(url)
    sleep(2)
    print(f'🔗 {url}')
    urls = [elm.get_attribute('href') for elm in driver.find_elements(By.CSS_SELECTOR, '.sb-checkbox__link.sb-checkbox__link__section')]
    
    for url in urls:
        print(f'🔗 {url}')
        get_pages(website_id, url, driver)
    # close driver
    sleep(5)
    driver.close()
    driver.quit()
    

def get_bets(driver, game, ws):
    def bet_with_scroll():
        for elm in driver.find_elements(By.CSS_SELECTOR, '[role="listitem"]'):
            soup = BeautifulSoup(elm.get_attribute('innerHTML'), 'html.parser')
            group = soup.find('div', class_='markets__market__header__title').get_text()
            group = ' '.join(group.split())
            for soup_b in soup.find_all('button'):
                if soup_b.get_text().split():
                    name = soup_b.find('span', class_='selections__selection__title').get_text()
                    name = ' '.join(name.split())
                    bet = Bet(
                        id= f'{group}_{name}'.replace(' ', '-'),
                        websiteId=game.websiteId,
                        gameId=game.id,
                        group=group,
                        name=name,
                        bet = float(soup_b.find('span', class_='selections__selection__odd').get_text())
                    )
                    print(bet.__dict__)
    for i in range(4):
        try:
            bet_with_scroll()
        except:
            pass
        sleep(1)
        scroll_down(driver, '[role="group"]', 2000)
    sleep(5)
    scroll_down(driver, '[role="group"]', -15000)
    

def scraping_game(game, ws, bets=False):
    driver = init_driver()
    driver = init_driver()
    driver.get(game.id)
    print(f'⚽ {game.id}')
    sleep(5)
    if driver.current_url == 'https://pe.betano.com/live/':
        delete(game)
        print(f'❌ delete {game.id}')
        return
    
    if bets:
        for i in range(100):
            get_bets(driver, game, ws)
    
    sleep(30)
    driver.close()
    driver.quit()
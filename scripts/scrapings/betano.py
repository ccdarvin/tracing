from selenium.webdriver.common.by import By
from core.webdriver import init_driver
from core.models import Game
from time import sleep
from random import randint


def page_data(page_url, driver):
    driver.get(page_url)
    sleep(randint(1, 10))
    for elm in driver.find_elements(By.CSS_SELECTOR, '.GTM-event-link.events-list__grid__info__main'):
        url = elm.get_attribute('href').replace('https://', '')
        text = elm.find_element(By.CSS_SELECTOR, '*>div').get_attribute('innerText').split('\n')
        game = Game(
            url=url, site='betano.com', sport='futebol',
            firstTeam = text[0],
            secoundTeam = text[1],
            game= ' vs '.join(text),
        )
        game.save()
        game.expire(60*60*24)
        print(f'✅ {game.__dict__}')
        
        
def scraping_games():
    driver = init_driver()
    url = 'https://pe.betano.com/sport/futbol/'
    driver.get(url)
    sleep(2)
    print(f'🔗 {url}')
    driver.save_screenshot('games_betano.png')
    urls = [elm.get_attribute('href') for elm in driver.find_elements(By.CSS_SELECTOR, '.sb-checkbox__link sb-checkbox__link__section')]
    
    for url in urls:
        print(f'🔗 {url}')
        page_data(url)
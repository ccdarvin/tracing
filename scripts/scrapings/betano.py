from selenium.webdriver.common.by import By
from core.webdriver import init_driver
from core.models import Game, save
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
    
    
    

def scraping_game(game, ws):
    driver = init_driver()
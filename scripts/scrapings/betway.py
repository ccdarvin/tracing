from selenium.webdriver.common.by import By
from core.webdriver import init_driver
from core.models import Game
from time import sleep
from redis_om import Migrator
from rich import print

def scraping_games():
    driver = init_driver()
    url = 'https://betway.com/es/sports/cat/soccer'
    driver.get()
    sleep(20)
    print(f'🔗 {url}')
    driver.save_screenshot('games_betway.png')
    for elm in driver.find_elements(By.CSS_SELECTOR, '.scoreboardInfoNames'):
        game = Game(
            url = elm.get_attribute('href').replace('https://', ''),
            site ='betway.com',
            sport = 'futbol',
            game = elm.text,
            firstTeam = elm.text.split('-')[0].strip(),
            secoundTeam = elm.text.split('-')[1].strip()
        )
        game.save()
        game.expire(60*60*24*60)
        print(f'✅ {game.__dict__}')
        
    Migrator().run()
    # close driver
    sleep(5)
    driver.close()
    driver.quit()

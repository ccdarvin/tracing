from selenium.webdriver.common.by import By
from core.webdriver import init_driver
from core.utils import scroll_down
from redis_om import Migrator
from core.models import Game
from time import sleep
from rich import print

def scraping_games():
    driver = init_driver()
    url = 'https://betway.com/es/sports/ctl/soccer'
    driver.get(url)
    sleep(20)
    print(f'🔗 {url}')
    
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
        game = Game(
            url = elm.get_attribute('href').replace('https://', ''),
            site ='betway.com',
            sport = 'futbol',
            game = elm.text,
            firstTeam = elm.text.split('-')[0].strip(),
            secoundTeam = elm.text.split('-')[1].strip()
        )
        game.save()
        game.expire(60*60*24)
        print(f'✅ {game.__dict__}')
        
    Migrator().run()
    # close driver
    sleep(5)
    driver.close()
    driver.quit()

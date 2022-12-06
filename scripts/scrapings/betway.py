from selenium.webdriver.common.by import By
from datetime import datetime, timezone
from core.webdriver import init_driver
from core.utils import scroll_down
from core.models import Website, save, exists
from core.utils import send_message_website
from time import sleep
import logging



def get_pages(page_url, driver):
    driver.get(page_url)
    logging.info(f'🔗 {page_url}')
    sleep(20)
    
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
                sleep(5)
                height = (len(elm.find_elements(By.CSS_SELECTOR, '.scoreboardInfoNames')) + 1) * 30
                scroll_down(driver, 'body', height)
        
    
    for elm in driver.find_elements(By.CSS_SELECTOR, '.scoreboardInfoNames'):
        url = elm.get_attribute('href').replace('https://', '')
        try: 
            game = Game.get(url)
        except NotFoundError:            
            game = Game(
                url = url,
                site ='betway.com',
                sport = 'futbol',
                game = elm.text,
                firstTeam = elm.text.split('-')[0].strip(),
                secoundTeam = elm.text.split('-')[1].strip()
            )
        else:
            game.lastUpdate = datetime.now(timezone.utc)
        game.save()
        game.expire(60*60*24)
        logging.info(f'✅ {game.__dict__}')


def scraping():
    driver = init_driver()
    urls = [
        'https://betway.com/es/sports/ctl/soccer',
        'https://betway.com/es/sports/cpn/soccer/9',
        'https://betway.com/es/sports/cpn/soccer/90',
        'https://betway.com/es/sports/cpn/soccer/118',
        'https://betway.com/es/sports/cpn/soccer/291',
    ]
    for url in urls:
        pass
        #page_data(url, driver)
     
    # close driver
    sleep(10)
    driver.close()
    driver.quit()
    
    
    
    
async def main():
    website = Website(id='betway.com', scraping=True)
    save(website)
    await send_message_website(website)
    try:
        scraping()
    except Exception as e:
        logging.exception(e)
    finally:
        website = Website(id='betway.com', scraping=False)
        save(website)
        await send_message_website(website)


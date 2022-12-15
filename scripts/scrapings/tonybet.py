from selenium.webdriver.common.by import By
from scrapings.base import ScrapingBase
from core.models import Game, Bet
from core.models import Bet
from thefuzz import fuzz
from rich import print
from time import sleep

class Scraping(ScrapingBase):
    website_id = 'tonybet'
    
    def get_urls(self) -> list[str]:
        url = 'https://tonybet.com/pe/prematch/football/leagues'
        print(f'🔗 {url}')
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        sleep(15)
        urls = []
        print(self.driver.find_element(By.CSS_SELECTOR, 'html').get_attribute('innerHTML'))
        for elm in self.driver.find_elements(By.CSS_SELECTOR, '.leagues-list-module_itemName__EV6dh'):
            try:
                urls.append(elm.get_attribute('href'))
            except Exception as e:
               print(e)
        return urls
               
    def get_games(self, max_pages:str=None):
        for url in self.get_urls()[:max_pages]:
            print
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            for elm in self.driver.find_elements(By.CSS_SELECTOR, 'a.event-table__col-align '):
                first = elm.text.split('\n')[1].strip()
                secound = elm.text.split('\n')[2].strip()
                game = Game(
                    id = elm.get_attribute('href'),
                    websiteId=self.website_id,
                    urlSource=url,
                    sport='futbol',
                    fullName=f'{first} vs {secound}',
                    firstTeam=first,
                    secoundTeam=secound
                )
                self.save_game(game)
                print(f'✅ {game.__dict__}')
                
    def get_bets(self, url, load=False, ws=None):
        if load:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            
        def __select_click(selector):
            self.driver.implicitly_wait(1)
            try:
                elm = self.driver.find_element(By.CSS_SELECTOR, selector)
            except Exception as e:
                return False
            else:
                elm.click()
            return True
            
            
        def __get_bets(period):
            for elm in self.driver.find_elements(By.CSS_SELECTOR, '[class*=sport-event-table-module_etaSection]'):
                group = elm.find_element(By.CSS_SELECTOR, '[class*=sport-event-markets-header-module_title]').text.strip()
                elms_bet = elm.find_elements(By.CSS_SELECTOR, '[class*=sport-event-table-module_etaCoefficient]')
                if '1x2' in group.lower():
                    self._get_1x2(elm, elms_bet, url, period)
                if fuzz.token_set_ratio('doble oportunidad', group.lower()) > 95:
                    self._get_doble_oportunidad(elm, elms_bet, url, period)
                    
        # regular
        if __select_click('[data-text="Principal"]'):
            __get_bets('regular')
        # Primer tiempo
        if __select_click('[data-text="1er Tiempo"]'):
            __get_bets('primer')
        # Segundo tiempo
        if __select_click('[data-text="2do tiempo"]'):
            __get_bets('segundo')
        
        
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapings.base import ScrapingBase
from core.models import Game, Bet
from thefuzz import fuzz
from time import sleep
from rich import print


class Scraping(ScrapingBase):
    website_id = 'dafabet.com'
    
    def get_urls(self):
        url= 'https://www.dafabet.com/es/dfgoal/sports/240-football'
        print(f'🔗 {url}')
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        urls = []
        for elm in self.driver.find_elements(By.CSS_SELECTOR, '.expand .subitems h4.parent a'):
            try:
                urls.append(elm.get_attribute('href'))
            except Exception as e:
                print(e)
        return urls
    
    def get_games(self, max_pages: str = None):
        for url in self.get_urls()[:max_pages]:
            print(f'🔗 {url}')
            self.driver.get(url)
            self.driver.implicitly_wait(20)
            sleep(20)
            try:
                for elm in self.driver.find_elements(By.CSS_SELECTOR, '.event-description'):
                    text = elm.get_attribute('innerText')
                    first = text.split('vs')[0].strip()
                    secound = text.split('vs')[1].strip()
                    game = Game(
                        id = elm.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'),
                        websiteId=self.website_id,
                        urlSource=url,
                        sport='futbol',
                        fullName=f'{first} vs {secound}',
                        firstTeam=first,
                        secondTeam=secound
                    )
                    self.save_game(game)
                    print(f'✅ {game.__dict__}')
            except Exception as e:
                print(e)
                
    def _show_bets_group(self, elm):
        if 'collapsed' in elm.get_attribute('class'):
            ActionChains(self.driver).scroll_to_element(elm).perform()
            ActionChains(self.driver).click(elm).perform()
            sleep(1)
            # validate
            self._show_bets_group(elm)
                
    def get_bets(self, url, load=False, ws=None):
        if load:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            
        for elm in self.driver.find_elements(By.CSS_SELECTOR, '.markets-group-component'):
            group_elm = elm.find_element(By.CSS_SELECTOR, 'h2')
            elms_bet = elm.find_elements(By.CSS_SELECTOR, '.formatted_price')
            if fuzz.token_set_ratio('Victoria/Empate/Victoria - Tiempo Regular', group_elm.text) > 95:
                self._get_1x2(elm, elms_bet, url, 'regular')
                
            if fuzz.token_set_ratio('Victoria/Empate/Victoria - Primer tiempo', group_elm.text) > 95:
                self._get_1x2(elm, elms_bet, url, 'primer')
            
            if fuzz.token_set_ratio('Victoria/Empate/Victoria - Segundo tiempo', group_elm.text) > 95:
                self._get_1x2(elm, elms_bet, url, 'segundo')
    
                
            if fuzz.token_set_ratio('Doble oportunidad - Tiempo Regular', group_elm.text) > 95:
                self._get_doble_oportunidad(elm, elms_bet, url, 'regular')
                
            if fuzz.token_set_ratio('Doble oportunidad - Primer tiempo', group_elm.text) > 95:
                self._get_doble_oportunidad(elm, elms_bet, url, 'primer')
                
            if fuzz.token_set_ratio('Doble oportunidad - Segundo tiempo', group_elm.text) > 95:
                self._get_doble_oportunidad(elm, elms_bet, url, 'segundo')

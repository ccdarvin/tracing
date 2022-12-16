from core.models import save, Game, Bet
from core.webdriver import init_driver
from core.config import get_settings
from threading import Thread
import websocket
import time
import json
from rich.console import Console

console = Console()


settings = get_settings()


def on_message(ws):
    while True:
        try:
            data = ws.recv()
            print(data)
        except websocket.WebSocketConnectionClosedException:
            print('Connection closed')
            break


class ScrapingBase:
    website_id = None
    ws_bet = None
    use_ws_bet = False
    bets = {}
    
    def __init__(self, headless=True, use_ws_bet=False) -> None:
        self.headless = headless
        self.driver = init_driver(self.headless)
        self.use_ws_bet = use_ws_bet

    @classmethod
    def check_url(self, url):
        if self.website_id not in url:
            return False
        return True

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def save_game(self, game: Game):
        save(game, 24*60*60) 
    
    def get_urls(self):
        raise NotImplementedError
    
    def get_games(self, max_pages:str=None):
        raise NotImplementedError
    
    def get_bets(self, url, load=False):
        raise NotImplementedError
    
    def get_gets_per_period(self, url:str, wait=5):
        """
        Args:
            url (str): _description_
            wait (int, optional): _description_. Defaults to 10 minutes
        """
        self.ws_bet_connect(url)
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        start_time = time.time()
        # run per period of time 
        while time.time() - start_time < wait*60:
            self.get_bets(url)
            time.sleep(10)
            
    def _show_bets_group(self, elm):
        pass
    
    def _get_1x2(self, elm:any, elms_bet: any, url: str, period: str):
        self._show_bets_group(elm)
        for index, bet_elm in enumerate(elms_bet):
            name = '1' if index == 0 else 'X' if index == 1 else '2'
            bet = Bet(
                websiteId=self.website_id,
                gameId = url,
                period = period,
                group='1x2',
                name=name,
                bet=float(bet_elm.text.replace(',', '.')),
            )
            self.ws_send_bet(bet)
        
    def _get_doble_oportunidad(self, elm:any, elms_bet: any, url: str, period: str):
        self._show_bets_group(elm)
        for index, bet_elm in enumerate(elms_bet):
            if index == 1:
                name = 'X2'
            else:
                name = '1X' if index == 0 else '12'
            bet = Bet(
                websiteId=self.website_id,
                gameId = url,
                period = period,
                group='doble-oportunidad',
                name=name,
                bet=float(bet_elm.text.replace(',', '.')),
            )
            self.ws_send_bet(bet)
            
    def ws_send_bet(self, bet: Bet, ws=None):
        if check_bet := self.bets.get(bet.id):
            if check_bet.bet == bet.bet:
                print('bet not sent', bet.json())
                return 
        
        self.bets[bet.id] = bet    
        if self.use_ws_bet:
            #check if ws connect is open
            self.ws_bet.send(json.dumps({
                'type': 'bet',
                'data': bet.dict(),
            }))
        else:
            print('bet not sent', bet.json())
        

    def ws_bet_connect(self, url:str):
        if self.use_ws_bet:
            url = f'{settings.WS}/games/{self.website_id}?game_id={url}'
            #check if ws connect is open
            if self.ws_bet is None:
                self.ws_bet = websocket.WebSocket()
                self.ws_bet.connect(url)
                Thread(target=on_message, args=(self.ws_bet,)).start()

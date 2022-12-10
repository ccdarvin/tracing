from sentry_sdk.integrations.logging import LoggingIntegration
from scrapings.betano import (
    scraping as betano_scraping,
)
from scrapings.betway import (
    scraping as betway_scraping,
    scraping_game as betway_scraping_game,
)
from redis.commands.search.query import Query
from core.config import get_settings
from rich import print
import sentry_sdk
import websocket
import typer
from core.models import r, Game
import json
from random import randint


sentry_sdk.init(
    dsn="https://f7b61367ec5f472eb4b989913b5879b1@o220382.ingest.sentry.io/4504272342155264",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


app = typer.Typer()
settings = get_settings()


@app.command()
def websites(betway: bool=False, betano: bool=False):
    uri = f'{settings.WS}/websites'
    ws = websocket.WebSocket()
    if betway:
        website_id='betway.com'
        ws.connect(f'{uri}?scraping={website_id}')
        print(ws.recv())
        try:
            betway_scraping(website_id)
        except Exception as e:
            raise e      
        
    if betano:
        website_id='betano.com'
        ws.connect(f'{uri}?scraping={website_id}')
        print(ws.recv())
        try:
            betano_scraping(website_id)
        except Exception as e:
            raise e

@app.command()
def games(clean: bool=False):
    
    if clean:
        keys = r.keys('games:*')
        for key in keys:
            r.json().set(key, '.scraping', False)
        print(f'Cleaned {len(keys)} games')
        return
    
    docs = r.ft('idxGames').search(Query('@scraping:{false}').sort_by('lastScraping')).docs
    r.close()
    if len(docs) == 0:
        print('No games to scrape')
        return
    
    doc = docs[randint(0, len(docs)-1)]
    game = Game(**json.loads(doc.json))
    ws = websocket.WebSocket()
    uri = f'{settings.WS}/games/{game.websiteId}?game_id={game.id}'
    ws.connect(uri)
    print(ws.recv())
    if game.websiteId == 'betway.com':
        betway_scraping_game(game, ws)
    else:
        print('No scraping for this website')
    ws.close()

if __name__ == "__main__":
    app()
from sentry_sdk.integrations.logging import LoggingIntegration
#from scrapings.betano import scraping_games as betano_scraping
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


sentry_sdk.init(
    dsn="https://f7b61367ec5f472eb4b989913b5879b1@o220382.ingest.sentry.io/4504272342155264",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


app = typer.Typer()
settings = get_settings()

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")


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
            
        
    #if betano:
    #    await betano_scraping()
    #asyncio.run(main())

@app.command()
def games():
    docs = r.ft('idxGames').search(Query('@scraping:{false}').paging(0, 1)).docs
    r.close()
    for doc in docs:
        game = Game(**json.loads(doc.json))
        print(game)
        ws = websocket.WebSocket()
        uri = f'{settings.WS}/games/{game.websiteId}?game_id={game.id}'
        ws.connect(uri)
        print(ws.recv())
        if game.websiteId == 'betway.com':
            betway_scraping_game(game, ws)
        

if __name__ == "__main__":
    app()
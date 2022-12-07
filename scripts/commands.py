from sentry_sdk.integrations.logging import LoggingIntegration
#from scrapings.betano import scraping_games as betano_scraping
from scrapings.betway import scraping as betway_scraping
from datetime import datetime, timezone
from core.config import get_settings
import sentry_sdk
import websocket
import logging
import typer
import json
from rich import print


logging.basicConfig(
    level=logging.INFO, 
    filename="jobs.log",
    filemode="w",
    format='%(name)s %(asctime)s %(levelname)s %(message)s'
)

sentry_logging = LoggingIntegration(
    #level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn="https://f7b61367ec5f472eb4b989913b5879b1@o220382.ingest.sentry.io/4504272342155264",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    integrations=[
        sentry_logging,
    ],
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
        ws.connect(f'{uri}?scraping=betway.com')
        try:
            betway_scraping()
        except Exception as e:
            raise e
            
        
    #if betano:
    #    await betano_scraping()
    #asyncio.run(main())

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
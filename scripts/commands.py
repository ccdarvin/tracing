from sentry_sdk.integrations.logging import LoggingIntegration
#from scrapings.betano import scraping_games as betano_scraping
from scrapings.betway import scraping as betway_scraping
from core.config import get_settings
from rich import print
import sentry_sdk
import websocket
import typer

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
        try:
            betway_scraping(website_id)
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
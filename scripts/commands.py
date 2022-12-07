from sentry_sdk.integrations.logging import LoggingIntegration
#from scrapings.betano import scraping_games as betano_scraping
from scrapings.betway import main as betway_scraping
import sentry_sdk
import asyncio
import logging
import typer


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


@app.command()
def websites(betway: bool=False, betano: bool=False):
    async def main():
        if betway:
            await betway_scraping()
        #if betano:
        #    await betano_scraping()
    asyncio.run(main())

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
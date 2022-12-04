from sentry_sdk.integrations.logging import LoggingIntegration
from scrapings.betano import scraping_games as betano
from scrapings.betway import scraping_games as betway
import sentry_sdk
import threading
import schedule
import logging
import time
logging.basicConfig(
    level=logging.INFO, 
    filename="jobs_log.log",
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


def job():
    print('I am working...')
    

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
    

schedule.every(15).to(20).minutes.do(run_threaded, betano)
schedule.every(10).to(15).minutes.do(run_threaded, betway)
schedule.every(60).seconds.do(run_threaded, job)

while 1:
    schedule.run_pending()
    time.sleep(1)

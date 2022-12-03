import threading
import time
import schedule
from scrapings.betano import scraping_games as betano
from scrapings.betway import scraping_games as betway


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
    

schedule.every(3).to(5).hours.do(run_threaded, betano)
schedule.every(2).to(5).hours.do(run_threaded, betway)


while 1:
    schedule.run_pending()
    time.sleep(1)
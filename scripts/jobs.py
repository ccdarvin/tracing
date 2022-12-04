import threading
import time
import schedule
from scrapings.betano import scraping_games as betano
from scrapings.betway import scraping_games as betway


def job():
    print('I am working... %s' % time.ctime())

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
    

schedule.every(1).to(3).hours.do(run_threaded, betano)
schedule.every(1).to(3).hours.do(run_threaded, betway)
schedule.every(1).minutes.do(run_threaded, job)


while 1:
    schedule.run_pending()
    time.sleep(1)
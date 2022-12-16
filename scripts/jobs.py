from core.models import r, RelatedGame, Game, save
from scrapings.base import ScrapingBase
from rich.console import Console
from multiprocessing import Pool
from scrapings import tonybet
from scrapings import dafabet
from thefuzz import fuzz
from time import sleep
from rich import print
import typer
from rich.tree import Tree

console = Console()


app = typer.Typer()


scraping_classes: list[ScrapingBase] = [
    dafabet.Scraping,
    tonybet.Scraping,
]


@app.command()
def games(headless: bool = False):
    for scraping_class in scraping_classes:
        scraping = scraping_class()
        try:
            scraping.get_games()
        except Exception as e:
            console.print_exception(show_locals=True)
        
        scraping.quit()
        sleep(30)


@app.command()
def related():
    docs = r.json().mget(r.keys('games:*'), '.')
    for doc in docs:
        related = {
            'name': doc['fullName'],
            'related': [doc]
        }
        docs.remove(doc)
        for _doc in docs:
            ratio = fuzz.ratio(related['name'], _doc['fullName'])
            if ratio > 90:
                related['related'].append(_doc)
                docs.remove(_doc)
            elif ratio > 60:
                first_ratio = fuzz.token_set_ratio(doc['firstTeam'], _doc['firstTeam'])
                second_ratio = fuzz.token_set_ratio(doc['secondTeam'], _doc['secondTeam'])
                if first_ratio > 90 and second_ratio > 90:
                    related['related'].append(_doc)
                    docs.remove(_doc)

        related['count'] = len(related['related'])
        related['id'] = related['name'].replace(' ', '-')
        if len(related['related']) > 1:
            tree = Tree(f"{related['name']} - {related['count']}")
            related_obj = RelatedGame(**related)
            save(related_obj, 12*60*60)
            for doc in related['related']:
                game = Game(**doc)
                tree.add(game.key())
                r.json().set(game.key(), '.relatedKey', related_obj.key())
            print(tree)


def scraping_page(doc):
    game = Game(**doc)
    url = game.id
    for scraping_class in scraping_classes:
        if scraping_class.check_url(url):
            try:
                scraping = scraping_class(use_ws_bet=True)
                scraping.get_gets_per_period(url)
                scraping.quit()
            except Exception as e:
                console.print_exception(show_locals=True)
            finally:
                scraping.quit()
                break


@app.command()
def bets():
    keys = r.keys('related:*')
    docs = r.json().mget(keys, '.')
    for doc in docs:
        if doc['scraping']:
            continue
        with Pool(doc['count']+1) as p:
            p.map(scraping_page, doc['related'])
        
            
if __name__ == "__main__":
    app()

from scrapings.betano import scraping_games as betano_scraping
from scrapings.betway import scraping_games as betway_scraping
import typer



app = typer.Typer()


@app.command()
def games(betway: bool=False, betano: bool=False):
    if betway:
        betway_scraping()
    elif betano:
        betano_scraping()
    else:
        typer.echo("No command selected")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
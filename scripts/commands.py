from scrapings.betano import scraping_games as betano_scraping
from scrapings.betway import main as betway_scraping
import asyncio
import typer



app = typer.Typer()


@app.command()
def websites(betway: bool=False, betano: bool=False):
    async def main():
        if betway:
            await betway_scraping()
        if betano:
            await betano_scraping()
    asyncio.run(main())

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
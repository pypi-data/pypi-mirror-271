import os

import typer

import omie

app = typer.Typer()


@app.command()
def test(name: str):
    api = omie.OmieClient(
        os.getenv('OMIE_APP_KEY'),
        os.getenv('OMIE_APP_SECRET'),
    )
    print()

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

def main():
    app()

if __name__ == "__main__":
    main()
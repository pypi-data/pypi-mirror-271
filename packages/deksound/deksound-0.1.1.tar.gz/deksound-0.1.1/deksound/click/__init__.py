import typer
from ..core import play_file, play_res

app = typer.Typer(add_completion=False)


@app.command()
def play(path):
    play_file(path)


@app.command()
def notify(name, path=None):
    play_res(name, path)

import click
import pyperclip
import requests
from bs4 import BeautifulSoup


@click.command()
@click.argument("lection", type=int)
@click.option("-p", "--port", type=int, default=8000)
def cli(lection: int, port: int):
    url = f"http://localhost:{port}/tema-{lection}"
    try:
        res = requests.get(url)
        res.raise_for_status()
    except (requests.ConnectionError, requests.HTTPError) as exc:
        raise click.ClickException("HTTPException: " + str(exc))

    soup = BeautifulSoup(res.content.decode("utf8"), "html.parser")
    content = soup.find("article")
    if content is None:
        raise click.ClickException("Can't process request data")
    pyperclip.copy(content.text)
    print("Copied redered text")


if __name__ == "__main__":
    cli()

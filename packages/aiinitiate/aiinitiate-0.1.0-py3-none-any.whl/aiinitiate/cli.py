import typer

app = typer.Typer()


@app.command()
def logo():
    logo = """
    █████  ██ ███████ ██ ███    ██ ██ ████████ ██  ██████  ███    ██ 
    ██   ██ ██ ██      ██ ████   ██ ██      ██    ██    ██  ████   ██ 
    ███████ ██ ███████ ██ ██ ██  ██ ██    ██    ██    ██ ██ ██ ██  ██ 
    ██   ██ ██      ██ ██ ██  ██ ██ ██    ██    ██    ██ ██ ██  ██ ██ 
    ██   ██ ██ ███████ ██ ██   ████ ██    ██     ██████  ██ ██   ████ 
    """
    typer.echo(logo)


@app.command()
def main():
    logo()
    typer.echo("Welcome to AIInitiate command!")


if __name__ == "__main__":
    app()

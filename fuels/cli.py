import click
from fuels import FuelsBot

@click.group()
@click.option("--path_to_creds", type = click.STRING, default = "TelegramBotCreds.json", help = "path to bot creds", show_default=True)
def cli(path_to_creds: str):
    bot = FuelsBot(path_to_creds)
    bot.main()

@cli.command(name="run")
def run() -> None:
    pass

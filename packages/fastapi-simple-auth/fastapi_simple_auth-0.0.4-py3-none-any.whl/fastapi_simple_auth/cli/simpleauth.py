import os
import typer
import click
from rich.console import Console
from typing_extensions import Annotated
from sqlalchemy import create_engine
import alembic

from ..models import User, Code
from ..db import SessionLocal
from ..cron import cron
from ..settings import settings
from .. import package_path

err_console = Console(stderr=True)

panel_local="Local commands"

app = typer.Typer(pretty_exceptions_show_locals=False, 
    # rich_markup_mode="rich"
    no_args_is_help=True,                
    rich_markup_mode="markdown"
    )
err_console = Console(stderr=True)


@app.callback(
        context_settings={"help_option_names": ["-h", "--help"]})
def callback(ctx: typer.Context,
    ):
    """
    Client for FastAPI Simple Auth
    """
    global db
    
    db = SessionLocal()


@app.command(rich_help_panel=panel_local,
             help='List all users')
def users():
    for user in db.query(User).all():
        print(user)

@app.command(rich_help_panel=panel_local,
             help='List all codes')
def codes():
    for code in db.query(Code).all():
        print(code)

@app.command("cron", rich_help_panel=panel_local,
             help='Run cron job once')
def clicron():
    cron(force=True)

@app.command("dbupgrade", rich_help_panel=panel_local,
             help='upgrade/create db (alembic upgrade head)')
def upgrade_head():

    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("sqlalchemy.url", settings.db_url)
    alembic_cfg.set_main_option("script_location", os.path.join(package_path(), "alembic"))

    print("Doing 'upgrade head'...")
    engine = create_engine(settings.db_url)
    with engine.connect() as connection:
        alembic_cfg.attributes['connection'] = connection
        from alembic import command
        command.upgrade(alembic_cfg, "head")



def main():
    global exact
    command = typer.main.get_command(app)

    try:
        rc = command(standalone_mode=False)

    except click.ClickException as e:
        err_console.print(e)

    except Exception as e:
        err_console.print(type(e))
        err_console.print(f"Got unexpected exception: {e}")


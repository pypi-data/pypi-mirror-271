import subprocess
import click
from click.testing import CliRunner
import os
import aise_toolkit_demo
from aise_toolkit_demo.app import app_utiles

@click.group()
@click.version_option(version='0.5')
def cli():
    "A set of tools to assist developer to use AI"

@cli.command(name="command")
@click.argument(
    "example"
)
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def first_command(example, option):
    "Command description goes here"
    click.echo(f"Here is some output: {aise_toolkit_demo.get_message()}")
    click.echo(f"Here is some output: {aise_toolkit_demo.calculate()}")
    click.echo(f"Here is some output: {app_utiles.app_get_message()}")
    click.echo(f"Here is some output: {app_utiles.app_calculate()}")

@cli.command(name="start_app")
def start_app():
    """Start the Streamlit app from ./app/app.py"""
    # Path to your Streamlit script

    # get the current directory
    current_dir = os.getcwd()
    click.echo(current_dir)

    # Path to the Streamlit app
    app_path = os.path.join(current_dir, "aise_toolkit_demo", "app", "app.py")
    click.echo(app_path)

    # Run the Streamlit app
    subprocess.run(["streamlit", "run", app_path])

if __name__ == "__main__":
    cli()

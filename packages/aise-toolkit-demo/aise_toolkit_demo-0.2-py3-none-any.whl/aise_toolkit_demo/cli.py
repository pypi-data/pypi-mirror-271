import click

@click.group()
@click.version_option(version='aise, 0.1.1')
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
    click.echo("Here is some output")

if __name__ == "__main__":
    cli()

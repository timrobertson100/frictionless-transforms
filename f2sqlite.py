import click
from datapackage import Package

from helpers import package_to_sqlite


@click.command()
@click.argument('input_package_path', type=click.Path(exists=True))
@click.argument('database_path', type=click.Path(file_okay=True, writable=True, resolve_path=True))
def cli(input_package_path: str, database_path: str):
    input_package = Package(input_package_path)
    package_to_sqlite(input_package, f"sqlite:///{database_path}")

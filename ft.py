import click
from datapackage import Package

# https://github.com/frictionlessdata/datapackage-py/issues/273
# Is it https://github.com/openknowledge-archive/datapackage-storage-py ??
from helpers import package_to_sqlite, sqlpackage_to_disk


@click.command()
@click.argument('input_package_path', type=click.Path(exists=True))  # TODO: accept URL in addition to local directory?
@click.argument('transform_dir_path', type=click.Path(exists=True))
@click.argument('output_package_path', type=click.Path(exists=False))
def cli(input_package_path: str, transform_dir_path: str, output_package_path: str):
    """Reshape a (frictionless) data package."""
    click.echo("Opening the source data package and loading into SQLite...")
    engine = package_to_sqlite(Package(input_package_path))

    click.echo("Processing transformations...")
    with engine.connect() as con:
        rs = con.execute("UPDATE data SET name = UPPER(name)")

    click.echo("Saving the transformed data")
    package_from_sql = Package(storage='sql', engine=engine)
    sqlpackage_to_disk(package_from_sql, output_package_path)

    click.echo("Done.")

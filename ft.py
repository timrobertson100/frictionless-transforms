import glob
import importlib
import os
from pathlib import Path

import click
from datapackage import Package

# https://github.com/frictionlessdata/datapackage-py/issues/273
# Is it https://github.com/openknowledge-archive/datapackage-storage-py ??
from helpers import package_to_sqlite, sqlpackage_to_disk, natural_sort

PREPROCESSING_MODULE = "preprocessing"

@click.command()
@click.argument('input_package_path', type=click.Path(exists=True))  # TODO: accept URL in addition to local directory?
@click.argument('transform_dir_path', type=click.Path(exists=True))
@click.argument('output_package_path', type=click.Path(exists=False))
def cli(input_package_path: str, transform_dir_path: str, output_package_path: str):
    """Reshape a (frictionless) data package."""
    click.echo("Opening the source data package...")
    input_package = Package(input_package_path)

    try:
        preprocessing = importlib.import_module(f"{transform_dir_path}.{PREPROCESSING_MODULE}")
        click.echo("Data preprocessing...")
        input_package = preprocessing.process(input_package)
    except ModuleNotFoundError:
        click.echo("No preprocessing module found, skipping")

    click.echo("Load into SQLite...")
    engine = package_to_sqlite(input_package)

    with engine.connect() as con:
        transformation_files = natural_sort(glob.glob(os.path.join(transform_dir_path, '*.sql')))
        for transformation_file in transformation_files:
            click.echo(f"Processing transformation: {transformation_file}")
            con.execute(Path(transformation_file).read_text())

    click.echo("Saving the transformed data...")
    package_from_sql = Package(storage='sql', engine=engine)
    sqlpackage_to_disk(package_from_sql, output_package_path)

    click.echo("Done.")


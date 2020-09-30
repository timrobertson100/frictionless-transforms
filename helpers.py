import csv
import os
import re

import sqlalchemy
from datapackage import Package


def _table_to_csv(engine: sqlalchemy.engine.base.Engine, table_name: str, file_path: str):
    with open(file_path, 'w') as fh:
        outcsv = csv.writer(fh)

        with engine.connect() as con:
            records = con.execute(f"SELECT * FROM {table_name}")
            outcsv.writerow(records.keys())
            outcsv.writerows(records)


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)


def sqlpackage_to_disk(package: Package, output_path: str):
    """Get a package whose storage is SQL and save it to a self-contained data package on disk"""
    # 1. Create a target directory
    os.mkdir(output_path)

    # 2. Create a CSV file for each resource
    for resource in package.resources:
        engine = resource._Resource__storage._Storage__connection.engine
        table_name = resource.source

        _table_to_csv(engine, table_name, os.path.join(output_path, f"{table_name}.csv"))

    # 3. Generate a descriptor
    output_package = Package()
    output_package.infer(f"{output_path}/*.csv")
    output_package.save(os.path.join(output_path, "datapackage.json"))


def package_to_sqlite(package: Package) -> sqlalchemy.engine.base.Engine:
    """Get a package (freshly loaded from disk) and store it in a in-memory SQLite instance

    The SQLAlchemy engine is returned
    """
    engine = sqlalchemy.create_engine('sqlite://')  # We currently create db in memory. Make that configurable?
    package.save(storage='sql', engine=engine)
    return engine
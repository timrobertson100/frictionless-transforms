# frictionless-transforms

A scratch area for collaborating on Frictionless data transforms.

Initial design objective:

- A simple framework that allows a transformation to be applied to reshape a Frictionless data package. 
- Attention to detail on documentation
- Ability to use different transforms
- Runnable on "laptop scale" data (v1) 

It currently consists of two scripts:

- `ft`
- `f2sqlite`
    
## Installation

Clone the repository, create a Python virtual environment, then install the package:

```
$ pip install --editable . 
```

## How to use 

### ft: Whole pipeline

To run the pipeline, you'll need:

- an input package (to be transformed)
- a transformation directory (contains the transformation scripts)

```
$ ft <input_package_path> <transform_dir_path> <output_package_path>
```
    
For example with the included sample data:
    
```
$ cd datasets/periodic_table
$ ft data/raw/datapackage.json transforms data/processed/
```

The transformation directory may contains:

- multiple numbered (execution order) SQL scripts, with a .sql extension
- a `postprocessing.py` file that must implement a single function: `postprocess_database(connection)`

### f2sqlite: Data package to sqlite conversion script

```
$ f2sqlite data/raw/datapackage.json data/interim/periodic_table.sqlite3
```

## Run in Docker

The `ft` and `f2sqlite` scripts can also be run in Docker if you don't have a Python ecosystem available:

- First, clone this repository
- Then, build the `ft` the Docker image (to be done only once after each code change):


    $  docker build -t ft .
- You can then run the scripts (only the local `mnt` subdirectory is accessible to the Docker container). Small bash scripts are 
provided to make things simpler: 


    $ ./ft-docker mnt/sample_input_packages/periodic-table/datapackage.json mnt/sample_transform_dir mnt/output_package
    $ ./f2sqlite-docker sample_input_packages/periodic-table/datapackage.json mnt/mydb.sqlite3
    
If the bash scripts don't work for you (e.g. on Windows), you'll have to use longer commands:

    $ docker run --rm -it -v %cd%/mnt:/usr/src/app/mnt ft /usr/src/app/mnt/sample_input_packages/periodic-table/datapackage.json /usr/src/app/mnt/sample_transform_dir /usr/src/app/mnt/output-package    


## Development notes  

### Lessons learned

- Thanks to the frictionless ecosystem, it's straightforward to load a tabular data package into SQLite (and to 
apply transformations there). It seems less straightforward for the last step (get data back from SQLite) to a 
self-contained data package. Possible approaches:
    - roll our own solution (that's what we do now, in a quick and dirty way)
    - wait for the ecosystem to provide it (https://github.com/frictionlessdata/frictionless-py/issues/439)
    - revive deprecated tools (jttsql/datapackage-storage-py? see: https://gist.github.com/vitorbaptista/19d476d99595584e9ad5)
- A [datapackage pipeline](https://github.com/frictionlessdata/datapackage-pipelines) tool already exists, would it 
work for us?
- It seems [datapackage-py](https://github.com/frictionlessdata/datapackage-py) is getting replaced by the 
[Frictionless Framework](https://github.com/frictionlessdata/frictionless-py). Looks like a great option for the future, 
but it currently appears under heavy development (not much documentation, changing API, not yet battle-tested, ...)
    
### Pending questions (move to GitHub issues)

- intermediate (for data transformation/reshape) format ? **SQLite** for the first POC. **PostgreSQL** might be more 
scalable and available "for free" thanks to https://github.com/frictionlessdata/datapackage-pipelines-sql-driver 
(which relies on SQLAlchemy). A **Python/Pandas** transformation feature can be easily implemented: no data 
transformation needed, so it's just a matter a defining a clean interface (parameters and return value of a 
transformation function?)
- What about logging and error reporting:
    - it would be good that the tool reports messages in both human-readable (for interactive use) and 
    machine-readable (to use in non interactive pipelines) format.
    - basic: return code of the CLI tool (O if transformation was successful)
    - meaningful warning/error messages.
    - should the data transformation code (SQL at first) be also able to emit its own warning and errors? 
    How to capture those?

### Testing

### Type annotations




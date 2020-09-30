# frictionless-transforms
A scratch area for collaborating on Frictionless data transforms.

Initial design objective: 
  - A simple framework that allows a transformation to be applied to reshape a Frictionless data package. 
  - Attention to detail on documentation
  - Ability to use different transforms
  - Runable on "laptop scale" data (v1) 

## POC Installation

Clone the repository, create a Python virtual environment, then install the package:

    $ pip install --editable . 
    
## How to use 

To run the pipeline, you'll need:

- an input package (to be transformed)
- a transformation directory (contains the transformation scripts)


    $ ft <input_package_path> <transform_dir_path> <output_package_path>
    
For example with the included sample data:
    
    $ ft ./sample_input_packages/periodic-table/datapackage.json sample_transform_dir ./output_package

## (POC) development notes  

### TODO
- Second script to execute the first step (load into SQLite) only?
- pre/post process steps using Python (optional Pandas?)

### Current issues
- The database -> datapackage step is a quick and dirty hack:
    - extra files (not data nor datapackage.json) are lost in the process
    - what about performance for large files?
    - are foreign keys kept?

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
- Use Docker for easier execution? (end-users not familiar with Python)

### Configuration

- Idea: make it configurable if needed, but let's provide sensible default so it can be run with just
    - input (file/directory)
    - transformation (file/directory)
    - output (file/directory)
    
### Dependencies and requirements

I'd like to keep this as limited as possible, for maintenance and ease of installation reasons:

- Python 3.8+
- click to create the CLI
- https://github.com/frictionlessdata/datapackage-pipelines-sql-driver for the SQL data transformation

Note: the official frictionless packages (datapackage, tableschema-sql, ...) seems to have themselves tons of 
dependencies...

### Testing

### Type annotations




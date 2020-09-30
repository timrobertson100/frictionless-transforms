from setuptools import setup

setup(
    name='frictionless-transforms',
    version='0.1',
    py_modules=['ft'],
    # TODO: test it installs and work fine in a fresh virtualenv
    install_requires=[
        'click==7.1.2',
        'datapackage==1.15.1',
        'tableschema-sql==1.3.1'
    ],
    entry_points='''
        [console_scripts]
        ft=ft:cli
    ''',
)
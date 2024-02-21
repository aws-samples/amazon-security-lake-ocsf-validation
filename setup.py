#!/usr/bin/python

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

    
setup(
    name='Validate OCSF Schema',
    version='1.0.0',
    description='Validation Script For AWS Security Lake - OCSF Versions: 1.0.0-rc.2, 1.1.0',
    long_description=readme,
    author='Adam Plotzker',
    author_email='adplotzk@amazon.com',
    url='https://github.com/aws-samples/amazon-security-lake',
    license=license,
    
    requires=[
        'path',
        'pathlib',
        'jsonschema',
        'pandas',
        'urllib3',
        'pyarrow',
        'inquirer',
        'requests'
    ],
    packages=find_packages(exclude=('tests', 'docs'))
)








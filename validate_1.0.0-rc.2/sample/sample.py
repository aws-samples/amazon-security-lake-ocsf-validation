#!/usr/bin/python
# -*- coding: utf-8 -*-

from pathlib import Path
import re
import jsonschema
import pandas as pd
import json
import os
import sys
import urllib.request
import requests
import argparse
from argparse import ArgumentParser, RawTextHelpFormatter
import inquirer


answers = {}

# Take in input arguments from CLI
parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show help.')
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-i', '--input', help='Path to directory containing parquet files.', required=True)
requiredNamed.add_argument('-version', help='User Specified OCSF Version.', required=False)
args = vars(parser.parse_args())

if not args['version']:
    questions = [inquirer.List('version', choices=['ocsf_schema_1.0.0-rc.2'])]
    answers = inquirer.prompt(questions)
    answers['version'] = answers['version']
else:
    answers['version'] = args['version']

answers['path'] = args['input']

# Check that input argument is a valid directory
if answers['version'] not in ['ocsf_schema_1.0.0-rc.2']:
    print('\033[1;91m' + '\nThe input specified is not a valid OCSF version.' + '\033[0m')
    exit()

# Check that input argument is a valid directory
if not os.path.isdir(answers['path']):
    print('\033[1;91m' + '\nThe input specified is not a valid directory.' + '\033[0m')
    exit()

if not bool(sorted(Path(answers['path']).glob('*.parquet'))):
    print('\033[1;91m' + '\nThe input directory contains no parquet files.' + '\033[0m')
    exit()

print(answers)


def main():

    """
    # The main function in this script will take a users input
    # '-i /path/to/some/file/file.parquet' and search for parquet
    # files within this specified directory. These files will be
    # converted to JSON format, cleaned using symantic filters,
    # and finally the schema on that JSON will be validated against
    # the set of schema files in /ocsf_schema_1.0.0-rc.2 to determine
    # if the schema is valid OCSF
    """

    def recursive_filter(item, *forbidden):

        """
        This is a function which takes in a JSON object
        and a filter key. The function will recursivly iterate
        though the JSON object and remove all instances of that key.
        """

        if isinstance(item, list):
            return [recursive_filter(entry, *forbidden) for entry in
                    item if entry not in forbidden]
        if isinstance(item, dict):
            result = {}
            for (key, value) in item.items():
                value = recursive_filter(value, *forbidden)
                if key not in forbidden and value not in forbidden:
                    result[key] = value
            return result
        return item

    # Store the absolute path of this script in path variable
    path = Path(os.path.abspath(__file__))

    # Recursive search for all files with .parquet extension in input directory path
    pathlist = Path(answers['path']).glob('*.parquet')

    # Iterate through pathlist containing all of the .parquet files
    for file in pathlist:

        key_vals = []
        EVENT = {}
        SCHEMA_CLASS = ''

        (name, ext) = str(file).split('.parquet')
        new_path = '{}.{}'.format(name, 'json')

        # Use pandas dataframes to convert the parquet file at each iter to a JSON object
        df = pd.read_parquet(file)
        df.to_json(new_path)

        # Write JSON object data to empty json file
        with open(new_path, 'r') as testData:
            testData = json.load(testData)

            # Load schema definition file from ocsf_schema_1.0.0-rc.2 based on OCSF class_uid
            if str(testData['class_uid']['0']) == '1001':
                SCHEMA_CLASS = 'file_activity'

            if str(testData['class_uid']['0']) == '1002':
                SCHEMA_CLASS = 'kernal_extension'

            if str(testData['class_uid']['0']) == '1003':
                SCHEMA_CLASS = 'kernel_activity'

            if str(testData['class_uid']['0']) == '1004':
                SCHEMA_CLASS = 'memory_activity'

            if str(testData['class_uid']['0']) == '1005':
                SCHEMA_CLASS = 'module_activity'

            if str(testData['class_uid']['0']) == '1006':
                SCHEMA_CLASS = 'scheduled_job_activity'

            if str(testData['class_uid']['0']) == '1007':
                SCHEMA_CLASS = 'process_activity'

            if str(testData['class_uid']['0']) == '1008':
                SCHEMA_CLASS = 'registry_key_activity'

            if str(testData['class_uid']['0']) == '1009':
                SCHEMA_CLASS = 'registry_value_activity'

            if str(testData['class_uid']['0']) == '1010':
                SCHEMA_CLASS = 'resource_activity'

            if str(testData['class_uid']['0']) == '2001':
                SCHEMA_CLASS = 'security_finding'

            if str(testData['class_uid']['0']) == '3001':
                SCHEMA_CLASS = 'account_change'

            if str(testData['class_uid']['0']) == '3002':
                SCHEMA_CLASS = 'authentication'

            if str(testData['class_uid']['0']) == '3003':
                SCHEMA_CLASS = 'authorization'

            if str(testData['class_uid']['0']) == '3004':
                SCHEMA_CLASS = 'entity_management'

            if str(testData['class_uid']['0']) == '3005':
                SCHEMA_CLASS = 'api_activity'

            if str(testData['class_uid']['0']) == '4001':
                SCHEMA_CLASS = 'network_activity'

            if str(testData['class_uid']['0']) == '4002':
                SCHEMA_CLASS = 'http_activity'

            if str(testData['class_uid']['0']) == '4003':
                SCHEMA_CLASS = 'dns_activity'

            if str(testData['class_uid']['0']) == '4004':
                SCHEMA_CLASS = 'dhcp_activity'

            if str(testData['class_uid']['0']) == '4005':
                SCHEMA_CLASS = 'rdp_activity'

            if str(testData['class_uid']['0']) == '4006':
                SCHEMA_CLASS = 'smb_activity'

            if str(testData['class_uid']['0']) == '4007':
                SCHEMA_CLASS = 'ssh_activity'

            if str(testData['class_uid']['0']) == '4008':
                SCHEMA_CLASS = 'ftp_activity'

            if str(testData['class_uid']['0']) == '5001':
                SCHEMA_CLASS = 'inventory_info'

            if str(testData['class_uid']['0']) == '5002':
                SCHEMA_CLASS = 'config_state'

            # If class_uid is not specified within the JSON exit script
            if str(testData['class_uid']['0']) is None:
                print('\033[1;91m' + 'No schema found for:', testData['class_uid']['0'])
                exit()

            print('\nValidating Against Event Class: ' + SCHEMA_CLASS + ' (' + str(testData['class_uid']['0']) + ')...\n')

            with open(str(path.parent.parent).replace('\\', '/')
                      + '/' + answers['version']+'/' + SCHEMA_CLASS
                      + '.json', 'r') as ocsf_schema:
                ocsf_schema = json.load(ocsf_schema)

            # Instatiate JSON validator
            validator = jsonschema.Draft7Validator(ocsf_schema)

            for keys in testData.keys():
                key_vals.append(keys)

            # Get clean JSON data object by grabbing first event & correcting typing from .parquet
            for i in key_vals:
                K = i
                V = testData[i]['0']
                if K == 'data':
                    V = str(V).replace('"', "'")
                if K == 'raw_data':
                    V = str(V).replace('"', "'")
                EVENT[K] = V

            # Remove None types from JSON object
            EVENT = json.dumps(EVENT)
            EVENT = json.loads(EVENT)
            EVENT = recursive_filter(EVENT, None)
            EVENT = recursive_filter(EVENT, 'None')

            # Run iterative validation against EVENT
            errors = validator.iter_errors(EVENT)

        output = []

        try:

            # Clean JSON file
            os.remove(new_path)

            # Save errors from iterator
            for error in errors:
                output.append(str(error))

            # Print event data and validation errors
            if output == []:
                print('\033[1;32m' + '-----------------------------------FILE DATA-----------------------------------' + '\033[0m')
                print('\033[1;32m' + json.dumps(EVENT, indent=6) + '\n' + '\033[0m')
                print('\033[1;32m' + '---------------------------------------------------------------------------\n' + '\033[0m')
                print('\033[1;32m' + 'VALID OCSF.\n' + '\033[0m')
            else:
                print('\033[1;91m' + '-----------------------------------FILE DATA-----------------------------------' + '\033[0m')
                print('\033[1;91m' + json.dumps(EVENT, indent=6) + '\n' + '\033[0m')
                print('\033[1;91m' + '---------------------------------------------------------------------------\n' + '\033[0m')
                print('\033[1;91m' + 'INVALID OCSF.\n' + '\033[0m')
                for i in output:
                    print('\033[1;91m' + i + '\033[0m')
        except NameError:

            print('\033[1;91m' + 'Please place a parquet file in the input directory.' + '\033[0m')


if __name__ == '__main__':

    main()

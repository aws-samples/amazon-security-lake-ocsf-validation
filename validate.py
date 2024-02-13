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
from pathlib import Path
import glob

answers = {}

# Take in input arguments from CLI
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show help.')
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-i', '--input', help='Path to directory containing parquet files.', required=True)
requiredNamed.add_argument('-version', help='User Specified OCSF Version.', required=False)
requiredNamed.add_argument('-verbose', help='Set as true for verbose output.', required=False)
requiredNamed.add_argument('-filetype', help='Set as json or parquet.', required=False)
requiredNamed.add_argument('-eventclass', help='Set as OCSF event class.', required=False)
requiredNamed.add_argument('-profiles', help='Set as comma seperated list of profiles used.', required=False)
args = vars(parser.parse_args())

#If version not specified at runtime inquire
if not args['version']:
    print("Select the OCSF schema version to validate against")
    questions = [inquirer.List('version', choices=['1.0.0-rc.2', '1.1.0'])]
    answers['version'] = inquirer.prompt(questions)['version']
else:
    answers['version'] = args['version']
#If filetype not specified at runtime inquire
if not args['filetype']:
    print("Select the input filetype you wish to validate")
    questions = [inquirer.List('filetype', choices=['parquet', 'json'])]
    answers['filetype'] = inquirer.prompt(questions)['filetype']
else:
    answers['filetype'] = args['filetype']
if not args['profiles']:
    print("Select the OCSF profiles you wish to validate against")
    if answers['version'] == "1.0.0-rc.2":
        questions = [inquirer.Checkbox('profiles', choices=['cloud', 'datetime', 'host', 'security_control'], default=[""])]
    if answers['version'] == "1.1.0":  
        questions = [inquirer.Checkbox('profiles', choices=['cloud', 'container', 'datetime', 'host', 'load_balancer','network_proxy', 'security_control'], default=[""])]
    answers['profiles'] = inquirer.prompt(questions)['profiles']
else:
    if ',' in args['profiles']:
        answers['profiles'] = list(args['profiles'].split(","))
    if ' ' in args['profiles']:
        answers['profiles'] = list(args['profiles'].split(" "))
    if ',' and ' ' not in args['profiles']:
        answers['profiles'] = []
        answers['profiles'].append(args['profiles'])
    
#If eventclass is not specified at runtime inquire
if not args['eventclass']:
    print("Select the OCSF event class you wish to validate against")
    if answers['version'] == "1.0.0-rc.2":
        questions = [inquirer.List('eventclass', choices=['access_activity', 
                                                          'account_change', 
                                                          'api_activity', 
                                                          'authentication', 
                                                          'authorization', 
                                                          'config_state', 
                                                          'dhcp_activity', 
                                                          'dns_activity', 
                                                          'email_activity', 
                                                          'entity_management', 
                                                          'file_activity', 
                                                          'ftp_activity', 
                                                          'http_activity', 
                                                          'inventory_info', 
                                                          'kernel_activity', 
                                                          'kernel_extension', 
                                                          'memory_activity', 
                                                          'module_activity', 
                                                          'network_activity', 
                                                          'process_activity', 
                                                          'rdp_activity', 
                                                          'registry_key_activity', 
                                                          'registry_value_activity', 
                                                          'resource_activity', 
                                                          'scheduled_job_activity', 
                                                          'security_finding', 
                                                          'smb_activity', 
                                                          'ssh_activity'])]
    if answers['version'] == "1.1.0":
        questions = [inquirer.List('eventclass', choices=['access_activity', 
                                                          'account_change', 
                                                          'api_activity', 
                                                          'authentication', 
                                                          'authorization', 
                                                          'config_state', 
                                                          'dhcp_activity', 
                                                          'dns_activity', 
                                                          'email_activity', 
                                                          'entity_management', 
                                                          'file_activity', 
                                                          'ftp_activity', 
                                                          'http_activity', 
                                                          'inventory_info', 
                                                          'kernel_activity', 
                                                          'kernel_extension', 
                                                          'memory_activity', 
                                                          'module_activity', 
                                                          'network_activity', 
                                                          'process_activity', 
                                                          'rdp_activity', 
                                                          'registry_key_activity', 
                                                          'registry_value_activity', 
                                                          'resource_activity', 
                                                          'scheduled_job_activity', 
                                                          'security_finding', 
                                                          'smb_activity', 
                                                          'ssh_activity'])]
    answers['eventclass'] = inquirer.prompt(questions)['eventclass']
else:
    answers['eventclass'] = args['eventclass']
#Set default verbosity if not specified at runtime
if not args['verbose']:
    args['verbose'] = ''
#Set default profile to null if not specified at runtime
if not args['profiles']:
    args['profiles'] = ''
#Set answers object using arguments
answers['verbose'] = args['verbose']
answers['path'] = args['input']
#answers['profiles'] = args['profiles']
# Check that version argument is set to expected value
if answers['version'] not in ['1.0.0-rc.2', '1.1.0']:
    print('\033[1;91m' + '\n' + answers['version'] + ' is not a valid OCSF version.' + '\033[0m')
    sys.exit()
# Check that verbose argument is set to expected value
if answers['verbose'] not in ['true','']:
    print('\033[1;91m' + '\nWhen used, verbose flag must be set to true.' + '\033[0m')
    sys.exit()   
if answers['filetype'] not in ['parquet', 'json']:
    print('\033[1;91m' + '\n' + answers['filetype'] + 'is not a supported valid filetype.' + '\033[0m')
    sys.exit()
if answers['version'] == "1.0.0-rc.2":
    for i in answers['profiles']:
        if i not in ['', 'cloud', 'datetime', 'host', 'security_control']:
            print('\033[1;91m' + '\n' + i + ' is not a supported profile for ' + answers['version'] + '.\033[0m')
            sys.exit()
if answers['version'] == "1.1.0":
    for i in answers['profiles']:
        if i not in ['', 'cloud', 'container', 'datetime', 'host', 'load_balancer','network_proxy', 'security_control']:
            print('\033[1;91m' + '\n' + i + ' is not a supported profile for ' + answers['version'] + '.\033[0m')
            sys.exit()

answers['profiles'] = ",".join(str(x) for x in answers['profiles'])

if answers['version'] == "1.0.0-rc.2" and answers['eventclass'] not in [ 'access_activity', 
                                  'account_change', 
                                  'api_activity', 
                                  'authentication', 
                                  'authorization', 
                                  'config_state', 
                                  'dhcp_activity', 
                                  'dns_activity', 
                                  'email_activity', 
                                  'entity_management', 
                                  'file_activity', 
                                  'ftp_activity', 
                                  'http_activity', 
                                  'inventory_info', 
                                  'kernel_activity', 
                                  'kernel_extension', 
                                  'memory_activity', 
                                  'module_activity', 
                                  'network_activity', 
                                  'process_activity', 
                                  'rdp_activity', 
                                  'registry_key_activity', 
                                  'registry_value_activity', 
                                  'resource_activity', 
                                  'scheduled_job_activity', 
                                  'security_finding', 
                                  'smb_activity', 
                                  'ssh_activity']:
    print('\033[1;91m' + 'Please provide a valid class_uid for OCSF validation.' + '\033[0m')
    sys.exit()
if answers['version'] == "1.1.0" and answers['eventclass'] not in [ 'access_activity', 
                                  'account_change', 
                                  'api_activity', 
                                  'authentication', 
                                  'authorization', 
                                  'config_state', 
                                  'dhcp_activity', 
                                  'dns_activity', 
                                  'email_activity', 
                                  'entity_management', 
                                  'file_activity', 
                                  'ftp_activity', 
                                  'http_activity', 
                                  'inventory_info', 
                                  'kernel_activity', 
                                  'kernel_extension', 
                                  'memory_activity', 
                                  'module_activity', 
                                  'network_activity', 
                                  'process_activity', 
                                  'rdp_activity', 
                                  'registry_key_activity', 
                                  'registry_value_activity', 
                                  'resource_activity', 
                                  'scheduled_job_activity', 
                                  'security_finding', 
                                  'smb_activity', 
                                  'ssh_activity']:
    print('\033[1;91m' + 'Please provide a valid class_uid for OCSF validation.' + '\033[0m')
    sys.exit()
# Check that input argument is a valid directory
if not os.path.isdir(answers['path']):
    print('\033[1;91m' + '\nThe input specified is not a valid directory.' + '\033[0m')
    sys.exit()
if not bool(sorted(Path(answers['path']).glob('*.parquet'))):
    print('\033[1;91m' + '\nThe input directory contains no parquet files.' + '\033[0m')
    sys.exit()

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
    if len(glob.glob1(Path(answers['path']),"*.parquet")) > 0 :
        if answers['filetype'] == 'parquet':
            pathlist = Path(answers['path']).glob('*.parquet')
        else:
            print(print('\033[1;91m' + 'There is no input file of type *.' + answers["filetype"] + ' in the specified directory.' + '\033[0m'))
            sys.exit()
    if len(glob.glob1(Path(answers['path']),"*.json")) > 0 :
        if answers['filetype'] == 'json':
            pathlist = Path(answers['path']).glob('*.parquet') 
        else:
            print(print('\033[1;91m' + 'There is no input file of type *.' + answers["filetype"] + ' in the specified directory.' + '\033[0m'))        
            sys.exit()
        
    # Iterate through pathlist containing all of the .parquet files
    for file in pathlist:
        print('\033[96m' + "Attempting to Validate File:",os.path.basename(os.path.normpath(file))+"..." + '\033[0m')
        key_vals = []
        EVENT = {}
        if answers['filetype'] == 'parquet':
            (name, ext) = str(file).split('.parquet')
            new_path = '{}.{}'.format(name, 'json')
            # Use pandas dataframes to convert the parquet file at each iter to a JSON object
            df = pd.read_parquet(file)
            df.to_json(new_path)     
        if answers['filetype'] == 'json':
            (name, ext) = str(file).split('.json')
            new_path = '{}.{}'.format(name, 'json')
        
        # Write JSON object data to empty json file
        with open(new_path, 'r') as testData:
            testData = json.load(testData)
            print('\033[96m' + 'Validating Against Event Class: ' + answers['eventclass'] + " " + answers['version'] + '...\n' + '\033[0m')
                
            # Pull OCSF Schema from browser
            url = ('https://schema.ocsf.io/' + answers['version'] + '/schema/classes/' + answers['eventclass'] + '?profiles=' + answers['profiles'])
            response = urllib.request.urlopen(url)
            ocsf_schema = response.read().decode('UTF-8')
            ocsf_schema = json.loads(ocsf_schema)
               
            # Write OCSF Schema to file
            with open(str(path.parent).replace('\\', '/') + "/schemas/" + answers['eventclass'] + "-[" + answers['profiles'] + "]-" + answers['version'] + ".json", 'w') as f:
                json.dump(ocsf_schema, f, ensure_ascii=False)
                
            # Grab OCSF Schema file data
            with open(str(path.parent).replace('\\', '/') + "/schemas/" + answers['eventclass'] + "-[" + answers['profiles'] + "]-" + answers['version'] + ".json", 'r') as ocsf_schema:
                ocsf_schema = json.load(ocsf_schema)
    
            # Instatiate JSON validator
            validator = jsonschema.Draft7Validator(ocsf_schema)
               
            if type(testData['activity_id']) == dict:
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
            if type(testData['activity_id']) == int:
                EVENT = testData
                
            '''
            # The following is a simple algorithm that handles parquet 'Map' types.
            # Pandas representation of parquet Map types is as an array of arrays.
            # This algorithm checks if unmapped is both used and of type list.
            # If unmapped satisfies these conditions these array of arrays is mapped
            # to a standard dictionary type object so that the JSON representation of 
            # of the OCSF parquet is compliant with the intended OCSF schema. 
            '''
                
            if "unmapped" in testData and type(EVENT['unmapped']) is list:
                new_unmapped = {}
                for i,j in EVENT['unmapped']:
                    new_unmapped[i] = j
                EVENT['unmapped'] = new_unmapped
            # Remove None types from JSON object
            EVENT = json.dumps(EVENT)
            EVENT = json.loads(EVENT)
            EVENT = recursive_filter(EVENT, None)
            EVENT = recursive_filter(EVENT, 'None')
            # Run iterative validation against EVENT
            errors = validator.iter_errors(EVENT)
        output = []
        
        try:
            # Clean JSON file if input parquet
            if answers['filetype'] == 'parquet':
                os.remove(new_path)
            # Save errors from iterator
            for error in errors:
                output.append(str(error))
            # Print event data and validation errors
            if output == []:
                if answers['verbose'] == 'true':
                    print('\033[1;32m' + '-----------------------------------FILE DATA-----------------------------------' + '\033[0m')
                    print('\033[1;32m' + json.dumps(EVENT, indent=6) + '\n' + '\033[0m')
                    print('\033[1;32m' + '---------------------------------------------------------------------------\n' + '\033[0m')
                print('\033[1;32m' + 'VALID OCSF.\n' + '\033[0m')
            else:
                if answers['verbose'] == 'true':
                    print('\033[1;91m' + '-----------------------------------FILE DATA-----------------------------------' + '\033[0m')
                    print('\033[1;91m' + json.dumps(EVENT, indent=6) + '\n' + '\033[0m')
                    print('\033[1;91m' + '---------------------------------------------------------------------------\n' + '\033[0m')
                print('\033[1;91m' + 'INVALID OCSF.\n' + '\033[0m')
                for i in output:
                    print('\033[1;91m' + i + '\033[0m')
        except NameError:
            print('\033[1;91m' + 'There is no input file of type' + answers["filetype"] + 'in the specified directory.' + '\033[0m')

if __name__ == '__main__':

    main()

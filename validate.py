#!/usr/bin/python
# -*- coding: utf-8 -*-

import jsonschema
import pandas as pd
import json
import os
import sys
import requests
from pathlib import Path
import pathlib
import glob
from flatten_json import flatten
import pyarrow.parquet as pq
import argparse
import urllib.parse
from json.decoder import JSONDecodeError

# Take in input arguments from CLI
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show help.')
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-i', '--input', help='Path to directory containing parquet or json files.', required=True)
args = vars(parser.parse_args())

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ocsf_class_dictionary = {
	"1.1.0": {
		"1001": {
			"url": "file_activity",
			"class_name": "File System Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1002": {
			"url": "kernel_extension",
			"class_name": "Kernel Extension Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1003": {
			"url": "kernel_activity",
			"class_name": "Kernel Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1004": {
			"url": "memory_activity",
			"class_name": "Memory Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1005": {
			"url": "module_activity",
			"class_name": "Module Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1006": {
			"url": "scheduled_job_activity",
			"class_name": "Scheduled Job Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1007": {
			"url": "process_activity",
			"class_name": "Process Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"2001": {
			"url": "security_finding",
			"class_name": "Security Finding",
			"category_name": "Findings",
			"category_uid": 2
		},
		"2002": {
			"url": "vulnerability_finding",
			"class_name": "Vulnerability Finding",
			"category_name": "Findings",
			"category_uid": 2
		},
		"2003": {
			"url": "compliance_finding",
			"class_name": "Compliance Finding",
			"category_name": "Findings",
			"category_uid": 2
		},
		"2004": {
			"url": "detection_finding",
			"class_name": "Detection Finding",
			"category_name": "Findings",
			"category_uid": 2
		},
		"2005": {
			"url": "incident_finding",
			"class_name": "Incident Finding",
			"category_name": "Findings",
			"category_uid": 2
		},
		"3001": {
			"url": "account_change",
			"class_name": "Account Change",
			"category_name": "Identity & Access Management",
			"category_uid": 3
		},
		"3002": {
			"url": "authentication",
			"class_name": "Authentication",
			"category_name": "Identity & Access Management",
			"category_uid": 3
		},
		"3003": {
			"url": "authorize_session",
			"class_name": "Authorize Session",
			"category_name": "Identity & Access Management",
			"category_uid": 3
		},
		"3004": {
			"url": "entity_management",
			"class_name": "Entity Management",
			"category_name": "Identity & Access Management",
			"category_uid": 3
		},
		"3005": {
			"url": "user_access",
			"class_name": "User Access Management",
			"category_name": "Identity & Access Management",
			"category_uid": 3
		},
		"3006": {
			"url": "group_management",
			"class_name": "Group Management",
			"category_name": "Identity & Access Management",
			"category_uid": 3
		},
		"4001": {
			"url": "network_activity",
			"class_name": "Network Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4002": {
			"url": "http_activity",
			"class_name": "HTTP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4003": {
			"url": "dns_activity",
			"class_name": "DNS Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4004": {
			"url": "dhcp_activity",
			"class_name": "DHCP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4005": {
			"url": "rdp_activity",
			"class_name": "RDP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4006": {
			"url": "smb_activity",
			"class_name": "SMB Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4007": {
			"url": "ssh_activity",
			"class_name": "SSH Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4008": {
			"url": "ftp_activity",
			"class_name": "FTP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4009": {
			"url": "email_activity",
			"class_name": "Email Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4010": {
			"url": "network_file_activity",
			"class_name": "Network File Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4011": {
			"url": "email_file_activity",
			"class_name": "Email File Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4012": {
			"url": "email_url_activity",
			"class_name": "Email URL Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4013": {
			"url": "ntp_activity",
			"class_name": "NTP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"5001": {
			"url": "inventory_info",
			"class_name": "Device Inventory Info",
			"category_name": "Discovery",
			"category_uid": 5
		},
		"5002": {
			"url": "config_state",
			"class_name": "Device Config State",
			"category_name": "Discovery",
			"category_uid": 5
		},
		"5003": {
			"url": "user_inventory",
			"class_name": "User Inventory Info",
			"category_name": "Discovery",
			"category_uid": 5
		},
		"5004": {
			"url": "patch_state",
			"class_name": "Device Config State Change",
			"category_name": "Discovery",
			"category_uid": 5
		},
		"5019": {
			"url": "device_config_state_change",
			"class_name": "",
			"category_name": "Discovery",
			"category_uid": 5
		},
		"6001": {
			"url": "web_resources_activity",
			"class_name": "Web Resources Activity",
			"category_name": "Application Activity",
			"category_uid": 6
		},
		"6002": {
			"url": "application_lifecycle",
			"class_name": "Application Lifecycle",
			"category_name": "Application Activity",
			"category_uid": 6
		},
		"6003": {
			"url": "api_activity",
			"class_name": "API Activity",
			"category_name": "Application Activity",
			"category_uid": 6
		},
		"6004": {
			"url": "web_resource_access_activity",
			"class_name": "Web Resource Access Activity",
			"category_name": "Application Activity",
			"category_uid": 6
		},
		"6005": {
			"url": "datastore_activity",
			"class_name": "Datastore Activity",
			"category_name": "Application Activity",
			"category_uid": 6
		},
		"6006": {
			"url": "file_hosting",
			"class_name": "File Hosting Activity",
			"category_name": "Application Activity",
			"category_uid": 6
		},
		"6007": {
			"url": "scan_activity",
			"class_name": "Scan Activity",
			"category_name": "Application Activity",
			"category_uid": 6
		}
	},
	"1.0.0-rc.2": {
		"1001": {
			"url": "file_activity",
			"class_name": "File System Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1002": {
			"url": "kernel_extension",
			"class_name": "Kernel Extension Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1003": {
			"url": "kernel_activity",
			"class_name": "Kernel Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1004": {
			"url": "memory_activity",
			"class_name": "Memory Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1005": {
			"url": "module_activity",
			"class_name": "Module Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1006": {
			"url": "scheduled_job_activity",
			"class_name": "Scheduled Job Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1007": {
			"url": "process_activity",
			"class_name": "Process Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1008": {
			"url": "registry_key_activity",
			"class_name": "Registry Key Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1009": {
			"url": "registry_value_activity",
			"class_name": "Registry Value Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"1010": {
			"url": "resource_activity",
			"class_name": "Windows Resource Activity",
			"category_name": "System Activity",
			"category_uid": 1
		},
		"2001": {
			"url": "security_finding",
			"class_name": "Security Finding",
			"category_name": "Findings",
			"category_uid": 2
		},
		"3001": {
			"url": "account_change",
			"class_name": "Account Change",
			"category_name": "Audit Activity",
			"category_uid": 3
		},
		"3002": {
			"url": "authentication",
			"class_name": "Authentication",
			"category_name": "Audit Activity",
			"category_uid": 3
		},
		"3003": {
			"url": "authorization",
			"class_name": "Authorization",
			"category_name": "Audit Activity",
			"category_uid": 3
		},
		"3004": {
			"url": "entity_management",
			"class_name": "Entity Management",
			"category_name": "Audit Activity",
			"category_uid": 3
		},
		"3005": {
			"url": "api_activity",
			"class_name": "",
			"category_name": "Audit Activity",
			"category_uid": 3
		},
		"3006": {
			"url": "access_activity",
			"class_name": "API Activity",
			"category_name": "Audit Activity",
			"category_uid": 3
		},
		"4001": {
			"url": "network_activity",
			"class_name": "Network Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4002": {
			"url": "http_activity",
			"class_name": "HTTP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4003": {
			"url": "dns_activity",
			"class_name": "DNS Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4004": {
			"url": "dhcp_activity",
			"class_name": "DHCP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4005": {
			"url": "rdp_activity",
			"class_name": "RDP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4006": {
			"url": "smb_activity",
			"class_name": "SMB Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4007": {
			"url": "ssh_activity",
			"class_name": "SSH Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4008": {
			"url": "ftp_activity",
			"class_name": "FTP Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"4009": {
			"url": "email_activity",
			"class_name": "Email Activity",
			"category_name": "Network Activity",
			"category_uid": 4
		},
		"5001": {
			"url": "inventory_info",
			"class_name": "Device Inventory Info",
			"category_name": "Configuration/Inventory",
			"category_uid": 5
		},
		"5002": {
			"url": "config_state",
			"class_name": "Device Config State",
			"category_name": "Configuration/Inventory",
			"category_uid": 5
		}
	}
}


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

    def produce_event_and_shchema(EVENT, temp_file, targetPath):

        '''
        This function takes in an event and a file path containg files
        the user intends to validate and produces a schema and an
        singular event from a file containining a record
        '''

        EVENT = json.dumps(EVENT)
        EVENT = json.loads(EVENT)
        EVENT = recursive_filter(EVENT, None)
        EVENT = recursive_filter(EVENT, 'None')

        # Check for required fields
        try:
            x = EVENT['class_uid']
        except KeyError:
            print("\nThe class_uid field has not defined within:", os.path.basename(temp_file))
            sys.exit()
        try:
            x = EVENT['metadata']['version']
        except KeyError:
            print("\nThe metadata.version field has not been defined within:", os.path.basename(temp_file))
            sys.exit()
        try:
            x = EVENT['class_name']
        except KeyError:
            print("\nThe class_name field has not defined within:", os.path.basename(temp_file))
            sys.exit()
        try:
            x = EVENT['category_uid']
        except KeyError:
            print("\nThe category_uid field has not defined within:", os.path.basename(temp_file))
            sys.exit()
        try:
            x = EVENT['category_name']
        except KeyError:
            print("\nThe category_name field has not defined within:", os.path.basename(temp_file))
            sys.exit()
	    
        if 'profiles' not in EVENT['metadata'].keys():
            EVENT['metadata']['profiles'] = []
            
        with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
            print('Validating Against OCSF Event Class: ' + str(EVENT['class_uid']), file=f)
            print('Validating Against OCSF Version: ' + str(EVENT['metadata']['version']), file=f)
            print('Validating Against OCSF Profiles: ' + str(EVENT['metadata']['profiles']), file=f)

        # define parameters for OCSF schema call
        url_profiles = ','.join(str(x) for x in EVENT['metadata']['profiles'])
        if str(EVENT['metadata']['version']) not in ["1.1.0", "1.0.0-rc.2"]:
            print("\nERROR: " + EVENT['metadata']['version'] + " is not a supported OCSF schema version. Please ensure the schema version is one of the following: 1.1.0, 1.0.0-rc.2.")
            sys.exit()
        try:
            url_class_name = ocsf_class_dictionary[str(EVENT['metadata']['version'])][str(EVENT['class_uid'])]['url']
        except KeyError:
            print("\nERROR: The \"class_uid:\"", str(EVENT['class_uid']),"is not defined within OCSF", str(EVENT['metadata']['version']))
            sys.exit()
        # Pull OCSF Schema from browser
        url = ('https://schema.ocsf.io/' + str(EVENT['metadata']['version']) + '/schema/classes/' + url_class_name + '?profiles=' + urllib.parse.quote(url_profiles))
        response = requests.get(url)
        ocsf_schema = json.loads(json.dumps(response.json()))
        # Write OCSF Schema to file
        with open(str(targetPath) + "/schemas/" + str(EVENT['class_uid']) + "-" + url_profiles + "-" + str(EVENT['metadata']['version']) + ".json", 'w') as f:
            json.dump(ocsf_schema, f, ensure_ascii=False)
        # Grab OCSF Schema file data
        with open(str(targetPath) + "/schemas/" + str(EVENT['class_uid']) + "-" + url_profiles + "-" + str(EVENT['metadata']['version']) + ".json", 'r') as ocsf_schema:
            ocsf_schema = json.load(ocsf_schema)
            ocsf_schema["additionalProperties"] = False
            return(EVENT, ocsf_schema)

    def generate_schema_errors(errors, EVENT, runtimePath):

        '''
        This function takes in a list of JSON errors, an event and a runtime path
        and returns the printed errors to the output file
        '''
        if 'class_name' in EVENT.keys():
            if EVENT['class_name'] != ocsf_class_dictionary[str(EVENT['metadata']['version'])][str(EVENT['class_uid'])]['class_name']:
                print("\nERROR: The input contains the \"class name\" value:", str(EVENT['class_name']) + ".", "Using the OCSF class uid", str(EVENT['class_uid']), "requires the \"class name\" value:", ocsf_class_dictionary[str(EVENT['metadata']['version'])][str(EVENT['class_uid'])]['class_name'])
                sys.exit()
            
        if EVENT['category_name'] != ocsf_class_dictionary[str(EVENT['metadata']['version'])][str(EVENT['class_uid'])]['category_name']:
            print("\nERROR:The input contains the \"category name\" value:", str(EVENT['category_name']) + ".", "Using the OCSF class uid", str(EVENT['class_uid']), "requires the \"category name\" value:", ocsf_class_dictionary[str(EVENT['metadata']['version'])][str(EVENT['class_uid'])]['category_name'])
            sys.exit()
            
        if EVENT['category_uid'] != ocsf_class_dictionary[str(EVENT['metadata']['version'])][str(EVENT['class_uid'])]['category_uid']:
            print("\nERROR:The input contains the \"category uid\" value:", str(EVENT['category_uid']) + ".", "Using the OCSF class uid", str(EVENT['class_uid']), "requires the \"category uid\" value:", ocsf_class_dictionary[str(EVENT['metadata']['version'])][str(EVENT['class_uid'])]['category_uid'])
            sys.exit()
        
        output = []
        for error in errors:
            output.append(str(error))

        # Print event data and validation errors
        with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
            print('\n------------------------------- INPUT RECORD ------------------------------\n', file=f)
            print(json.dumps(EVENT, indent=6) + '\n', file=f)
        if output == []:
            with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                print('\n---------------------------------- OUTPUT ---------------------------------' + '\n', file=f)
                print('VALID OCSF.', file=f)
                if str(EVENT['class_uid']) == '2001':
                    print("WARN: " + "OCSF event class: Security Findings (2001) is deprecated!", file=f)
                if str(EVENT['class_uid']) == '4010':
                    print("WARN: " + "OCSF event class: Network File Activity (4010) is deprecated!", file=f)
            print('\nVALID OCSF.')
        else:
            with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                print('\n---------------------------------- OUTPUT ---------------------------------' + '\n', file=f)
                print('INVALID OCSF.', file=f)
                if str(EVENT['class_uid']) == '2001':
                    print("WARN: " + "OCSF event class: Security Findings (2001) is deprecated!", file=f)
                if str(EVENT['class_uid']) == '4010':
                    print("WARN: " + "OCSF event class: Network File Activity (4010) is deprecated!", file=f)
                for i in output:
                    print("\n---------------------------------------------------------------------------\n", file=f)
                    print(i, file=f)
                print("\n---------------------------------------------------------------------------", file=f)
            print('\nINVALID OCSF.')

        # Check unmapped field utilization
        try:
            with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                print('\n' + "--------------------------------- METRICS ---------------------------------" + '\n', file=f)
            flat_json = flatten(EVENT)
            if len(EVENT['unmapped']) > 0:
                with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                    print("WARN:", "The OCSF log has:", str(round(100*(len(EVENT['unmapped'])/len(flat_json)), 2)) + '%', "of its keys in unmapped.", file=f)
        except KeyError:
            with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                print("INFO: Unmapped is not used in this mapping.\n", file=f)

    def measure_dropped_records(testSource, EVENT):

        '''
        This function takes in a testSource file and an event
        and flattens and compares them to indentify potentially
        dropped valus within the ETL
        '''

        flat_source = flatten(testSource)
        flat_dest = flatten(EVENT)
        idx = 0
        source_values = []
        source_keys = []
        dest_values = []
        dest_keys = []
        dropped_keys = []
        dropped_values = []
        dropped_dict = {}
        for k, v in flat_source.items():
            source_values.append(v)
        for k, v in flat_source.items():
            source_keys.append(k)
        for k, v in flat_dest.items():
            dest_values.append(v)
        for k, v in flat_dest.items():
            dest_keys.append(k)
        for i in source_values:
            if i not in dest_values and i is not None:
                dropped_keys.append(source_keys[idx])
                dropped_values.append(i)
                dropped_dict[source_keys[idx]] = i
            idx = idx + 1
        with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
            if len(dropped_keys) > 0:
                print("WARN:", "The following number of source values:", len(dropped_keys), "- did not have a corresponding key containing the value in the transformed data...\n", file=f)
                print(json.dumps(dropped_dict, indent=4, sort_keys=True) + '\n', file=f)
            else:
                print("INFO: There were no dropped attributes in the transformed data.\n", file=f)

    def control_function(testData):
        with open(temp_file, 'r') as testData:
                        try:
                            testData = json.load(testData)
                        except JSONDecodeError:  
                            print("\nERROR: THE FILE " + str(temp_file) + " IS NOT A PROPERLY FORMATTED JSON OR PARQUET.")
                            sys.exit()
                        # Code for scenario where testData is single record
                        if type(testData) == dict:
                            EVENT = testData
                            if "unmapped" in EVENT and type(testData['unmapped']) is list:
                                new_unmapped = {}
                                for i, j in EVENT['unmapped']:
                                    new_unmapped[i] = j
                                EVENT['unmapped'] = new_unmapped
                            # Produce event record and generate OCSF schema
                            EVENT, ocsf_schema = produce_event_and_shchema(EVENT, temp_file, targetPath)
                            # Instatiate and run JSON validator and generate schema errors
                            validator = jsonschema.Draft7Validator(ocsf_schema)
                            errors = validator.iter_errors(EVENT)
                            generate_schema_errors(errors, EVENT, runtimePath)
                            # Check dropped sources
                            source_path = Path(str(targetPath) + '/inputs/' + str(s_file_name))
                            if os.path.isfile(source_path):
                                with open(source_path, 'r', encoding='utf-8') as testSource:
                                    try:
                                        testSource = json.load(testSource)
                                        if type(testSource) == list:
                                            for i in testSource:
                                                measure_dropped_records(i, EVENT)
                                        if type(testSource) == dict:
                                            measure_dropped_records(testSource, EVENT)
                                    except JSONDecodeError:  
                                        with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                                          print("WARN: " + "THE FILE WITH NAME", str(s_file_name), "IN", str(Path(str(targetPath) + '/inputs/')), "- IS NOT A JSON FILE. SKIPPING METRICS FOR DROPPED RECORDS.\n", file=f)
                            else:
                                with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                                    print("WARN: " + "THERE IS NO FILE WITH NAME", str(s_file_name), "IN", str(Path(str(targetPath) + '/inputs/')), "- SKIPPING METRICS FOR DROPPED RECORDS.\n", file=f)
                        # Code for scenario where testData is list of records
                        if type(testData) == list:
                            for x in range(0, len(testData)):
                                EVENT = testData[x]
                                # Format unmapped for JSON validation
                                if "unmapped" in EVENT and type(EVENT['unmapped']) is list:
                                    new_unmapped = {}
                                    for i, j in EVENT['unmapped']:
                                        new_unmapped[i] = j
                                    EVENT['unmapped'] = new_unmapped
                                # Produce clean event and ocsf schema
                                EVENT, ocsf_schema = produce_event_and_shchema(EVENT, temp_file, targetPath)
                                # Instatiate and run JSON validator and generate schema errors
                                validator = jsonschema.Draft7Validator(ocsf_schema)
                                errors = validator.iter_errors(EVENT)
                                generate_schema_errors(errors, EVENT, runtimePath)
                                # Check dropped sources
                                source_path = Path(str(targetPath) + '/inputs/' + str(s_file_name))
                                if os.path.isfile(source_path):
                                    with open(source_path, 'r') as testSource:
                                        try:
                                          testSource = json.load(testSource)
                                        except JSONDecodeError:  
                                          with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                                            print("WARN: " + "THE FILE WITH NAME", str(s_file_name), "IN", str(Path(str(targetPath) + '/inputs/')), "- IS NOT A JSON FILE. SKIPPING METRICS FOR DROPPED RECORDS.\n", file=f)
                                        else:
                                          if type(testSource) == list:
                                              try:
                                                  measure_dropped_records(testSource[x], EVENT)
                                              except IndexError:
                                                  with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                                                      print("WARN: " + str(s_file_name) + " IN " + str(Path(str(targetPath) + '/inputs/')) + " HAS EXCEEDED THE LENGTH OF THE TEST DATA AND WAS SKIPPED.", file=f)
                                          if type(testSource) == dict:
                                              measure_dropped_records(testSource, EVENT)
                                else:
                                    with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                                        print("WARN: " + "THERE IS NO FILE WITH NAME", str(s_file_name), "IN", str(Path(str(targetPath) + '/inputs/')), "- SKIPPING METRICS FOR DROPPED RECORDS.\n", file=f)

    # Store the absolute path of this script in path variable
    runtimePath = Path(os.path.abspath(__file__))
    targetPath = Path(args['input'])
    targetFiles = os.listdir(targetPath)
    switch = 0

    # Creating required directories
    if not os.path.exists(str(targetPath) + "/temp/"):
        os.makedirs(str(targetPath) + "/temp/")
    if not os.path.exists(str(targetPath) + "/inputs/"):
        os.makedirs(str(targetPath) + "/inputs/")
    if not os.path.exists(str(targetPath) + "/schemas/"):
        os.makedirs(str(targetPath) + "/schemas/")

    # Create output.txt
    with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'w') as f:
        print('\n', file=f)
    
    for i in targetFiles:
        ext = pathlib.Path(i).suffix
        s_file_name = i.replace(".json", ".source").replace(".parquet", ".source").replace(".ndjson", ".source")

        # Run this process for parquet files
        if ext == ".parquet":
            print('\n' + "ATTEMPTING TO VALIDATE FILE:", i)
            with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                print('\n' + "--------" + " ATTEMPTING TO VALIDATE FILE: ", i + "--------" + '\n', file=f)
            EVENT = {}
            switch = switch + 1
            (file, ext) = str(i).split('.parquet')
            temp_file = '{}.{}'.format(file, 'json')
            temp_file = Path(temp_file.replace(os.path.basename(temp_file), "/temp/" + os.path.basename(temp_file)))
            temp_file = Path(str(targetPath) + str(temp_file))
            read_file = Path(str(targetPath) + '/' + str(i))
            
            table = pq.read_table(read_file)
            pythonified = table.to_pylist()
            pq_array = []
            with open(temp_file, 'w') as tempData:
                for record in pythonified:
                    pq_array.append(record)
                print(json.dumps(pq_array, indent=4, sort_keys=True, default=str), file=tempData)
            control_function(temp_file)
                                
        # Run this process for json files
        elif ext == ".json" or ext == ".ndjson":
            print('\n' + "ATTEMPTING TO VALIDATE FILE:", i)
            with open(Path(str(runtimePath.parent.absolute()) + '/output.txt'), 'a') as f:
                print('\n' + "--------" + " ATTEMPTING TO VALIDATE FILE: ", i + " --------" + '\n', file=f)
            EVENT = {}
            switch = switch + 1
            temp_file = Path(str(targetPath) + '/' + str(i))
            control_function(temp_file)
            
    if switch == 0:
        print("\nERROR: There are no .parquet or .json/.ndjson files in the target directory.")
        sys.exit()
    print('\nSending verbose output to: ' + str(Path(str(runtimePath.parent.absolute()) + '/output.txt\n')))


if __name__ == '__main__':

    main()

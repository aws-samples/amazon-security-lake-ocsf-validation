#!/usr/bin/python
from pathlib import Path
import re
import jsonschema
import pandas as pd
import json
import os
import sys
import requests
import argparse

args = {"input": ""}

path = Path(os.path.abspath(__file__))

args["input"] = Path(path.parent)

#Check that input argument is a valid directory
if not os.path.isdir(args['input']):
    print('\nThe input specified is not a valid directory.')
    exit()
    
if not bool(sorted(Path(args['input']).glob('*.parquet'))):
    print('\nThe input directory contains no parquet files.')
    exit()


def main():
    def recursive_filter(item, *forbidden):
        if isinstance(item, list):
            return [
                recursive_filter(entry, *forbidden)
                for entry in item
                if entry not in forbidden
            ]
        if isinstance(item, dict):
            result = {}
            for key, value in item.items():
                value = recursive_filter(value, *forbidden)
                if key not in forbidden and value not in forbidden:
                    result[key] = value
            return result
        return item

    pathlist = Path(args["input"]).glob("*.parquet")

    for file in pathlist:

        key_vals = []
        EVENT = {}
        SCHEMA_CLASS = ""

        name, ext = str(file).split(".parquet")
        new_path = "{}.{}".format(name, "json")

        df = pd.read_parquet(file)
        df.to_json(new_path)

        with open(new_path, "r") as testData:
            testData = json.load(testData)

            # LOAD SCHEMA DEFINITION FILE BASED ON CLASS NAME

            if str(testData["class_uid"]["0"]) == "1001":
                SCHEMA_CLASS = "file_activity"

            if str(testData["class_uid"]["0"]) == "1002":
                SCHEMA_CLASS = "kernal_extension"

            if str(testData["class_uid"]["0"]) == "1003":
                SCHEMA_CLASS = "kernel_activity"

            if str(testData["class_uid"]["0"]) == "1004":
                SCHEMA_CLASS = "memory_activity"

            if str(testData["class_uid"]["0"]) == "1005":
                SCHEMA_CLASS = "module_activity"

            if str(testData["class_uid"]["0"]) == "1006":
                SCHEMA_CLASS = "scheduled_job_activity"

            if str(testData["class_uid"]["0"]) == "1007":
                SCHEMA_CLASS = "process_activity"

            if str(testData["class_uid"]["0"]) == "1008":
                SCHEMA_CLASS = "registry_key_activity"

            if str(testData["class_uid"]["0"]) == "1009":
                SCHEMA_CLASS = "registry_value_activity"

            if str(testData["class_uid"]["0"]) == "1010":
                SCHEMA_CLASS = "resource_activity"

            if str(testData["class_uid"]["0"]) == "2001":
                SCHEMA_CLASS = "security_finding"

            if str(testData["class_uid"]["0"]) == "3001":
                SCHEMA_CLASS = "account_change"

            if str(testData["class_uid"]["0"]) == "3002":
                SCHEMA_CLASS = "authentication"

            if str(testData["class_uid"]["0"]) == "3003":
                SCHEMA_CLASS = "authorization"

            if str(testData["class_uid"]["0"]) == "3004":
                SCHEMA_CLASS = "entity_management"

            if str(testData["class_uid"]["0"]) == "3005":
                SCHEMA_CLASS = "api_activity"

            if str(testData["class_uid"]["0"]) == "4001":
                SCHEMA_CLASS = "network_activity"

            if str(testData["class_uid"]["0"]) == "4002":
                SCHEMA_CLASS = "http_activity"

            if str(testData["class_uid"]["0"]) == "4003":
                SCHEMA_CLASS = "dns_activity"

            if str(testData["class_uid"]["0"]) == "4004":
                SCHEMA_CLASS = "dhcp_activity"

            if str(testData["class_uid"]["0"]) == "4005":
                SCHEMA_CLASS = "rdp_activity"

            if str(testData["class_uid"]["0"]) == "4006":
                SCHEMA_CLASS = "smb_activity"

            if str(testData["class_uid"]["0"]) == "4007":
                SCHEMA_CLASS = "ssh_activity"

            if str(testData["class_uid"]["0"]) == "4008":
                SCHEMA_CLASS = "ftp_activity"

            if str(testData["class_uid"]["0"]) == "5001":
                SCHEMA_CLASS = "inventory_info"

            if str(testData["class_uid"]["0"]) == "5002":
                SCHEMA_CLASS = "config_state"

            if SCHEMA_CLASS == "":
                print("No schema found for:", testData["class_uid"]["0"])
                exit()

            print(
                "\nValidating Against Event Class: "
                + SCHEMA_CLASS
                + " ("
                + str(testData["class_uid"]["0"])
                + ")...\n"
            )

            with open(
                str(path.parent.parent).replace("\\", "/")
                + "/ocsf_schema_1.0.0-rc.2/"
                + SCHEMA_CLASS
                + ".json",
                "r",
            ) as ocsf_schema:
                ocsf_schema = json.load(ocsf_schema)

            validator = jsonschema.Draft7Validator(ocsf_schema)

            for keys in testData.keys():
                key_vals.append(keys)

            for i in key_vals:
                K = i
                V = testData[i]["0"]
                if K == "data":
                    V = str(V).replace('"', "'")
                if K == "raw_data":
                    V = str(V).replace('"', "'")
                EVENT[K] = V

            EVENT = json.dumps(EVENT)
            EVENT = json.loads(EVENT)
            EVENT = recursive_filter(EVENT, None)
            EVENT = recursive_filter(EVENT, "None")
            errors = validator.iter_errors(EVENT)

        output = []

        try:
            os.remove(new_path)
            for error in errors:

                if (
                    re.search(r"Failed validating \'type\' in schema.+\n.+", str(error))
                    != None
                ):
                    output.append(str(error))
                if re.search(r"\'.+\' is a required property", str(error)) != None:
                    output.append(
                        re.search(r"\'.+\' is a required property", str(error)).group(0)
                    )

            if output == []:
                print(
                    "----------------------------------------FILE DATA----------------------------------------"
                )
                print(json.dumps(EVENT, indent=6) + "\n")
                print(
                    "-------------------------------------------------------------------------------------\n"
                )
                print("VALID OCSF.")
            else:
                print(
                    "----------------------------------------FILE DATA----------------------------------------"
                )
                print(json.dumps(EVENT, indent=6) + "\n")
                print(
                    "-------------------------------------------------------------------------------------\n"
                )
                for i in output:
                    print(i)

        except NameError:
            print("Please place a parquet file in the input directory.")


if __name__ == "__main__":
    main()


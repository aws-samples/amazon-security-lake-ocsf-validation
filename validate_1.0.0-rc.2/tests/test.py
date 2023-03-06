#!/usr/bin/python
from core import slTestSuite
import os

os.system("")  # enables ansi escape characters in terminal


if __name__ == "__main__":

    """Test Case 1 - Checking For Most Recent jsonschema Package"""
    if slTestSuite.check_ver("jsonschema") == True:
        # print(COLOR["GREEN"], "Testing Green!!", COLOR["ENDC"])
        print("\033[92m", "\nStatus: PASS.\n", "\033[0m")
    else:
        print("\033[91m", "\nStatus: FAIL.\n", "\033[0m")
        print("jsonschema python package is out of date, please upgrade and try again.")

    """Test Case 1 - Checking For Most Recent pandas Package"""
    if slTestSuite.check_ver("pandas") == True:
        print("\033[92m", "\nStatus: PASS.\n", "\033[0m")
    else:
        print("\033[91m", "\nStatus: FAIL.\n", "\033[0m")
        print("pandas python package is out of date, please upgrade and try again.")

    """Test Case 2 - Checking For Most Recent requests Package"""
    if slTestSuite.check_ver("requests") == True:
        print("\033[92m", "\nStatus: PASS.\n", "\033[0m")
    else:
        print("\033[91m", "\nStatus: FAIL.\n", "\033[0m")
        print("requests python package is out of date, please upgrade and try again.")


#!/usr/bin/python
import unittest
import requests
from argparse import ArgumentParser, RawTextHelpFormatter
from importlib.metadata import version


class slTestSuite(unittest.TestCase):

    """Basic test cases."""

    def check_ver(name):
        current_version = version(name)
        package = name
        response = requests.get(f"https://pypi.org/pypi/{package}/json")
        latest_version = response.json()["info"]["version"]

        if current_version == latest_version:
            print("\nChecking Package: " + package)
            print("Current Version " + current_version)
            print("Latest Version: " + latest_version)
            return True
        else:
            print("\nChecking Package: " + package)
            print("Current Version " + current_version)
            print("Latest Version: " + latest_version)
            return False


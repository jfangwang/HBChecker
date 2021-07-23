#!/usr/bin/python3
from checker import run_checker
from helper_functions import *
import os, sys
import getpass
def run():
    run_checker()

# Find what OS this script is running on
os_sys = platform.system()
if os_sys == 'Windows':
    run()
elif os_sys == 'Linux':
    run()
else:
    print("HBChecker cannot run on " + os_sys + " just yet.")
    exit(1)

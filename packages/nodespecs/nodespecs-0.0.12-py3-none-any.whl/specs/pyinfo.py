import sys
import platform

print (sys.executable)
platform.python_branch()
platform.python_compiler()
platform.python_implementation()
platform.architecture()

import subprocess
from pprint import pprint

def find_python_interpreters():
    try:
        # Running the 'where' command to find all occurrences of python.exe
        result = subprocess.check_output("where python", shell=True)
        interpreters = result.decode().strip().split('\n')
        return interpreters
    except subprocess.CalledProcessError:
        return []

# List the found Python interpreters
pprint(find_python_interpreters())
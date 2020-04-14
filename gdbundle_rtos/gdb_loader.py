import gdb
import os

PACKAGE_DIR = os.path.dirname(__file__)

SCRIPT_PATHS = [
    [PACKAGE_DIR, 'scripts', 'zephyr_gdb.py']
    [PACKAGE_DIR, 'scripts', 'threadx_gdb.py']
]

def _abs_path(path):
    return os.path.abspath(os.path.join(*path))

def gdbundle_load():
    for script_path in SCRIPT_PATHS:
        gdb.execute("source {}".format(_abs_path(script_path)))

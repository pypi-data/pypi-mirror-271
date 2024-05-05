import json
from pathlib import Path

from os import environ

class Conf :
    pkg = 'pip_pkg'
    py_ver = 'py_ver'  # python version to use
    module = "module"  # module name to run
    rm_venv = 'rm_venv'  # whether to remove venv after running

class Const :
    rc = Path(environ['HOME']) / 'auto_run_configs'

c = Const()

def read_json(fp) :
    # if fp is not entered with .json extension, add .json to it
    fp = fp.with_suffix('.json')

    fp = c.rc / fp

    with open(fp , 'r') as f :
        return json.load(f)

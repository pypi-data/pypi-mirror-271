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

def read_json(conf_stem) :
    fp = c.rc / conf_stem
    fp = fp.with_suffix('.json')
    with open(fp , 'r') as _f :
        return fp , json.load(_f)

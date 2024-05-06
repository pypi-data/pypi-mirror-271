"""

    1. Installs the required python version, skips if already installed
    2. Creates a virtual environment with that python version

    """

import subprocess
import sys
from pathlib import Path

from .util import Conf
from .util import read_json

c = Conf()

def make_venv(fp) :
    j = read_json(fp)

    py_ver = j[c.py_ver]

    venv_name = Path(fp).stem

    _cmds = ['pyenv' , 'install' , '--skip-existing' , py_ver]
    subprocess.run(_cmds)

    _cmds = ['pyenv' , 'virtualenv' , py_ver , venv_name , '&> /dev/null']
    subprocess.run(_cmds)

    print(venv_name)

if __name__ == '__main__' :
    conf_fn = sys.argv[1]
    make_venv(conf_fn)

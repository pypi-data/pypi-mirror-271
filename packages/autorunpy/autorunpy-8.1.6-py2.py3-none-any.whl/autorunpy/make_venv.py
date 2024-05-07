"""

    1. Installs the required python version, skips if already installed
    2. Creates a virtual environment with that python version

    """

import subprocess
import sys

from .util import Conf
from .util import read_json

c = Conf()

def make_venv(conf_stem) :
    fp , j = read_json(conf_stem)

    py_ver = j[c.py_ver]

    _cmds = ['pyenv' , 'install' , '--skip-existing' , py_ver]
    _cmds += ['&> /dev/null']
    subprocess.run(_cmds)

    _cmds = ['pyenv' , 'virtualenv' , py_ver , conf_stem]
    _cmds += ['&> /dev/null']
    subprocess.run(_cmds)

    print(conf_stem)

if __name__ == '__main__' :
    arg = sys.argv[1]
    make_venv(arg)

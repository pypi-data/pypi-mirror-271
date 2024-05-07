"""

    Removes virtualenv using pyenv if specified in the config file

    """

import subprocess
import sys

from .util import Conf
from .util import read_json

c = Conf()

def rm_venv(conf_stem) :
    _ , j = read_json(conf_stem)

    if j[c.rm_venv] :
        _cmds = ['pyenv' , 'virtualenv-delete' , '-f' , conf_stem]
        _cmds += ['&> /dev/null']

        subprocess.run(_cmds)

if __name__ == '__main__' :
    arg = sys.argv[1]
    rm_venv(arg)

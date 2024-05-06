"""

    Removes virtualenv using pyenv if specified in the config file

    """

import subprocess
import sys
from pathlib import Path

from .util import Conf
from .util import read_json

c = Conf()

def rm_venv(conf_stem) :
    fp , j = read_json(conf_stem)

    if j[c.rm_venv] :
        cmds = ['pyenv' , 'virtualenv-delete' , '-f' , conf_stem]
        cmds += ['&> /dev/null']

        subprocess.run(cmds)

if __name__ == '__main__' :
    conf_stem = sys.argv[1]
    rm_venv(conf_stem)

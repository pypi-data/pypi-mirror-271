"""

    Removes virtualenv using pyenv if specified in the config file

    """

import subprocess
import sys
from pathlib import Path

from .util import Conf
from .util import read_json

c = Conf()

def rm_venv(fp) :
    j = read_json(fp)
    
    if j[c.rm_venv] :
        cmds = ['pyenv' , 'virtualenv-delete' , '-f' , Path(fp).stem]
        cmds += ['&> /dev/null']

        subprocess.run(cmds)

if __name__ == '__main__' :
    conf_fn = sys.argv[1]
    rm_venv(conf_fn)

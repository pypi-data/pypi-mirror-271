import subprocess
import sys

from .util import Conf
from .util import read_json

c = Conf()

def make_venv(fp) :
    """ make virtualenv with pyenv, delete existing venv if it exists """
    j = read_json(fp)

    py_ver = j[c.py_ver]
    pkg = j[c.pkg]

    venv_name = pkg + '_' + py_ver

    subprocess.run(['pyenv' , 'install' , '--skip-existing' , py_ver])

    cmds = ['pyenv' , 'virtualenv' , py_ver , venv_name ,'&> /dev/null']
    subprocess.run(cmds)

    print(venv_name)

if __name__ == '__main__' :
    conf_fn = sys.argv[1]
    make_venv(conf_fn)

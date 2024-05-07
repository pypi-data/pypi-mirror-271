"""

    return relative command to run module

    """

import sys

from .util import Conf
from .util import read_json

c = Conf()

def ret_module_2_run_rel_command(conf_stem) :
    _ , j = read_json(conf_stem)
    print(j[c.pkg] + '.' + j[c.module])

if __name__ == '__main__' :
    arg = sys.argv[1]
    ret_module_2_run_rel_command(arg)

import sys

from .util import Conf
from .util import read_json

c = Conf()

def ret_module_2_run_rel_command(fp) :
    """ return relative command to run module"""
    j = read_json(fp)
    print(j[c.pkg] + '.' + j[c.module])

if __name__ == '__main__' :
    conf_fn = sys.argv[1]
    ret_module_2_run_rel_command(conf_fn)

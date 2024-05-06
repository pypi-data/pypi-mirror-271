import sys

from .util import Conf
from .util import read_json

c = Conf()

if __name__ == '__main__' :
    conf_stem = sys.argv[1]
    _ , js = read_json(conf_stem)
    print(js[c.pkg])

import sys

from .util import Conf
from .util import read_json

c = Conf()

if __name__ == '__main__' :
    conf_fn = sys.argv[1]
    js = read_json(conf_fn)
    print(js[c.pkg])

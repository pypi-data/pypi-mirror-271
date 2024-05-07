import sys

from .util import Conf
from .util import read_json

c = Conf()

if __name__ == '__main__' :
    arg = sys.argv[1]
    _ , js = read_json(arg)
    print(js[c.pkg])

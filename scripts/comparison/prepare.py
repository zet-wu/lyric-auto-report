from common import *
import sys
sys.path.insert(0, str(ROOT / 'scripts/timing'))
from prepare import prepare_dataset

if __name__ == '__main__':
    prepare_dataset(OUT, CACHE, include_protocol=False)

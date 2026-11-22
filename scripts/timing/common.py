from pathlib import Path
import gzip, hashlib, json, os, re, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import ROOT, portable, dump, read, exists, sha, plain_line

OUT = ROOT / 'results/timing'
CACHE = ROOT / '.cache/timing'
DEPS = ROOT / '.deps/comparison' if (ROOT / '.deps/comparison/studio').exists() else ROOT / '.deps'
UPSTREAM = DEPS / 'timing'
STUDIO = DEPS / 'studio'
for p in (OUT, CACHE):
    p.mkdir(parents=True, exist_ok=True)

def product_imports():
    sys.path[:0] = [str(STUDIO), str(DEPS / 'lazulite/src')]

def timing_imports():
    sys.path.insert(0, str(UPSTREAM))

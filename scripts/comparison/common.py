from pathlib import Path
import gzip, hashlib, json, os, re, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import ROOT, portable, dump, read, exists, sha, plain_line

OUT = ROOT / 'results/comparison'
CACHE = ROOT / '.cache/comparison'
UPSTREAM = ROOT / '.deps/comparison/timing'
STUDIO = ROOT / '.deps/comparison/studio'
for p in (OUT, CACHE):
    p.mkdir(parents=True, exist_ok=True)

def product_imports():
    sys.path[:0] = [str(STUDIO), str(ROOT / '.deps/comparison/lazulite/src')]

def timing_imports():
    sys.path.insert(0, str(UPSTREAM))

def songs():
    return [s for s in read(OUT / 'reference.json') if s['id'] not in ('s11', 's13', 's14')]

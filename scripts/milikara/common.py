from pathlib import Path
import gzip, hashlib, json, os, re, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import ROOT, portable, dump, read, exists, sha, plain_line

OUT = ROOT / 'results/milikara'
CACHE = ROOT / '.cache/milikara'
DEPS = ROOT / '.deps/comparison' if (ROOT / '.deps/comparison/studio').exists() else ROOT / '.deps'
UPSTREAM = DEPS / 'milikara'
STUDIO = DEPS / 'studio'
for p in (OUT, CACHE):
    p.mkdir(parents=True, exist_ok=True)

def product_imports():
    sys.path[:0] = [str(STUDIO), str(DEPS / 'lazulite/src')]

def timing_imports():
    sys.path.insert(0, str(UPSTREAM))

sys.path.insert(0, str(UPSTREAM))
MODES = ['concat_core']
FACTORS = ['delimiter', 'line_gap', 'rest_gap', 'rest_token', 'free_tail']
SOURCES = [(OUT, CACHE)]

def inputs(kind='confirmed-targets'):
    for song in read(OUT / (kind + '.json')):
        selected = os.environ.get('BENCHMARK_SONGS', '').split(',')
        if selected != [''] and song['id'] not in selected:
            continue
        yield song, OUT, CACHE

def prediction_paths():
    return sorted({p.with_suffix('') if p.suffix == '.gz' else p for p in (OUT / 'predictions').glob('*.json*')})

"""Frozen factorial research; no imports modify product or upstream sources."""
from common import ROOT, UPSTREAM, STUDIO, dump, read, exists as present, product_imports, timing_imports
from pathlib import Path

PREVIOUS = ROOT / 'results/timing'
OLD_CACHE = ROOT / '.cache/timing'
OUT = ROOT / 'results/ablation'
CACHE = ROOT / '.cache/ablation'
for folder in (OUT, CACHE):
    folder.mkdir(parents=True, exist_ok=True)
PRIMARY = [f's{i:02}' for i in range(1, 13) if i != 11] + ['s15']

def songs():
    return [s for s in read(PREVIOUS / 'reference.json') if s['id'] != 's14']

def stem_path(song, separator):
    if separator == 'demucs':
        return OLD_CACHE / 'audio' / (Path(song['audio']).stem + '.wav')
    return CACHE / 'stems' / separator / (song['id'] + '.wav')

def result_path(separator, backend, strategy, sid):
    return OUT / 'predictions' / separator / backend / strategy / (sid + '.json')

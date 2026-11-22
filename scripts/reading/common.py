from pathlib import Path
import json, os, re, sys, unicodedata
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import ROOT, read, dump

OUT = ROOT / 'results/reading'
deps = ROOT / '.deps/comparison' if (ROOT / '.deps/comparison/studio').exists() else ROOT / '.deps'
sys.path[:0] = [str(deps / name) for name in ('studio', 'milikara', 'timing')]

def hira(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(chr(ord(c) - 96) if 'ァ' <= c <= 'ヶ' else c for c in s)

def clean(s):
    return ''.join(c for c in hira(s) if c.isalnum() or c == 'ー')

def kana(s):
    return bool(clean(s)) and bool(re.fullmatch('[ぁ-ゖー]+', clean(s)))

def segments(text, pairs):
    result = []; pos = 0
    for surface, reading in pairs:
        start = text.find(surface, pos)
        if start < 0:
            raise ValueError('source surface mismatch ' + repr(surface))
        if start > pos:
            result.append({'a': pos, 'b': start, 'text': text[pos:start], 'reading': text[pos:start]})
        result.append({'a': start, 'b': start + len(surface), 'text': surface, 'reading': hira(reading or '')})
        pos = start + len(surface)
    if pos < len(text):
        result.append({'a': pos, 'b': len(text), 'text': text[pos:], 'reading': text[pos:]})
    assert ''.join(p['text'] for p in result) == text
    return result

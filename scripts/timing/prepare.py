"""Extract reference lyric structure and prepare untimed inputs for evaluation."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from timing.common import *
import xml.etree.ElementTree as ET
import hashlib, subprocess, re

T = '{http://www.w3.org/ns/ttml}'; S = '{http://www.w3.org/ns/ttml#styling}'
M = '{http://www.w3.org/ns/ttml#metadata}'; X = '{http://www.w3.org/XML/1998/namespace}'
D = '{urn:lazulite:studio:draft}'

def seconds(s):
    if s is None:
        return None
    if s.endswith('ms'):
        return float(s[:-2]) / 1000
    if s.endswith('s'):
        return float(s[:-1])
    return sum(float(v) * 60 ** i for i, v in enumerate(reversed(s.split(':'))))

def body_text(e):
    if e.get(S + 'ruby') in ('text', 'textContainer') or e.get(M + 'role', '').startswith('x-'):
        return ''
    return (e.text or '') + ''.join(body_text(c) + (c.tail or '') for c in e)

def prepare_dataset(out_dir, cache_dir, include_protocol=False):
    dataset_ids = read(ROOT / 'configs/dataset-ids.json')
    records = []
    for path in sorted((ROOT / 'datasets/annotations').glob('*.ttml')):
        sid = dataset_ids[path.name]
        name = path.stem; audio = ROOT / 'datasets/audio' / f'{name.removesuffix("-假名注音")}.m4a'
        tree = ET.parse(path); root = tree.getroot()
        for j, node in enumerate(root.iter()):
            node.set(D + 'id', f'{sid}-n{j}')
        rows = []; backgrounds = []
        for index, p in enumerate(root.findall('.//' + T + 'body//' + T + 'p')):
            words = []; leaves = []; cursor = 0
            for w in p:
                if w.tag != T + 'span' or w.get(M + 'role', '').startswith('x-'):
                    if w.get(M + 'role') == 'x-bg':
                        backgrounds.append(w.get(D + 'id'))
                    continue
                text = body_text(w) + (w.tail or ''); a, b = cursor, cursor + len(text); cursor = b
                record = {'id': w.get(D + 'id'), 'text': text, 'a': a, 'b': b, 'start': seconds(w.get('begin')), 'end': seconds(w.get('end'))}
                words.append(record)
                ruby = [x for x in w.iter(T + 'span') if x.get(S + 'ruby') == 'text']
                for leaf in ruby or [w]:
                    reading = ''.join(leaf.itertext()) if ruby else body_text(w)
                    leaves.append({
                        'id': leaf.get(D + 'id'),
                        'word_id': record['id'],
                        'text': reading,
                        'start': seconds(leaf.get('begin')),
                        'end': seconds(leaf.get('end')),
                        'kind': 'ruby' if ruby else 'word',
                    })
            text = ''.join(w['text'] for w in words)
            valid = [x for x in leaves if x['start'] is not None and x['end'] is not None and x['end'] > x['start'] and any(c.isalnum() for c in x['text'])]
            language = ('ja' if index < 10 else 'yue') if sid == 'jy01' else ('teochew' if sid.startswith('t') else 'cmn' if sid.startswith('m') else 'yue' if sid.startswith('y') else 'ja')
            rows.append({
                'id': p.get(D + 'id'),
                'index': index + 1,
                'text': text,
                'words': words,
                'leaves': leaves,
                'start': seconds(p.get('begin')),
                'end': seconds(p.get('end')),
                'vocal_start': min((x['start'] for x in valid), default=None),
                'vocal_end': max((x['end'] for x in valid), default=None),
                'language': language,
            })
        bg_intervals = [(seconds(x.get('begin')), seconds(x.get('end'))) for b in root.findall('.//' + T + 'body//' + T + 'span') if b.get(M + 'role') == 'x-bg' for x in b.iter() if x.get('begin') and x.get('end')]
        for p in root.findall('.//' + T + 'body//' + T + 'p'):
            for w in list(p):
                if w.tail:
                    separator = ET.Element(T + 'span', {D + 'id': w.get(D + 'id') + '-tail'})
                    separator.text = w.tail; w.tail = None
                    p.insert(list(p).index(w) + 1, separator)
        snapshot = {
            'lyrics': {'draftTtml': ET.tostring(root, encoding='unicode')},
            'lineOrder': [x['id'] for x in rows],
            'editing': {'skippedAlignmentLineIds': backgrounds},
        }
        for node in root.iter():
            for attr in ('begin', 'end', 'dur'):
                node.attrib.pop(attr, None)
        snapshot['lyrics']['draftTtml'] = ET.tostring(root, encoding='unicode')
        dump(cache_dir / 'inputs' / f'{sid}-studio.json', snapshot)
        dump(cache_dir / 'inputs' / f'{sid}-untimed.json', [{'text': r['text']} for r in rows])
        dump(cache_dir / 'inputs' / f'{sid}-trusted.json', [{'text': r['text'], 'start': r['start'], 'end': r['end']} for r in rows])
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(audio)]))
        records.append({
            'id': sid,
            'name': name,
            'audio': str(audio.relative_to(ROOT)),
            'ttml': str(path.relative_to(ROOT)),
            'audio_sha256': sha(audio),
            'ttml_sha256': sha(path),
            'duration': float(probe['format']['duration']),
            'background_lines': len(backgrounds),
            'lines': rows,
            'background_intervals': bg_intervals,
        })
    dump(out_dir / 'reference.json', records)
    if include_protocol:
        dump(out_dir / 'protocol.json', {
            'timing_commit': subprocess.check_output(['git', '-C', str(UPSTREAM), 'rev-parse', 'HEAD'], text=True).strip(),
            'studio_commit': subprocess.check_output(['git', '-C', str(STUDIO), 'rev-parse', 'HEAD'], text=True).strip(),
            'input': '26 audio files / 26 TTML references; primary chain only; background intervals retained',
            'audio': 'same Demucs htdemucs seed=0 complete stem supplied to both systems; all stems generated in this evaluation',
            'conditions': ['current Studio projection + default NextFire, no hints or gap fill', 'Timing tifa with untimed surface text, source mode on shared stem', 'Timing tifa with trusted human line windows, surface text'],
            'dialects': 'Cantonese and Teochew out of declared model scope, kept separate; kana transcription is not Japanese speech',
            'metrics': 'positive duration, both endpoints <=100/200 ms; missing boundaries stay in denominator; no timestamp interpolation; paired common surface groups secondary',
            'no_external_llm': True, 'product_changes': False, 'reference_changes': False,
        })
    print([(s['id'], s['name'], len(s['lines']), s['background_lines']) for s in records])

if __name__ == '__main__':
    prepare_dataset(OUT, CACHE, include_protocol=True)

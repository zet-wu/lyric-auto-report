"""Prepare Japanese text inputs; reading references remain separate."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import ROOT, read, dump

def display(text):
    return text.replace('\n', '').replace('\r', '').replace('\t', '')

def prepare():
    selected = set(read(ROOT / 'configs/reading.json')['songs'])
    references = []
    for song in read(ROOT / 'results/timing/reference.json'):
        if song['id'] not in selected:
            continue
        data = {'song': song['id'], 'lines': []}
        gold = {'song': song['id'], 'lines': []}
        for line in song['lines']:
            words = [display(word['text']) for word in line['words']]
            text = ''.join(words)
            truth = []
            for word in line['words']:
                leaves = [leaf for leaf in line['leaves'] if leaf['word_id'] == word['id']]
                truth.append({'text': display(word['text']),
                              'reading': display(''.join(leaf['text'] for leaf in leaves)),
                              'ruby': any(leaf['kind'] == 'ruby' for leaf in leaves)})
            data['lines'].append({'id': line['id'], 'text': text, 'words': words})
            gold['lines'].append({'id': line['id'], 'words': truth})
        dump(ROOT / 'results/reading/inputs' / f"{song['id']}.json", data)
        references.append(gold)
    dump(ROOT / 'results/reading/references.json.gz', references)

if __name__ == '__main__':
    prepare()

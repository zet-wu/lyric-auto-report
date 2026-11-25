"""Merge anonymous, text-only Terra corrections into native candidate parts."""
import argparse
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import ROOT, read, dump


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('answers', nargs='+', type=Path)
    args = parser.parse_args()
    seen = set()
    for path in args.answers:
        for answer in read(path)['songs']:
            number = int(answer['id'].removeprefix('X'))
            sid = f'j{number:02}'
            if sid not in read(ROOT / 'configs/reading.json')['songs'] or sid in seen:
                raise ValueError('Unexpected or duplicate anonymous song')
            seen.add(sid)
            result = copy.deepcopy(read(ROOT / 'results/reading/predictions/studio' / f'{sid}.json'))
            if result.get('status')!='ok':
                raise ValueError('Native Studio candidate generation failed; no valid correction input')
            applied = set()
            for correction in answer['corrections']:
                line, part = correction['line'] - 1, correction['part']
                if type(line) is not int or type(part) is not int or line < 0 or part < 0 or (line, part) in applied:
                    raise ValueError('Duplicate or invalid correction location')
                value = correction['reading']
                if not isinstance(value, str):
                    raise TypeError('Reading must be a string')
                result['lines'][line]['parts'][part]['reading'] = value
                applied.add((line, part))
            result.update(method='studio-llm-corrected', model='gpt-6.1-terra', status='ok', correction_count=len(applied))
            dump(ROOT / 'results/reading/predictions/llm-corrected' / f'{sid}.json.gz', result)
            print(sid, len(applied))
    if seen != set(read(ROOT / 'configs/reading.json')['songs']):
        raise ValueError('LLM correction import does not cover all 20 songs')


if __name__ == '__main__':
    main()

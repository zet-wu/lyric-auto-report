"""Run native CPU reading engines on text-only inputs; failures remain explicit."""
from common import *
from shared import portable
import argparse
import time


def reader(method):
    if method == 'studio':
        from server.reading import SudachiReadingProposer
        proposer = SudachiReadingProposer()
        if not proposer.available:
            raise RuntimeError(proposer.unavailable_reason)
        def pairs(line):
            text = line['text']; result = []; pos = 0
            for proposal in sorted(proposer.propose([{'id': line['id'], 'text': text}]), key=lambda item: item.base_start):
                if proposal.base_start < pos or text[proposal.base_start:proposal.base_end] != proposal.base:
                    raise ValueError('Overlapping or mismatched native reading proposal')
                if proposal.base_start > pos:
                    result.append((text[pos:proposal.base_start], text[pos:proposal.base_start]))
                result.append((proposal.base, proposal.reading)); pos = proposal.base_end
            if pos < len(text):
                result.append((text[pos:], text[pos:]))
            return result
        return pairs
    if method == 'sudachi':
        from sudachipy import dictionary, tokenizer
        engine = dictionary.Dictionary().create()
        return lambda line: [(token.surface(), token.reading_form()) for token in engine.tokenize(line['text'], tokenizer.Tokenizer.SplitMode.C)]
    if method == 'milikara':
        from kara_align.reading import japanese
        from timing.japanese_dictionary import make_tagger
        japanese._tagger_state['t'] = make_tagger()
        def pairs(line):
            return [(part.surface, part.reading if part.reading is not None else ''.join(unit.reading for unit in part.units) if part.units else '' if part.uncertain else part.surface)
                    for part in japanese.rule_segments(line['text'])]
        return pairs
    if method == 'timing':
        from timing.text import tokenize
        from timing.singing import pronunciation_overrides
        overrides = pronunciation_overrides()['ja']
        return lambda line: [(word.text, overrides.get(word.spoken) or word.source_pronunciation or word.reading or word.spoken) for word in tokenize(line['text'], fine=False)]
    if method == 'openjtalk':
        os.environ['OPEN_JTALK_DICT_DIR'] = str(ROOT / '.models/openjtalk/open_jtalk_dic_utf_8-1.11')
        if not Path(os.environ['OPEN_JTALK_DICT_DIR']).is_dir():
            raise FileNotFoundError('OpenJTalk dictionary is not installed; run scripts/download.py reading')
        import pyopenjtalk
        return lambda line: [(node['string'], node['pron'] if node['pron'] not in ('', '*', '、', '？') else node['string']) for node in pyopenjtalk.run_frontend(line['text'])]
    raise ValueError(f'Unknown method: {method}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--methods', nargs='+', choices=['studio', 'sudachi', 'milikara', 'timing', 'openjtalk'], default=['studio', 'milikara', 'timing', 'openjtalk'])
    args = parser.parse_args()
    for method in args.methods:
        runtime = []; initialization = None
        try:
            engine = reader(method)
        except Exception as exc:
            initialization = {'type': type(exc).__name__, 'message': portable(exc)[:500]}
        for sid in read(ROOT / 'configs/reading.json')['songs']:
            song = read(OUT / 'inputs' / f'{sid}.json')
            rows = []; started = time.perf_counter()
            for line in song['lines']:
                error = initialization
                if error is None:
                    try:
                        pairs = engine(line)
                        if method == 'openjtalk' and ''.join(surface for surface, _ in pairs) != line['text']:
                            # Native OpenJTalk source normalization changes boundaries; score the complete source span.
                            parts = [{'a': 0, 'b': len(line['text']), 'text': line['text'], 'reading': hira(''.join(value for _, value in pairs))}]
                        else:
                            parts = segments(line['text'], pairs)
                    except Exception as exc:
                        error = {'type': type(exc).__name__, 'message': portable(exc)[:500]}
                if error:
                    parts = [{'a': 0, 'b': len(line['text']), 'text': line['text'], 'reading': ''}]
                rows.append({'id': line['id'], 'status': 'failed' if error else 'ok', 'parts': parts, **({'error': error} if error else {})})
            status = 'failed' if any(row.get('error') for row in rows) else 'ok'
            dump(OUT / 'predictions' / method / f'{sid}.json.gz', {'song': sid, 'method': method, 'status': status, 'lines': rows})
            runtime.append({'song': sid, 'method': method, 'status': status, 'seconds': time.perf_counter() - started})
            print(method, sid, status, flush=True)
        dump(OUT / 'runtime' / f'{method}.json', runtime)


if __name__ == '__main__':
    main()

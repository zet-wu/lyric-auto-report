"""Run SUG's native Sudachi resolver or the required Windows WinRT resolver."""
from common import *
from shared import portable
import argparse
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-winrt', action='store_true')
    parser.add_argument('--output-dir', type=Path, default=OUT)
    args = parser.parse_args()
    method = 'sug-winrt' if args.require_winrt else 'sug'
    source = ROOT / '.deps/comparison/sug'
    sys.path.insert(0, str(source / 'src'))
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != read(ROOT / 'configs/comparison-sources.json')['sug']['commit']:
        raise RuntimeError('SUG source commit mismatch')
    from strange_uta_game.backend.domain import Project, Sentence, Singer
    from strange_uta_game.backend.application.ai_timing import PronunciationResolver
    from strange_uta_game.backend.infrastructure.parsers.ruby_analyzer import create_analyzer, WinRTAnalyzer, SudachiAnalyzer
    runtime = []
    for sid in read(ROOT / 'configs/reading.json')['songs']:
        song = read(OUT / 'inputs' / f'{sid}.json')
        started = time.perf_counter()
        result = {'song': sid, 'method': method, 'status': 'failed'}
        try:
            project = Project()
            project.singers = [Singer(id='s1', name='main')]
            project.sentences = [Sentence.from_text(line['text'], singer_id='s1') for line in song['lines']]
            analyzer = create_analyzer() if args.require_winrt else SudachiAnalyzer()
            if args.require_winrt and not isinstance(analyzer, WinRTAnalyzer):
                raise RuntimeError('WinRT unavailable; fallback is forbidden')
            if args.require_winrt and analyzer._pykakasi_conv is None:
                raise RuntimeError('WinRT native character-reading reference dependency is missing')
            plan = PronunciationResolver(analyzer=analyzer, chinese_mode=False).resolve_project(project, fill_missing=True)
            lookup = {}
            for unit in plan.units:
                if not unit.is_sentence_end:
                    lookup.setdefault((unit.line_idx, unit.char_idx), []).append(unit)
            lines = []
            for li, (line, sentence) in enumerate(zip(song['lines'], project.sentences, strict=True)):
                pairs = []
                for ci, char in enumerate(sentence.characters):
                    units = lookup.get((li, ci), [])
                    value = ''.join(unit.reading or ('' if unit.expects_token else unit.char_text) for unit in units) if units else char.char
                    pairs.append((char.char, value))
                lines.append({'id': line['id'], 'parts': segments(line['text'], pairs)})
            result.update(status='ok', lines=lines, pending_units=len(plan.pending_units))
        except Exception as exc:
            error = {'type': type(exc).__name__, 'message': portable(exc)[:500]}
            result.update(error=error, failed_stage='frontend_g2p', lines=[
                {'id': line['id'], 'error': error, 'parts': [{'a': 0, 'b': len(line['text']), 'text': line['text'], 'reading': ''}]}
                for line in song['lines']])
        extension = '.json' if args.require_winrt else '.json.gz'
        dump(args.output_dir / 'predictions' / method / (sid + extension), result)
        runtime.append({'song': sid, 'method': method, 'status': result['status'], 'seconds': time.perf_counter() - started})
        print(method, sid, result['status'], flush=True)
    dump(args.output_dir / 'runtime' / f'{method}.json', runtime)


if __name__ == '__main__':
    main()

"""M8 fixed prediction-only triggers and cross-backend local replacement."""
import argparse
import copy
import math
import re
import sys
import time
from dataclasses import asdict
from shared import ROOT, read, dump, exists, portable


def interval(timing):
    a, b = timing.get('start'), timing.get('end')
    return (a['time'], b['time']) if a and b and b['time'] > a['time'] else None


def trigger_sets(baseline, probabilities, vocab):
    import numpy as np
    by_line = {}
    for unit in baseline['units']:
        by_line.setdefault(unit['line_id'], []).append(unit)
    sets = {name: set() for name in ('short_unit_30ms', 'short_unit_40ms', 'same_vowel_imbalance', 'legacy_conf')}
    features = {}; legacy = []
    for index, (lid, units) in enumerate(by_line.items()):
        spans = [interval(unit['proposed_timing']) for unit in units]
        valid = [span for span in spans if span]
        durations = [b-a if span else 0. for span in spans for a, b in [span or (0., 0.)]]
        for threshold in (30, 40):
            if any(duration < threshold / 1000 for duration in durations):
                sets[f'short_unit_{threshold}ms'].add(lid)
        same = False
        for left, right, dl, dr in zip(units, units[1:], durations, durations[1:]):
            a, b = left['model_text'], right['model_text']
            av, bv = re.findall('[aeiou]', a), re.findall('[aeiou]', b)
            matching = bool(a and a == b) or bool(a and b and a[-1] in 'aeiou' and b[0] == a[-1])
            if matching and (min(dl, dr) < .04 or (min(dl, dr) < .08 and max(dl, dr) >= 4 * max(min(dl, dr), 1e-6))):
                same = True
        if same:
            sets['same_vowel_imbalance'].add(lid)
        confidence = []
        for unit in units:
            scores = []
            for char in unit['character_path']:
                start, end = char['frames']; symbol = char['character']
                if symbol in vocab and end > start:
                    scores.append(float(np.exp(probabilities[start:end, vocab[symbol]]).mean()))
            if scores:
                confidence.append(float(np.mean(scores)))
        duration = sum(b-a for a, b in valid)
        inside = sum(max(0, min(b, segment['core_end']) - max(a, segment['core_start'])) for a, b in valid for segment in baseline['core_segments'])
        coverage = min(1., inside / max(duration, 1e-8)); conf = float(np.mean(confidence)) if confidence else 0.
        cross = any(unit['crosses_removed_gap'] for unit in units)
        longest = max(durations, default=0.)
        invalid = len(valid) != len(units)
        excessive = any(d > (3 if j == len(units)-1 else 2) for j, d in enumerate(durations))
        window = [max(0., math.floor((min(a for a, b in valid)-.3)/.02)*.02), min(baseline['duration'], math.ceil((max(b for a, b in valid)+.3)/.02)*.02)] if valid else None
        features[lid] = {'window': window, 'confidence': conf, 'coverage': coverage, 'longest': longest, 'cross_gap': cross, 'invalid': invalid}
        if valid and (cross or invalid or excessive or coverage < .70 or conf < .60):
            rank = (not (cross or invalid), not excessive, -longest if excessive else 0, coverage, conf, index)
            legacy.append((rank, lid))
    used = 0.; cap = .2 * baseline['duration']; limit = math.ceil(.2 * len(by_line))
    for _, lid in sorted(legacy):
        window = features[lid]['window']; cost = window[1]-window[0]
        if len(sets['legacy_conf']) < limit and 0 < cost <= 35 and used + cost <= cap:
            sets['legacy_conf'].add(lid); used += cost
    for threshold in (30, 40):
        sets[f'combined_{threshold}ms'] = sets[f'short_unit_{threshold}ms'] | sets['same_vowel_imbalance']
    return by_line, sets, features


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--songs', nargs='+', required=True); args = parser.parse_args()
    sys.path[:0] = [str(ROOT / '.deps/comparison/studio'), str(ROOT / '.deps/comparison/lazulite/src')]
    import numpy as np
    import soundfile as sf
    from lazulite.audio.io import resample_audio
    from lazulite.audio.preparation import prepare_existing_vocals
    from lazulite.models.audio import AudioBuffer,VocalSegment
    from lazulite.models.japanese import JapaneseAlignmentRequest
    from lazulite.audio.concat import ConcatMap, Piece
    from lazulite.alignment.japanese.backend import open_backend
    from lazulite.alignment.japanese.stages import AcousticResult
    from lazulite.alignment.japanese.run import align_japanese, JapaneseConfig
    from server.alignment_postprocessing import object_timings
    refs = {song['id']: song for song in read(ROOT / 'results/timing/reference.json')}
    backends = {}
    try:
        for sid in args.songs:
            baseline = read(ROOT / 'results/M1/predictions/G1-studio-demucs-nextfire' / f'{sid}.json')
            swap = read(ROOT / 'results/M1/predictions/G1-studio-demucs-mms_fa-smart' / f'{sid}.json')
            if baseline['status'] != 'ok':
                for trigger in read(ROOT/'configs/phase2.json')['modules']['M8']['triggers']:
                    for strategy in read(ROOT/'configs/phase2.json')['modules']['M8']['strategies']:
                        dump(ROOT/'results/M8/predictions'/f'{trigger}-{strategy}'/f'{sid}.json.gz',{'song':sid,'status':'failed','failed_stage':'baseline_dependency','error':baseline.get('error'),'native_cases':baseline.get('cases',[]),'trigger':trigger,'strategy':strategy})
                continue
            prefix = ROOT / '.cache/phase2/emissions' / f'{sid}-demucs-nextfire-float-core-all'
            probabilities = np.load(prefix.with_suffix('.npy'))
            vocab = read(ROOT / '.models/nextfire/vocab.json')
            by_line, triggers, features = trigger_sets(baseline, probabilities, vocab)
            # Reference errors are accessed only for the explicitly labeled oracle control.
            truth = {leaf['id']: leaf for line in refs[sid]['lines'] for leaf in line['leaves']}
            error_ranks = []
            for lid, units in by_line.items():
                errors = []
                for item in baseline['projection']['mapping']:
                    if item['line_id'] != lid or item['object_id'] not in truth:
                        continue
                    ref = truth[item['object_id']]; pred = interval(baseline['object_timings'].get(item['object_id'], {}))
                    errors.append(max(abs(pred[0]-ref['start']), abs(pred[1]-ref['end'])) if pred and ref['start'] is not None and ref['end'] is not None else float('inf'))
                error_ranks.append((max(errors, default=0), lid))
            k = len(triggers['combined_30ms'])
            triggers['oracle_top_k'] = {lid for _, lid in sorted(error_ranks, reverse=True)[:k]}
            wave, rate = sf.read(ROOT / '.cache/comparison/stems/demucs' / f'{sid}.wav', dtype='float32', always_2d=True)
            vocals = AudioBuffer(wave.T.copy(), rate, sid)
            segments=tuple(VocalSegment(**segment) for segment in baseline['core_segments'])
            request = JapaneseAlignmentRequest.from_dict(baseline['projection']['request'])
            requests = {line.line_id: JapaneseAlignmentRequest((line,)) for line in request.lines}
            local = {}
            for lid in set.union(*triggers.values()):
                window = features[lid]['window']
                for model in ('nextfire', 'mms-fa'):
                    started = time.monotonic()
                    try:
                        if window is None or not 0 < window[1]-window[0] <= 35:
                            raise ValueError('Predicted line has no eligible local window (maximum 35 seconds)')
                        if model not in backends:
                            backends[model] = open_backend(ROOT / '.models' / model, 'cuda')
                        backend = backends[model]
                        # Re-project native phonetic input for each model vocabulary.
                        from server.alignment_projection import project_alignment
                        from phase2_native import snapshot_for
                        projection = project_alignment(snapshot_for(sid, 'manual'), False, model={'vocabulary': backend.vocab, 'blank': backend.blank})
                        req = JapaneseAlignmentRequest.from_dict(projection['request'])
                        req = JapaneseAlignmentRequest(tuple(line for line in req.lines if line.line_id == lid))
                        mono = resample_audio(vocals, sample_rate=backend.frames.sample_rate, channels=1)
                        a = int(window[0]*mono.sample_rate); b = min(mono.samples.shape[1], int(math.ceil(window[1]*mono.sample_rate)))
                        clip = AudioBuffer(mono.samples[:, a:b].copy(), mono.sample_rate, sid)
                        mapping = ConcatMap(mono.sample_rate, b-a, (Piece(a,b,0,b-a),))
                        acoustic = AcousticResult(backend.emissions(clip), backend.vocab, backend.blank, backend.frames, mapping, vocals.duration, special_tokens=backend.special_tokens)
                        result = align_japanese(None, req, acoustic=acoustic, config=JapaneseConfig(hint_mode='off'))
                        selected = [item for item in projection['mapping'] if item['line_id'] == lid]
                        timings = object_timings(result, selected, vocals, model == 'mms-fa', segments=segments)
                        local[lid, model] = {'status': 'failed' if result.status=='unresolved' else 'ok', 'native_status':result.status,'native_issues':[asdict(issue) for unit in result.units for issue in unit.issues], 'object_timings': timings, 'seconds': time.monotonic()-started}
                    except Exception as exc:
                        local[lid, model] = {'status':'failed','error':{'type':type(exc).__name__,'message':portable(exc)[:800]}, 'seconds':time.monotonic()-started}
            for trigger, selected in triggers.items():
                for strategy in ('nextfire_baseline','nextfire_local','mms_fa_local','mms_fa_global_swap'):
                    result = {'song':sid,'separator':'demucs','trigger':trigger,'strategy':strategy,'status':'ok',
                              'object_timings':copy.deepcopy(baseline['object_timings']), 'projection':baseline['projection'],
                              'triggered_lines':sorted(selected),'line_count':len(by_line),'features':features,'local_results':{}}
                    if strategy != 'nextfire_baseline':
                        for lid in selected:
                            candidate = swap if strategy == 'mms_fa_global_swap' else local[lid, 'nextfire' if strategy == 'nextfire_local' else 'mms-fa']
                            if candidate['status'] != 'ok':
                                result['status']='failed'; result['local_results'][lid]={'status':'failed','error':candidate.get('error'),'native_status':candidate.get('native_status'),'native_issues':candidate.get('native_issues',[]), 'retained_baseline':True}; continue
                            object_ids = {item['object_id'] for item in baseline['projection']['mapping'] if item['line_id']==lid}
                            result['object_timings'].update({key:value for key,value in candidate['object_timings'].items() if key in object_ids})
                            result['local_results'][lid]={'status':'ok','seconds':candidate.get('seconds',0) if strategy!='mms_fa_global_swap' else 0}
                    dump(ROOT/'results/M8/predictions'/f'{trigger}-{strategy}'/f'{sid}.json.gz',result)
            print('M8',sid,'complete',flush=True)
    finally:
        for backend in backends.values():backend.close()


if __name__ == '__main__':
    main()

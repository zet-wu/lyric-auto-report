"""M7: eight soft-cost combinations and delimiter/free-tail single controls."""
from common import *
from modules import *
from fast_ctc import install
import itertools, time
install()
for song, evidence, cache in inputs():
    sid = song['id']; doc = document(song)
    for mode in MODES:
        y, mapping, env, activity = load_audio(song, evidence, cache, mode)
        cases = []
        for bits in itertools.product([False, True], repeat=3):
            flags = dict(delimiter=False, free_tail=False, **dict(zip(('line_gap', 'rest_gap', 'rest_token'), bits)))
            cases.append(('soft-' + ''.join(str(int(bit)) for bit in bits), flags))
        for factor in ('delimiter', 'free_tail'):
            flags = dict.fromkeys(FACTORS, False); flags[factor] = True
            cases.append((factor, flags))
        for name, flags in cases:
            dest = OUT / 'predictions' / f'{sid}--{mode}--{name}.json.gz'
            if exists(dest):
                continue
            started = time.perf_counter()
            em = emission(cache, sid, mode, flags['delimiter'])
            units, outcome = global_decode(doc, em, activity, flags)
            dump(dest, {'song': sid, 'experiment': f'{mode}/{name}', 'kind': 'confirmed-targets',
                        'status': 'ok' if outcome.feasible else 'failed', 'flags': flags,
                        'predictions': predictions(doc, units, mapping), 'seconds': time.perf_counter() - started,
                        'feasible': outcome.feasible})
        print(sid, mode, '8 soft-cost combinations + 2 single controls complete', flush=True)

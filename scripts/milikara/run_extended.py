"""M7 extension: MiliKara soft-cost factorial on BS Karaoke and MMS_FA (raw + smart)."""
from bisect import bisect_left
import itertools
import sys
import time
import numpy as np
import soundfile as sf
from common import *
from modules import PROFILE, decode_config, document, predictions
from kara_align.align.activity import detect_activity
from kara_align.align.backends.wav2vec2_ctc import tokenize_chars
from kara_align.align.decoding import decode_task, prepare, unit_timings_for_line
from kara_align.align.planning import Task
from kara_align.audio.analysis import rms_envelope_db
from kara_align.interfaces import Emission
from kara_align.timebase import FrameMap
from shared import portable

sys.path[:0] = [str(ROOT / '.deps/comparison/studio'), str(ROOT / '.deps/comparison/lazulite/src')]
from lazulite.alignment.japanese.backend import MMS_VOCAB
from lazulite.audio.io import resample_audio
from lazulite.models.audio import AudioBuffer
from server.alignment_postprocessing import non_silent_ends

NEXTFIRE_VOCAB = read(ROOT / '.models/nextfire/vocab.json')


def apply_smart_extension(rows, silence_ends, core_ends, duration):
    flat = [unit for row in rows for unit in row]
    out = [[dict(unit) if unit is not None else None for unit in row] for row in rows]
    flat_out = [unit for row in out for unit in row]
    for idx, unit in enumerate(flat_out):
        if unit is None or unit.get('crosses_removed_gap'):
            continue
        start, end = unit['start'], unit['end']
        if not 0 <= start < end <= duration:
            continue
        limit = min(duration, next((u['start'] for u in flat[idx + 1:] if u is not None and u.get('start') is not None), duration))
        if limit <= end:
            continue
        extended = limit
        for candidates in (silence_ends, core_ends):
            pos = bisect_left(candidates, end)
            if pos < len(candidates):
                extended = min(extended, candidates[pos])
        unit['end'] = float(extended)
    return out


def decode_for_backend(doc, lp, vocab, blank_id, specials, activity, flags):
    tok = lambda ids, texts: tokenize_chars(ids, texts, vocab, specials)
    prep = prepare(doc, PROFILE, tok)
    order = prep.order
    em = Emission(lp, FrameMap(16000, 320, 0, 0), blank_id)
    task = Task('global', 'main', order, order, 0, em.num_frames, free_tail=flags['free_tail'])
    outcome = decode_task(task, em, prep, decode_config(flags), 'vocals', activity=activity)
    return [u for lid in order for u in unit_timings_for_line(prep, outcome, lid)], outcome


def main():
    songs = read(OUT / 'confirmed-targets.json')
    groups = [
        ('bs_nextfire', 'bs', 'nextfire', False),
        ('demucs_mms_fa', 'demucs', 'mms-fa', True),
        ('bs_mms_fa', 'bs', 'mms-fa', True),
    ]
    for group_name, sep, backend, is_mms in groups:
        vocab = MMS_VOCAB if is_mms else NEXTFIRE_VOCAB
        blank_id = 0 if is_mms else 29
        specials = {'-'} if is_mms else {'[UNK]', '[PAD]', '[BOS]', '[EOS]'}
        cases = []
        for bits in itertools.product([False, True], repeat=3):
            flags = dict(delimiter=False, free_tail=False, **dict(zip(('line_gap', 'rest_gap', 'rest_token'), bits)))
            cases.append(('soft-' + ''.join(str(int(bit)) for bit in bits), flags))
        if not is_mms:
            flags = dict.fromkeys(FACTORS, False); flags['delimiter'] = True
            cases.append(('delimiter', flags))
        flags = dict.fromkeys(FACTORS, False); flags['free_tail'] = True
        cases.append(('free_tail', flags))

        for song in songs:
            sid = song['id']
            doc = document(song)
            prefix = ROOT / '.cache/phase2/emissions' / f'{sid}-{sep}-{backend}-float-core-all'
            meta = read(prefix.with_suffix('.json'))
            raw_lp = np.load(prefix.with_suffix('.npy'))
            pieces = meta['mapping']['pieces']
            rate = meta['mapping']['sample_rate']
            mapping = pieces
            samples, wav_rate = sf.read(ROOT / '.cache/comparison/stems' / sep / f'{sid}.wav', dtype='float32', always_2d=True)
            vocals = AudioBuffer(samples.T.copy(), wav_rate, sid)
            mono16 = resample_audio(vocals, sample_rate=16000, channels=1).samples[0]
            concat_y = np.concatenate([mono16[p['source_start']:p['source_end']] for p in pieces]) if pieces else np.zeros(0, dtype=np.float32)
            env = rms_envelope_db(concat_y, 16000)
            activity = detect_activity(env, 10.0)
            silence_ends = non_silent_ends(vocals) if is_mms else None
            core_ends = sorted({p['source_end'] / rate for p in pieces}) if is_mms else None

            for name, flg in cases:
                raw_group = f'{group_name}_raw' if is_mms else group_name
                dest_raw = OUT / 'predictions' / f'{sid}--{raw_group}--{name}.json.gz'
                dest_smart = OUT / 'predictions' / f'{sid}--{group_name}_smart--{name}.json.gz' if is_mms else None
                if exists(dest_raw) and (dest_smart is None or exists(dest_smart)):
                    continue
                started = time.perf_counter()
                lp = raw_lp.copy()
                if flg['delimiter'] and not is_mms:
                    lp[:, 29] = np.logaddexp(lp[:, 29], lp[:, 0])
                    lp[:, 0] = -1e4
                record = {'song': sid, 'experiment': f'{raw_group}/{name}', 'kind': 'confirmed-targets', 'status': 'failed', 'flags': flg}
                try:
                    units, outcome = decode_for_backend(doc, lp, vocab, blank_id, specials, activity, flg)
                    preds = predictions(doc, units, mapping)
                    record.update(status='ok' if outcome.feasible else 'failed', predictions=preds, feasible=outcome.feasible)
                except Exception as exc:
                    preds = None
                    record['error'] = {'type': type(exc).__name__, 'message': portable(exc)[:800]}
                record['seconds'] = time.perf_counter() - started
                dump(dest_raw, record)
                if is_mms:
                    smart_rec = dict(record, experiment=f'{group_name}_smart/{name}')
                    if preds is not None and record['status'] == 'ok':
                        smart_rec['predictions'] = apply_smart_extension(preds, silence_ends, core_ends, vocals.duration)
                    dump(dest_smart, smart_rec)
            print(f'M7-ext {group_name} {sid} complete', flush=True)


if __name__ == '__main__':
    main()

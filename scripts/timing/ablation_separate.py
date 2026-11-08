"""Run unmodified upstream separators on every unique source recording."""
from ablation_common import *
timing_imports()
import argparse, hashlib, shutil, time, traceback
import soundfile as sf
import torch
from timing.bs_lead import separate
from timing.separation import separate_vocals

parser = argparse.ArgumentParser()
parser.add_argument('separator', choices=['bs', 'kim'])
args = parser.parse_args()
torch.set_num_threads(8)
assert torch.cuda.is_available()
for song in songs():
    sid = song['id']
    target = stem_path(song, args.separator)
    record = OUT / 'separation' / args.separator / (sid + '.json')
    if target.exists() and record.exists():
        continue
    start = time.monotonic()
    work = CACHE / 'separation' / args.separator / sid
    work.mkdir(parents=True, exist_ok=True)
    try:
        torch.manual_seed(0)
        torch.cuda.reset_peak_memory_stats()
        source, info = (separate if args.separator == 'bs' else separate_vocals)(ROOT / song['audio'], work, log=lambda s: print(s, flush=True))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        meta = sf.info(target)
        dump(record, {'song': sid, 'model': args.separator, 'source': song['audio'],
                      'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                      'frames': meta.frames, 'rate': meta.samplerate, 'channels': meta.channels,
                      'seconds': time.monotonic()-start, 'peak_gib': torch.cuda.max_memory_allocated()/2**30,
                      'upstream': info})
        print('DONE', args.separator, sid, round(time.monotonic()-start, 2), flush=True)
    except Exception:
        dump(record.with_name(sid+'-error.json'), {'error': traceback.format_exc()})
        print(traceback.format_exc(), flush=True)

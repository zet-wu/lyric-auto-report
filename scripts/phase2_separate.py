"""Generate current native stems once for all Phase 2 consumers."""
import argparse
import sys
import time
from shared import ROOT, read, dump, exists, portable


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model')
    parser.add_argument('--songs', nargs='+', required=True)
    args = parser.parse_args()
    sys.path[:0] = [str(ROOT / 'scripts/timing'),str(ROOT / '.deps/comparison/lazulite/src')]
    from native_separators import load
    import numpy as np
    import soundfile as sf
    import torch
    from lazulite.audio.io import decode_audio
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA is required for stem generation')
    torch.set_num_threads(8)
    refs = {song['id']: song for song in read(ROOT / 'results/timing/reference.json')}
    model, infer, identity = load(args.model, 'cuda')
    for sid in args.songs:
        output = ROOT / '.cache/comparison/stems' / args.model / f'{sid}.wav'
        target = ROOT / 'results/M5/separation' / args.model / f'{sid}.json.gz'
        if output.exists() and exists(target) and read(target)['status'] == 'ok':
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        record = {'song': sid, 'model': args.model, 'status': 'failed'}
        try:
            torch.manual_seed(0); np.random.seed(0)
            source = ROOT / refs[sid]['audio']
            wave = decode_audio(source, sample_rate=44100, channels=2).samples
            if hasattr(infer, 'native_file'):
                work = ROOT / '.cache/phase2/separation' / args.model / sid
                work.mkdir(parents=True, exist_ok=True)
                vocals = infer.native_file(source, work)
            else:
                vocals = infer(wave)
            torch.cuda.synchronize()
            if not np.isfinite(vocals).all() or vocals.ndim != 2:
                raise ValueError('Native separation returned nonfinite or invalid audio')
            sf.write(output, vocals.T, 44100, subtype='FLOAT')
            record.update(status='ok', frames=vocals.shape[1], sample_rate=44100,
                          source=refs[sid]['audio'], stem=output.relative_to(ROOT).as_posix())
        except Exception as exc:
            record.update(error={'type': type(exc).__name__, 'message': portable(exc)[:800]}, failed_stage='separation')
        record['seconds'] = time.monotonic() - started
        dump(target, record)
        print(args.model, sid, record['status'], flush=True)


if __name__ == '__main__':
    main()

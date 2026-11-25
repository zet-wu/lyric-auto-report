"""Generate only the two requested original-mixture M7 decoding controls."""
from common import *
product_imports()
import numpy as np
import torch
from lazulite.audio.io import decode_audio
from lazulite.models.audio import AudioBuffer
from lazulite.alignment.japanese.backend import open_backend
from concat import concatenate

torch.set_num_threads(8)
media = read(OUT / 'audio-sources.json')
backend = open_backend(ROOT / '.models/nextfire', 'cuda')
try:
    for song, evidence, cache in inputs():
        sid = song['id']
        path = cache / f'{sid}-concat_core-original.npy'
        if path.exists():
            continue
        original = decode_audio(ROOT / media[sid]['audio'], sample_rate=16000, channels=1)
        mapping = read(evidence / f'{sid}-concat_core-map.json')['pieces']
        signal = concatenate(original.samples[0], mapping)
        np.save(path, backend.emissions(AudioBuffer(signal[None, :].copy(), 16000, sid)))
        print('ORIGINAL EMISSIONS', sid, flush=True)
finally:
    backend.close()

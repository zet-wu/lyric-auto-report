"""Reuse native NextFire core emissions for the reduced M7 decoder matrix."""
from common import *
product_imports()
import numpy as np
import soundfile as sf
from lazulite.models.audio import AudioBuffer
from lazulite.audio.io import resample_audio

for song, evidence, cache in inputs():
    sid = song['id']
    wave, rate = sf.read(ROOT / '.cache/comparison/stems/demucs' / f'{sid}.wav', dtype='float32', always_2d=True)
    audio = resample_audio(AudioBuffer(wave.T.copy(), rate), sample_rate=16000, channels=1)
    np.save(cache / f'{sid}-vocals.npy', audio.samples)
    prefix = ROOT / '.cache/phase2/emissions' / f'{sid}-demucs-nextfire-float-core-all'
    metadata = read(prefix.with_suffix('.json'))
    if metadata['mapping']['sample_rate'] != 16000:
        raise ValueError('M7 requires the native 16 kHz core mapping')
    dump(evidence / f'{sid}-concat_core-map.json', {'pieces': metadata['mapping']['pieces']})
    np.save(cache / f'{sid}-concat_core-emissions.npy', np.load(prefix.with_suffix('.npy')))
    baseline = read(ROOT / 'results/M1/predictions/G1-studio-demucs-nextfire' / f'{sid}.json')
    dump(evidence / f'{sid}-analysis.json.gz', baseline['analysis'])
    print('REUSED EMISSIONS', sid, flush=True)

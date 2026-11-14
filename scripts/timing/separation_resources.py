"""Serial CUDA-only five-song separator benchmark with three warm repeats."""
from additional_separators import load, sync
from common import *
product_imports()
from lazulite.models.audio import AudioBuffer
from lazulite.audio.io import decode_audio
import additional_separators as adapters
import argparse, hashlib, random, threading, time
import numpy as np
import torch
import psutil
import pynvml

adapters.AudioBuffer = AudioBuffer
parser = argparse.ArgumentParser()
parser.add_argument('model', choices=['demucs', 'scnet', 'dttnet', 'bs_roformer', 'mel_roformer', 'windowed'])
args = parser.parse_args()
torch.set_num_threads(8)
assert torch.cuda.is_available(), 'CUDA required'
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)
out = ROOT / 'results/separation-resources'
inputs = read(ROOT / 'configs/separation-resources-inputs.json')
model, infer, identity = load(args.model, 'cuda')
records = []
for song in inputs:
    path = ROOT / song['audio']
    with path.open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == song['sha256']
    audio = decode_audio(path, sample_rate=44100, channels=2)
    samples = audio.samples
    random.seed(0); np.random.seed(0); torch.manual_seed(0)
    infer(samples[:, :min(samples.shape[1], 44100 * 30)])
    sync('cuda')
    for repeat in range(3):
        random.seed(0); np.random.seed(0); torch.manual_seed(0)
        torch.cuda.reset_peak_memory_stats()
        stop = threading.Event()
        measurements = []
        def observe():
            while not stop.is_set():
                process = psutil.Process()
                rss = process.memory_info().rss
                for child in process.children(recursive=True):
                    try: rss += child.memory_info().rss
                    except psutil.NoSuchProcess: pass
                measurements.append((time.monotonic(), pynvml.nvmlDeviceGetPowerUsage(handle) / 1000, rss))
                stop.wait(.02)
        thread = threading.Thread(target=observe, daemon=True)
        thread.start()
        start = time.monotonic()
        vocals = infer(samples)
        sync('cuda')
        seconds = time.monotonic() - start
        stop.set(); thread.join()
        assert vocals.shape == samples.shape and np.isfinite(vocals).all()
        energy = sum((b[0]-a[0])*(a[1]+b[1])/2 for a,b in zip(measurements, measurements[1:]))
        records.append({'song': song['id'], 'repeat': repeat + 1, 'seconds': seconds,
                        'duration': samples.shape[1]/44100,
                        'allocated_bytes': torch.cuda.max_memory_allocated(),
                        'rss_bytes': max(m[2] for m in measurements), 'board_energy_joules': energy,
                        'power_samples': len(measurements)})
        dump(out / (args.model + '.json'), {'model': args.model, 'identity': identity,
             'inputs': inputs, 'records': records, 'torch': torch.__version__,
             'gpu': torch.cuda.get_device_name(), 'threads': torch.get_num_threads(),
             'scope': 'Serial CUDA; warm inference including transfer and CPU return; decode, load and disk output excluded. Three repeats per song; board power includes idle consumption.'})
        print(args.model, song['id'], repeat + 1, round(seconds, 3), flush=True)

"""Serial resource benchmark; imports unchanged product/upstream separators."""
from common import *
import argparse, hashlib, subprocess, threading, time

parser = argparse.ArgumentParser()
parser.add_argument('model', choices=['demucs', 'bs', 'kim'])
parser.add_argument('repeat', type=int)
args = parser.parse_args()
product_imports()
timing_imports()
import soundfile as sf
import torch
from lazulite.audio.io import decode_audio
from lazulite.audio.separation import DemucsConfig, DemucsSeparator
from timing.bs_lead import separate
from timing.separation import separate_vocals

out = ROOT / 'results/ablation/resource-benchmark'
work = ROOT / '.cache/ablation/resource-benchmark' / f'{args.model}-{args.repeat}'
work.mkdir(parents=True, exist_ok=True)
song = read(OUT / 'reference.json')[0]
source = ROOT / song['audio']
weights = {
    'demucs': ROOT / '.models/torch/hub/checkpoints/955717e8-8726e21a.th',
    'bs': UPSTREAM / 'models/bs-karaoke/bs_roformer_karaoke_frazer_becruily.ckpt',
    'kim': UPSTREAM / 'models/separator/melband-roformer-kim-vocals/MelBandRoformer.ckpt',
}[args.model]
torch.set_num_threads(8)
torch.manual_seed(0)
assert torch.cuda.is_available()
torch.cuda.init()
torch.cuda.reset_peak_memory_stats()
stop = threading.Event()
samples = []

def observe():
    while not stop.is_set():
        result = subprocess.run(['nvidia-smi', '--query-compute-apps=pid,used_gpu_memory',
                                 '--format=csv,noheader,nounits'], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                pid, memory = (part.strip() for part in line.split(','))
                if pid == str(os.getpid()) and memory.isdigit():
                    samples.append(int(memory))
        stop.wait(.1)

observer = threading.Thread(target=observe, daemon=True)
observer.start()
torch.cuda.synchronize()
started = time.monotonic()
if args.model == 'demucs':
    audio = decode_audio(source, sample_rate=44100, channels=2)
    separator = DemucsSeparator(DemucsConfig())
    vocals = separator.separate(audio)
    target = work / 'vocals.wav'
    sf.write(target, vocals.samples.T, vocals.sample_rate, subtype='FLOAT')
    separator.close()
else:
    target, _ = (separate if args.model == 'bs' else separate_vocals)(source, work)
torch.cuda.synchronize()
elapsed = time.monotonic() - started
stop.set()
observer.join()
info = sf.info(target)
record = {
    'model': args.model, 'repeat': args.repeat, 'song': song['id'], 'audio': song['audio'],
    'duration_seconds': info.frames / info.samplerate,
    'weight_path': str(weights), 'weight_bytes': weights.stat().st_size,
    'weight_sha256': hashlib.sha256(weights.read_bytes()).hexdigest(),
    'seconds': elapsed, 'realtime_factor': elapsed / (info.frames / info.samplerate),
    'torch_peak_allocated_bytes': torch.cuda.max_memory_allocated(),
    'torch_peak_reserved_bytes': torch.cuda.max_memory_reserved(),
    'nvidia_process_peak_mib_sampled': max(samples) if samples else None,
    'nvidia_samples': len(samples),
    'gpu': torch.cuda.get_device_name(), 'gpu_bytes': torch.cuda.get_device_properties(0).total_memory,
    'torch': torch.__version__, 'threads': torch.get_num_threads(),
    'timing_scope': 'New process per run; CUDA initialized and entry-point imports done before timer. '
                    'Weights local; includes lazy runtime imports, decode, model load, separation, native '
                    'output/checks and close. Excludes downloads, interpreter startup and post-run hashing. '
                    'Original wrappers differ in ancillary validation and output count.',
}
dump(out / f'{args.model}-{args.repeat}.json', record)
print(json.dumps(record, ensure_ascii=False), flush=True)

"""Serial fixed-input CPU/CUDA inference benchmark, resumable by identity."""
import argparse, os
from separator_registry import MODELS
parser = argparse.ArgumentParser()
parser.add_argument('model', choices=MODELS)
parser.add_argument('--device', choices=['cpu','cuda'], default='cuda')
args = parser.parse_args()
if args.device == 'cpu': os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['OMP_NUM_THREADS'] = '8'; os.environ['MKL_NUM_THREADS'] = '8'; os.environ['OPENBLAS_NUM_THREADS'] = '8'
from common import *
from native_separators import load, digest
product_imports()
from lazulite.audio.io import decode_audio
import fcntl, platform, random, threading, time, subprocess
import numpy as np
import torch, psutil
lock = (ROOT / '.cache/separator-resources.lock').open('w')
fcntl.flock(lock, fcntl.LOCK_EX)
torch.set_num_threads(8)
assert torch.cuda.is_available() == (args.device == 'cuda')
handle = None
if args.device == 'cuda':
    import pynvml
    pynvml.nvmlInit(); handle = pynvml.nvmlDeviceGetHandleByIndex(0)
def sync():
    if handle is not None: torch.cuda.synchronize()
def seed():
    random.seed(0); np.random.seed(0); torch.manual_seed(0)
out = ROOT / 'results/separation-resources'
path = out / (args.model + ('' if args.device == 'cuda' else '-cpu') + '.json')
inputs = read(ROOT / ('configs/separation-cpu-inputs.json' if args.device == 'cpu' else 'configs/separation-resources-inputs.json'))
for song in inputs:assert digest(ROOT/song['audio'])==song['sha256']
model, infer, identity = load(args.model, args.device)
records = []
if path.exists():
    previous = read(path)
    for key in ('model','config','state_sha256','weight_sha256','providers','onnx_threads'):
        assert previous['identity'].get(key) == json.loads(json.dumps(identity.get(key))), ('Changed identity', key)
    assert previous['inputs'] == inputs and previous['torch'] == torch.__version__
    if handle is not None: assert previous['gpu'] == torch.cuda.get_device_name()
    records = previous['records']
    if len(records) == 3*len(inputs):
        print('VERIFIED REUSE', path, flush=True); raise SystemExit(0)
for song in inputs:
    source = ROOT / song['audio']; assert digest(source) == song['sha256']
    done = {r['repeat'] for r in records if r['song'] == song['id']}
    if done == {1,2,3}: continue
    samples = decode_audio(source, sample_rate=44100, channels=2).samples
    if args.device == 'cpu':
        samples = samples[:, int(song['start_seconds']*44100):int(song['end_seconds']*44100)]
        assert samples.shape == (2,1323000)
    print('WARMUP',args.model,args.device,song['id'],flush=True)
    seed(); warm = infer(samples[:, :min(samples.shape[1],44100*30)]); sync(); del warm
    for repeat in range(1,4):
        if repeat in done: continue
        print('START REPEAT',args.model,args.device,song['id'],repeat,flush=True)
        seed()
        if handle is not None: torch.cuda.reset_peak_memory_stats()
        stop = threading.Event(); measurements = []
        def sample():
            process = psutil.Process(); processes = [process] + process.children(recursive=True)
            rss = 0; pids = {p.pid for p in processes}
            for p in processes:
                try: rss += p.memory_info().rss
                except psutil.NoSuchProcess: pass
            power = memory = None
            if handle is not None:
                power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
                memory = sum(p.usedGpuMemory for p in pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
                             if p.pid in pids and isinstance(p.usedGpuMemory,int) and p.usedGpuMemory < 2**60)
            measurements.append((time.monotonic(),power,rss,memory))
        def observe():
            while not stop.wait(.02): sample()
        sample(); thread = threading.Thread(target=observe,daemon=True); thread.start()
        start = time.monotonic()
        try:
            vocals = infer(samples); sync(); seconds = time.monotonic()-start
        finally:
            stop.set(); thread.join(); sample()
        assert vocals.shape == samples.shape and np.isfinite(vocals).all()
        energy = (sum((b[0]-a[0])*(a[1]+b[1])/2 for a,b in zip(measurements,measurements[1:]))
                  if handle is not None else None)
        records.append({'song':song['id'], 'repeat':repeat, 'seconds':seconds, 'duration':samples.shape[1]/44100,
            'allocated_bytes':torch.cuda.max_memory_allocated() if handle is not None and args.model != 'sug' else None,
            'process_gpu_bytes':max(m[3] for m in measurements) if handle is not None else None,
            'rss_bytes':max(m[2] for m in measurements), 'board_energy_joules':energy,
            'power_samples':len(measurements) if handle is not None else 0,
            'output_shape':list(vocals.shape), 'output_finite':True})
        del vocals
        dump(path, {'model':args.model, 'device':args.device, 'identity':identity, 'inputs':inputs, 'records':records,
            'torch':torch.__version__, 'gpu':torch.cuda.get_device_name() if handle is not None else None,
            'threads':torch.get_num_threads(), 'cpu':subprocess.check_output(['lscpu'],text=True),
            'platform':platform.platform(), 'scope':'Serial warm inference including transfer and CPU return; decode, load, encoding and disk output excluded. Three repeats per song; GPU board energy includes idle consumption.'})
        print('DONE',args.model,args.device,song['id'],repeat,round(seconds,3),flush=True)

"""Run the fixed separator resource matrix serially in pinned environments."""
from separator_registry import *
import argparse, os, subprocess, json
p=argparse.ArgumentParser();p.add_argument('--devices',nargs='+',default=['cuda','cpu'],choices=['cuda','cpu'])
p.add_argument('--models',nargs='+',default=list(MODELS),choices=MODELS);a=p.parse_args()
logs=ROOT/'.cache/logs/separation-resources';logs.mkdir(parents=True,exist_ok=True)
for device in a.devices:
 for name in a.models:
    env=dict(os.environ,OMP_NUM_THREADS='8',MKL_NUM_THREADS='8',OPENBLAS_NUM_THREADS='8',PYTHONUNBUFFERED='1')
    if device=='cpu':env['CUDA_VISIBLE_DEVICES']=''
    path=logs/f'{name}-{device}.log'
    print('START',name,device,flush=True)
    with path.open('a') as log:
        command=[str(interpreter(name)),str(ROOT/'scripts/timing/separation_resources.py'),name,'--device',device]
        result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:
            error=ROOT/'results/separation-resources'/f'{name}-{device}-error.json'
            error.write_text(json.dumps({'model':name,'device':device,'returncode':result.returncode,'log':str(path.relative_to(ROOT))},indent=2)+'\n')
            raise SystemExit(result.returncode)
        error=ROOT/'results/separation-resources'/f'{name}-{device}-error.json'
        if error.exists():error.unlink()
    print('FINISH',name,device,flush=True)

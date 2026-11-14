from pathlib import Path
import json, os, sys, gzip, re
ROOT=Path(__file__).resolve().parents[2]
os.chdir(ROOT)
os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
os.environ['TORCHINDUCTOR_CACHE_DIR']=str(ROOT/'.cache/torchinductor')
os.environ['TRITON_CACHE_DIR']=str(ROOT/'.cache/triton')
os.environ['TORCH_HOME']=str(ROOT/'.models/torch')
os.environ['HF_HOME']=str(ROOT/'.cache/huggingface')
os.environ['NUMBA_CACHE_DIR']=str(ROOT/'.cache/numba')
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
os.environ['NODE_PATH']=str(ROOT/'.deps/node/node_modules')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['OMP_NUM_THREADS']='8'

OUT=ROOT/'results/comparison'
CACHE=ROOT/'.cache/comparison'
UPSTREAM=ROOT/'.deps/comparison/timing'
STUDIO=ROOT/'.deps/comparison/studio'
for p in (OUT,CACHE): p.mkdir(parents=True,exist_ok=True)
def portable(value):
    from enum import Enum
    if isinstance(value,Enum):return value.value
    if isinstance(value,str):
        value=value.replace(str(ROOT)+'/', '')
        value=re.sub(r'/(?:opt)/Miniconda3/', '<python>/', value)
        value=re.sub(r'\x1b\[[0-9;]*m','',value)
        value=re.sub(r'(?m)^20\d\d-\d\d-\d\d \d\d:\d\d:\d\d(?:\.\d+)? \| ', '', value)
        return value
    if isinstance(value,dict):return {portable(k):portable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [portable(v) for v in value]
    return value
def dump(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+f'.{os.getpid()}.part')
    temporary.write_text(json.dumps(portable(data),ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    temporary.replace(path)
def read(path):
    path=Path(path)
    if path.exists():return json.loads(path.read_text())
    with gzip.open(str(path)+'.gz','rt') as f:return json.load(f)
def exists(path):return Path(path).exists() or Path(str(path)+'.gz').exists()
def product_imports():sys.path[:0]=[str(STUDIO),str(ROOT/'.deps/comparison/lazulite/src')]
def timing_imports():sys.path.insert(0,str(UPSTREAM))

import hashlib
def sha(path):
    with Path(path).open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def songs():
    return [s for s in read(OUT/"reference.json") if s["id"] not in ("s11","s13","s14")]

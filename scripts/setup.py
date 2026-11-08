"""Create the repository-local Python and Node runtime from a fresh clone."""
from pathlib import Path
import argparse, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
parser=argparse.ArgumentParser()
parser.add_argument('--models',action='store_true')
args=parser.parse_args()
for name in ('git','ffmpeg','ffprobe','node','npm'):
    if not shutil.which(name): raise SystemExit('Install system prerequisite: '+name)
venv=ROOT/'.venvs/research'
if not venv.exists():subprocess.run([sys.executable,'-m','venv',str(venv)],check=True)
python=venv/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
bindir=python.parent
os.environ.update(UV_CACHE_DIR=str(ROOT/'.cache/uv'),PIP_CACHE_DIR=str(ROOT/'.cache/pip'),
    HF_HOME=str(ROOT/'.cache/huggingface'),TORCH_HOME=str(ROOT/'.models/torch'),
    PATH=str(bindir)+os.pathsep+os.environ['PATH'])
def run(*argv):subprocess.run(list(map(str,argv)),check=True,cwd=ROOT)
run(python,'-m','pip','install','uv==0.13.7')
run(bindir/'uv','pip','install','--python',python,'-r',ROOT/'requirements/research.txt','-c',ROOT/'requirements/linux-cuda-lock.txt')
run(python,ROOT/'scripts/download.py','sources')
node=ROOT/'.deps/node';node.mkdir(exist_ok=True)
shutil.copyfile(ROOT/'configs/node-package.json',node/'package.json')
run('npm','install','--prefix',node,'--cache',ROOT/'.cache/npm')
run(bindir/'uv','pip','install','--python',python,'--target',ROOT/'.deps/timing/models/tifa/deps',
    '--no-deps','-r',ROOT/'.deps/timing/scripts/tifa-requirements.txt')
run(bindir/'uv','pip','install','--python',python,'--target',ROOT/'.deps/msst-packages',
    '--no-deps','-r',ROOT/'requirements/separation.txt')
if args.models:run(python,ROOT/'scripts/download.py','models')

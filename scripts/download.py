"""Prepare pinned public sources and model assets inside this repository."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys, urllib.request

ROOT = Path(__file__).resolve().parents[1]
os.environ.update(HF_HOME=str(ROOT/'.cache/huggingface'),TORCH_HOME=str(ROOT/'.models/torch'),UV_CACHE_DIR=str(ROOT/'.cache/uv'),XDG_CACHE_HOME=str(ROOT/'.cache'))
os.environ['PATH']=str(Path(sys.executable).parent)+os.pathsep+os.environ['PATH']

def run(*args):
    subprocess.run(list(map(str,args)),check=True,cwd=ROOT)

def fetch(url,path,sha256=None):
    path=ROOT/path
    if path.exists() and sha256 and hashlib.file_digest(path.open('rb'),'sha256').hexdigest()==sha256:return
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.part')
    with urllib.request.urlopen(url) as source,temporary.open('wb') as out:
        import shutil
        shutil.copyfileobj(source,out)
    if sha256 and hashlib.file_digest(temporary.open('rb'),'sha256').hexdigest()!=sha256:
        raise ValueError('Download checksum mismatch: '+str(path.relative_to(ROOT)))
    temporary.replace(path)

def sources():
    for name,item in json.loads((ROOT/'configs/sources.json').read_text()).items():
        folder=ROOT/'.deps'/name
        if (folder/'.git').exists():
            head=subprocess.check_output(['git','-C',str(folder),'rev-parse','HEAD'],text=True).strip()
            if head==item['commit']:continue
            raise RuntimeError('Unexpected checkout: '+name)
        folder.mkdir(parents=True,exist_ok=True)
        run('git','init',folder)
        run('git','-C',folder,'fetch','--depth','1',item['url'],item['commit'])
        run('git','-C',folder,'checkout','--detach','FETCH_HEAD')

def models():
    from huggingface_hub import snapshot_download
    snapshot_download('NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn',
        revision='2ab2b5f46539ee284703c281f286b01d2410ee12',local_dir=ROOT/'.models/nextfire')
    expected=json.loads((ROOT/'configs/models.json').read_text())['nextfire']['files']
    for name,item in expected.items():
        path=ROOT/'.models/nextfire'/name
        with path.open('rb') as stream:actual=hashlib.file_digest(stream,'sha256').hexdigest()
        if actual!=item['sha256']:raise ValueError('NextFire checksum mismatch: '+name)
    fetch('https://dl.fbaipublicfiles.com/mms/torchaudio/ctc_alignment_mling_uroman/model.pt',
          '.models/mms-fa/model.pt',json.loads((ROOT/'configs/models.json').read_text())['mms-fa']['sha256'])
    (ROOT/'.models/mms-fa/alignment-model.json').write_text('{"type":"torchaudio-mms-fa","weights":"model.pt"}\n')
    for name in ('download_ctc.py','download_tifa.py','download_bs_karaoke.py','download_separator.py'):
        run(sys.executable,ROOT/'.deps/timing/scripts'/name)
    for asset in json.loads((ROOT/'configs/separation-models.json').read_text()):
        fetch(asset['url'],asset['path'],asset['sha256'])
    from demucs.pretrained import get_model
    os.environ['TORCH_HOME']=str(ROOT/'.models/torch')
    get_model('htdemucs')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('part',choices=['sources','models','all'],default='all',nargs='?')
    args=parser.parse_args()
    if args.part in ('sources','all'):sources()
    if args.part in ('models','all'):models()

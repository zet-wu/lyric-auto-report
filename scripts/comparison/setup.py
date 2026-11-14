"""Install the pinned comparison adapters without modifying upstream algorithms."""
from common import *
import subprocess,urllib.request,shutil
research=ROOT/'.venvs/research/bin/python';native=ROOT/'.venvs/milikara/bin/python'
os.environ['PIP_CACHE_DIR']=str(ROOT/'.cache/pip')
def run(*args,**kwargs):subprocess.run(list(map(str,args)),check=True,cwd=ROOT,**kwargs)
for name,item in read(ROOT/'configs/comparison-sources.json').items():
 folder=ROOT/'.deps/comparison'/name
 if not (folder/'.git').exists():
  folder.mkdir(parents=True,exist_ok=True);run('git','init',folder);run('git','-C',folder,'fetch','--depth','1',item['url'],item['commit']);run('git','-C',folder,'checkout','--detach','FETCH_HEAD')
 assert subprocess.check_output(['git','-C',str(folder),'rev-parse','HEAD'],text=True).strip()==item['commit'],name
models=ROOT/'.deps/comparison/timing/models'
if not models.exists():models.symlink_to(ROOT/'.deps/timing/models',target_is_directory=True)
run(research,'-m','pip','install','PyQt6==6.10.2','Janome==0.5.0','pysubs2==1.8.1','jieba==0.42.1','jaconv==0.5.0','nltk==3.10.4','nvidia-ml-py==13.615.71')
run(research,'-m','pip','install','--no-deps',ROOT/'.deps/comparison/yohane')
run(research,'-m','pip','--python',native,'install','onnxruntime-gpu==1.23.2','ml_dtypes==0.5.3')
sug=ROOT/'.venvs/sug/bin/python'
if not sug.exists():run(research,'-m','venv','--without-pip',sug.parent.parent)
# Share the pinned CUDA runtime; explicitly required SUG packages take priority.
version=subprocess.check_output([str(sug),'-c','import sys;print(f"python{sys.version_info.major}.{sys.version_info.minor}")'],text=True).strip()
site=sug.parent.parent/'lib'/version/'site-packages'
site.joinpath('shared-runtime.pth').write_text('\n'.join(str(p.parent.parent/'lib'/version/'site-packages') for p in (research,native))+'\n')
run(research,'-m','pip','--python',sug,'install','transformers==5.15.0','audio-separator==0.47.0','librosa==0.10.2.post1')
native5=ROOT/'.venvs/native5/bin/python'
if not native5.exists():run(research,'-m','venv','--without-pip',native5.parent.parent)
site=native5.parent.parent/'lib'/version/'site-packages'
site.joinpath('shared-runtime.pth').write_text('\n'.join(str(p.parent.parent/'lib'/version/'site-packages') for p in (research,native))+'\n')
run(research,'-m','pip','--python',native5,'install','transformers==5.15.0')
fakara=ROOT/'.venvs/fakara/bin/python'
if not fakara.exists():run(research,'-m','venv','--without-pip',fakara.parent.parent)
site=fakara.parent.parent/'lib'/version/'site-packages'
site.joinpath('shared-runtime.pth').write_text(str(research.parent.parent/'lib'/version/'site-packages')+'\n')
run(research,'-m','pip','--python',fakara,'install','librosa==0.11.0','transformers==5.14.1')
front=ROOT/'.deps/comparison/studio/frontend'
run('npm','exec','--yes','--package=pnpm@10.30.3','--','pnpm','--dir',front,'install','--frozen-lockfile','--ignore-scripts','--store-dir',ROOT/'.cache/pnpm')
for item in read(ROOT/'configs/comparison-assets.json'):
 path=ROOT/item['path']
 if not path.exists():
  path.parent.mkdir(parents=True,exist_ok=True)
  temporary=path.with_name(path.name+'.part')
  with urllib.request.urlopen(item['url']) as src,temporary.open('wb') as dst:shutil.copyfileobj(src,dst)
  assert temporary.stat().st_size==item['bytes'] and sha(temporary)==item['sha256'],item['path']
  temporary.replace(path)
 assert path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],item['path']
print('Comparison source and runtime setup complete')

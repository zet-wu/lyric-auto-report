"""Publish the exact untimed inputs, model identities and execution environment."""
from common import *
import subprocess,platform,shutil,hashlib,importlib.metadata as md
inputs=OUT/'inputs';inputs.mkdir(exist_ok=True)
manifest=[]
for s in songs():
 manifest.append({k:s[k] for k in ('id','name','audio','audio_sha256','ttml','ttml_sha256','duration')}|{'lines':[{'id':l['id'],'text':l['text']} for l in s['lines']]})
 for condition in ('manual','auto'):
  for suffix in ('','-project'):
   src=CACHE/'inputs'/f"{s['id']}-studio-{condition}{suffix}.json"
   dump(inputs/src.name,read(src))
dump(inputs/'songs.json',manifest)
models={}
paths=[ROOT/'.models/nextfire/model.safetensors',ROOT/'.models/mms-fa/model.pt',ROOT/'.models/comparison/sug/UVR-MDX-NET-Inst_HQ_3.onnx']
paths+=list((ROOT/'.models/milikara-native/separation').glob('*.ckpt'))
paths+=list((ROOT/'.models/torch/hub/checkpoints').glob('*.th'))
paths+=list((ROOT/'.models/torch/hub/torchaudio/models').glob('*.pt'))
paths+=list((ROOT/'.deps/comparison/timing/models/bs-karaoke').glob('*.ckpt'))
for asset in read(ROOT/'configs/comparison-assets.json'):
 p=ROOT/asset['path'];assert p.stat().st_size==asset['bytes'] and sha(p)==asset['sha256'],asset['path']
 paths.append(p)
for p in paths:
 if p.is_file():models[str(p.relative_to(ROOT))]={'bytes':p.stat().st_size,'sha256':sha(p)}
dump(OUT/'model-files.json',models)
versions={n:md.version(n) for n in ('torch','torchaudio','transformers','numpy','soundfile','SudachiPy','SudachiDict-core','pykakasi','jaconv','Janome','PyQt6','nltk','pysubs2','yohane','nvidia-ml-py')}
sug_versions=json.loads(subprocess.check_output([str(ROOT/'.venvs/sug/bin/python'),'-c',"import json,importlib.metadata as m;print(json.dumps({n:m.version(n) for n in ['torch','torchaudio','transformers','audio-separator','librosa','onnxruntime-gpu']}))"],text=True))
native_versions={}
for name,packages in [('native5',['torch','torchaudio','transformers','librosa']),('milikara',['torch','torchaudio','transformers','audio-separator','unidic-lite']),('fakara',['torch','torchaudio','transformers','librosa'])]:
 native_versions[name]=json.loads(subprocess.check_output([str(ROOT/'.venvs'/name/'bin/python'),'-c',f"import json,importlib.metadata as m;print(json.dumps({{n:m.version(n) for n in {packages!r}}}))"],text=True))
gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,memory.total,driver_version','--format=csv,noheader'],text=True).strip()
dump(OUT/'environment.json',{'python':platform.python_version(),'platform':platform.platform(),'gpu':gpu,'research_packages':versions,'sug_packages':sug_versions,'other_native_packages':native_versions,'source_commits':read(ROOT/'configs/comparison-sources.json'),'inference':'CUDA; no CPU alignment fallback','concurrency':'quality runs may overlap; durations are diagnostic, not a performance benchmark'})
checks=[]
for p in inputs.glob('*-project.json'):
 data=read(p)
 for l in data['lyrics']['lines']:
  assert l['beginMs'] is None and l['endMs'] is None
  for w in l['words']:
   for x in [w,*w['rubyUnits']]:assert x['beginMs'] is None and x['endMs'] is None
 checks.append({'file':str(p),'sha256':sha(p),'untimed':True})
for p in (OUT/'milikara/inputs/manual').glob('*.json'):
 data=read(p)
 for l in data['lines']:
  assert set(l)=={'id','text','words'}
  for w in l['words']:
   assert set(w)=={'id','text','units'}
   for u in w['units']:assert set(u)=={'id','reading'}
 checks.append({'file':str(p),'sha256':sha(p),'untimed':True})
dump(OUT/'input-audit.json',{'checks':checks,'manual_reading_supplements':[],'note':'Shared whole-word Ruby retained; no inferred Japanese reading supplements were needed.'})
print('Frozen',len(checks),'untimed inputs and',len(models),'model files')

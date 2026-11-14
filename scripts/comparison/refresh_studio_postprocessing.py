"""Reapply pinned Studio product postprocessing to unchanged saved acoustic results."""
from common import *
from types import SimpleNamespace as NS
import gzip,time,shutil
import numpy as np,soundfile as sf
product_imports()
from server.alignment_postprocessing import object_timings
from lazulite.models.audio import AudioBuffer

commit=read(ROOT/'configs/comparison-sources.json')['studio']['commit']
audit=[]
for song in songs():
 for sep,conditions in [('demucs',('manual','auto')),('bs',('manual',))]:
  stem=CACHE/'stems'/sep/(song['id']+'.wav');samples,rate=sf.read(stem,dtype='float32',always_2d=True)
  audio=AudioBuffer(samples.T.copy(),rate,song['id']);digest=sha(stem)
  for model in ('nextfire','mms-fa'):
   for condition in conditions:
    name=f"{song['id']}-{sep}-{model}-{condition}.json";path=OUT/'studio'/name;r=read(path)
    assert r['stem_sha256']==digest
    actual=path if path.exists() else Path(str(path)+'.gz')
    backup=CACHE/'studio-postprocessing-before'/actual.name;backup.parent.mkdir(exist_ok=True)
    if not backup.exists():shutil.copyfile(actual,backup)
    units=[]
    for u in r['result']['units']:
     t=u['proposed_timing'];units.append(NS(unit_id=u['unit_id'],proposed_timing=NS(start=NS(**t['start']) if t['start'] else None,end=NS(**t['end']) if t['end'] else None)))
    started=time.perf_counter()
    timings=object_timings(NS(units=units),r['projection']['mapping'],audio,model=='mms-fa',segments=[NS(**s) for s in r['analysis']['segments']])
    elapsed=time.perf_counter()-started
    if model=='nextfire':assert timings==r['object_timings']
    changed=sum(timings[k]['end']!=r['object_timings'][k]['end'] for k in timings)
    assert all(timings[k]['start']==r['object_timings'][k]['start'] for k in timings)
    r['object_timings']=timings;r['postprocessing']={'studio_commit':commit,'source_sha256':sha(STUDIO/'server/alignment_postprocessing.py'),'seconds':elapsed,'acoustic_result_reused':True,'segments':'saved current analysis segments'}
    target=Path(str(path)+'.gz');temp=Path(str(target)+'.part');temp.write_bytes(gzip.compress(json.dumps(portable(r),ensure_ascii=False,indent=2,allow_nan=False).encode(),mtime=0));temp.replace(target)
    if path.exists():path.unlink()
    audit.append({'song':song['id'],'separator':sep,'model':model,'condition':condition,'changed_ends':changed,'seconds':elapsed})
    print('REFRESH',name,changed,flush=True)
dump(OUT/'studio-postprocessing-audit.json',{'studio_commit':commit,'scope':'72 saved result cases; unchanged acoustic inference and inputs; native product postprocessing and frontend adoption rerun','records':audit})

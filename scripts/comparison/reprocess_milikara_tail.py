"""Apply native energy-tail postprocessing to frozen off-strategy predictions."""
from common import *
import time
import numpy as np
sys.path.insert(0,str(ROOT/'.deps/comparison/milikara'))
from kara_align.models import AlignmentResult,Project,stable_hash
from kara_align.align.tail import apply_tail
from kara_align.align.runner import _follow_units
from kara_align.align.activity import detect_activity
from kara_align.align.checks import check_uncovered
from kara_align.audio.io import load_audio
from kara_align.audio.analysis import rms_envelope_db
from kara_align.project.exports import export_alignment

def main():
 audit_path=OUT/'milikara-energy-audit.json'
 audit=read(audit_path)['records'] if audit_path.exists() else []
 for sep,condition in [('milikara','manual'),('bs','manual'),('milikara','auto')]:
  for song in songs():
   sid=song['id'];path=OUT/'milikara/runs'/f'{sid}-{sep}-{condition}.json';r=read(path)
   if r['result']['config']['tail']['strategy']=='energy':continue
   assert r['status']=='ok' and r['result']['config']['tail']['strategy']=='off'
   before=AlignmentResult.model_validate(r['result']);result=before.model_copy(deep=True)
   assert all(u.tail is None and u.manual is None for u in result.units)
   work=CACHE/'milikara-projects'/f'{sid}-{sep}-{condition}';project=Project.model_validate(read(work/'project.json'))
   assert project.lyrics.reading_revision()==result.snapshot.lyrics_reading_revision
   asset=project.asset('vocals');assert asset.sha256==r['stem_sha256']
   start=time.monotonic();data,rate=load_audio(work/asset.path,mono=True);env=rms_envelope_db(data[0],rate,hop_ms=10.0);del data
   shift=round(asset.origin_offset_samples*1000/asset.sample_rate/10)
   if shift>0:env=np.concatenate([np.full(shift,float(env.min()) if env.size else -120,dtype=env.dtype),env])
   elif shift<0:env=env[-shift:]
   result.config.tail.strategy='energy';voices={l['id']:l.get('voice','main') for l in r['export']['lyrics']['lines']};issues=[]
   for voice in set(voices.values()):issues+=apply_tail([u for u in result.units if voices[u.line_id]==voice],result.config.tail,(env,10.0),result.config.checks.min_unit_ms)
   _follow_units(result.lines,result.units)
   old_uncovered={i.code for i in check_uncovered(before.lines,detect_activity(env,10.0))}
   result.issues=[i for i in result.issues if i.code not in old_uncovered]+issues+check_uncovered(result.lines,detect_activity(env,10.0))
   result.snapshot.config_hash=stable_hash(result.config.model_dump(mode='json'))
   result.coverage.from_ms=min(l.start_ms for l in result.lines if l.start_ms is not None)
   result.coverage.to_ms=max(l.end_ms for l in result.lines if l.end_ms is not None)
   changes={'extended':0,'trimmed':0}
   for old,new in zip(before.units,result.units):
    assert old.start_ms==new.start_ms and old.model_end_ms==new.model_end_ms
    if old.end_ms is not None and new.end_ms is not None:
     changes['extended']+=new.end_ms>old.end_ms;changes['trimmed']+=new.end_ms<old.end_ms
   r['config']['tail']['strategy']='energy';r['result']=result.model_dump(mode='json');r['export']=json.loads(export_alignment(project,result).content)
   assert r['export']['lyrics']==read(path)['export']['lyrics']
   r['tail_reprocessing']={'strategy':'energy','source_strategy':'off','acoustic_and_decode_reused':True,'seconds':time.monotonic()-start,**changes}
   dump(path,r);audit.append({'song':sid,'separator':sep,'condition':condition,**changes});print(sid,sep,condition,changes,flush=True)
 dump(OUT/'milikara-energy-audit.json',{'strategy':'energy','acoustic_and_decode_reused':True,'records':audit})
if __name__=='__main__':main()

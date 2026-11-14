"""Repeat confirmed human readings over registered separators and two persistence paths."""
from common import *
product_imports()
from concat import make_map,concatenate,map_unit
from ctc_benchmark import align
from dataclasses import asdict
import argparse,time
import numpy as np,soundfile as sf,torch
from lazulite.audio.io import decode_audio,resample_audio
from lazulite.audio.activity import analyze_vocals
from lazulite.models.audio import AudioBuffer
from lazulite.alignment.japanese.backend import NextFireBackend,NextFireConfig
sys.path.insert(0,str(ROOT/'scripts/timing'))
from separator_registry import MODELS as SEPARATORS, NEW
parser=argparse.ArgumentParser()
parser.add_argument('--models',nargs='+',default=list(SEPARATORS),choices=SEPARATORS)
parser.add_argument('--songs',nargs='+',help='Resume selected song IDs without changing the scoring cohort')
args=parser.parse_args()
torch.set_num_threads(8)
backend=NextFireBackend(NextFireConfig(ROOT/'.models/nextfire','cuda'))
vocab=read(ROOT/'.models/nextfire/vocab.json')
targets={kind:{s['id']:s for s in read(OUT/(kind+'.json'))} for kind in ('confirmed-targets',)}
refs={s['id']:s for s in read(ROOT/'results/timing/reference.json')}
destination=ROOT/'results/separation-alignment'
for name in args.models:
 stems={r['song']:r for r in read(ROOT/'results/separation-alignment'/('stems-'+name+'.json'))['records']} if name in NEW else None
 for sid in targets['confirmed-targets']:
  if args.songs and sid not in args.songs:continue
  source=ROOT/'.cache/timing/audio'/(Path(refs[sid]['audio']).stem+'.wav') if name=='demucs' else ROOT/'.cache/ablation/stems'/name/(sid+'.wav')
  if stems is not None:
   source=ROOT/stems[sid]['path']
   assert sha(source)==stems[sid]['sha256']
  expected=[destination/'predictions'/name/persist/(sid+'--'+mode+'--confirmed-targets.json') for persist in ('float','pcm24') for mode in MODES]
  if name not in NEW and all(exists(p) for p in expected):continue
  wave,rate=sf.read(source,dtype='float32',always_2d=True)
  mix=decode_audio(ROOT/refs[sid]['audio'],sample_rate=44100,channels=2)
  for persist in ('float','pcm24'):
   cache_identity={'stem_sha256':sha(source),'source_sha256':sha(ROOT/refs[sid]['audio']),'targets_sha256':sha(OUT/'confirmed-targets.json'),'separator':name,'persistence':persist,'models_sha256':sha(ROOT/'configs/models.json'),'sources_sha256':sha(ROOT/'configs/sources.json')}
   work=ROOT/'.cache/separation-alignment'/name/persist/sid;work.mkdir(parents=True,exist_ok=True)
   identity_path=work/'identity.json'
   if identity_path.exists():assert read(identity_path)==cache_identity, ('Cache identity changed',name,persist,sid)
   elif name in NEW:
    assert not any(work.glob('*.npy')), 'Unidentified acoustic cache'
    dump(identity_path,cache_identity)
   if persist=='float':
    audio=AudioBuffer(wave.T.copy(),rate)
    analysis=analyze_vocals(audio,reference=mix)
    gain=1.
   else:
    gain=min(1.,(1-2**-23)/float(np.max(np.abs(wave)))) if np.any(wave) else 1.
    path=work/'vocals.flac'
    if not path.exists():sf.write(path,wave.astype(np.float64)*gain,rate,subtype='PCM_24')
    loaded,sr=sf.read(path,dtype='float32',always_2d=True)
    audio=AudioBuffer(loaded.T.copy(),sr)
    analysis=analyze_vocals(audio)
   segments=[asdict(s) for s in analysis.segments]
   y=resample_audio(audio,sample_rate=16000,channels=1).samples[0]
   dump(destination/'audio'/name/persist/(sid+'.json'),{'song':sid,'gain':gain,'analysis':asdict(analysis),'samples16k':len(y)})
   for mode in MODES:
    mapping=None if mode=='global' else make_map(segments,len(y),mode=='concat_padded')
    signal=y if mapping is None else concatenate(y,mapping)
    if mapping:dump(destination/'maps'/name/persist/(sid+'-'+mode+'.json'),mapping)
    path=work/(mode+'.npy')
    if not path.exists():np.save(path,backend.emissions(AudioBuffer(signal[None,:],16000)))
    em=np.load(path)
    for kind,lookup in targets.items():
     if sid not in lookup:continue
     dest=destination/'predictions'/name/persist/(sid+'--'+mode+'--'+kind+'.json')
     if exists(dest):continue
     song=lookup[sid]
     usable=[u for l in song['lines'] for u in l['units'] if u['text']]
     preds=align(em,0,usable,vocab,29)
     if preds is not None and mapping:preds=[map_unit(p,mapping) for p in preds]
     rows=[];offset=0
     for line in song['lines']:
      row=[]
      for u in line['units']:
       if not u['text']:row.append(None);continue
       row.append(preds[offset] if preds is not None else None);offset+=1
      rows.append(row)
     dump(dest,{'song':sid,'kind':kind,'separator':name,'persistence':persist,'mode':mode,
       'experiment':f'{name}/{persist}/{mode}/{kind}','predictions':rows,
       'omitted_empty_targets':sum(not u['text'] for l in song['lines'] for u in l['units'])})
    print(name,persist,sid,mode,flush=True)
backend.close()

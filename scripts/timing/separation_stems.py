"""Audit native equivalence and reuse source-matched GPU stems for downstream."""
from common import *
from native_separators import load, digest
from separator_registry import NEW
import argparse, random
import numpy as np, soundfile as sf, torch
product_imports()
from lazulite.audio.io import decode_audio
p=argparse.ArgumentParser();p.add_argument('model',choices=NEW);a=p.parse_args()
assert torch.cuda.is_available();torch.set_num_threads(8)
model,infer,identity=load(a.model,'cuda')
refs={s['id']:s for s in read(ROOT/'results/timing/reference.json')}
ids=[s['id'] for s in read(ROOT/'results/milikara/confirmed-targets.json')]
folder=ROOT/'.cache/separator-adapter'/a.model;folder.mkdir(parents=True,exist_ok=True)
x=decode_audio(ROOT/refs['s01']['audio'],sample_rate=44100,channels=2).samples[:,:44100*30]
random.seed(0);np.random.seed(0);torch.manual_seed(0)
y=infer(x)
random.seed(0);np.random.seed(0);torch.manual_seed(0)
z=infer.native_check(x,folder)
assert y.shape==z.shape,(y.shape,z.shape)
error=float(np.max(np.abs(y-z)))
# Native audio-separator writes through int16 before container encoding.
limit=2/32768 if a.model in ('sug','milikara') else 1e-5
assert error<=limit,(a.model,error,limit)
records=[]
manifest_path=ROOT/'results/separation-alignment'/('stems-'+a.model+'.json')
prior=read(manifest_path) if manifest_path.exists() else None
if prior:assert prior['identity']==json.loads(json.dumps(identity)), 'Changed separator identity'
previous_stems={r['song']:r for r in prior['records']} if prior else {}
for sid in ids:
    song=refs[sid];source=ROOT/song['audio']
    assert digest(source)==song['audio_sha256']
    cache=ROOT/'.cache/comparison/stems'/a.model/(sid+'.wav')
    meta=ROOT/'results/comparison/separation'/a.model/(sid+'.json')
    if cache.exists() and meta.exists():
        previous=read(meta)
        assert previous['source_sha256']==digest(source) and previous['sha256']==digest(cache)
        origin='comparison';target=cache
    elif a.model=='bs' and (ROOT/'.cache/ablation/stems/bs'/(sid+'.wav')).exists():
        target=ROOT/'.cache/ablation/stems/bs'/(sid+'.wav');origin='ablation'
        old=read(ROOT/'results/ablation/separation/bs'/(sid+'.json'))
        assert old['sha256']==digest(target) and old['upstream']['checkpoint_sha256']==identity['weight_sha256']
    elif sid in previous_stems:
        previous=previous_stems[sid];target=ROOT/previous['path']
        assert previous['source_sha256']==digest(source) and previous['sha256']==digest(target)
        origin=previous['origin']
    else:
        target=folder/(sid+'.wav')
        if a.model=='milikara':
            os.environ['KARA_ALIGN_MODELS']=str(ROOT/'.models/milikara-native')
            sys.path.insert(0,str(ROOT/'.deps/comparison/milikara'))
            os.environ['PYTHONPATH']=str(ROOT/'.deps/comparison/milikara')
            from kara_align.audio.separation import separate
            native_output=separate(source,folder/sid,python=sys.executable)
            import shutil
            shutil.copyfile(native_output.vocals_path,target)
            origin='native GPU inference'
            info=sf.info(target)
            records.append({'song':sid,'source_sha256':digest(source),'path':str(target),
                            'sha256':digest(target),'frames':info.frames,'rate':info.samplerate,'origin':origin})
            continue
        wave=decode_audio(source,sample_rate=44100,channels=2).samples
        random.seed(0);np.random.seed(0);torch.manual_seed(0)
        vocals=infer.native_file(source,folder/sid) if a.model=='sug' else infer(wave)
        assert vocals.shape==wave.shape and np.isfinite(vocals).all()
        sf.write(target,vocals.T,44100,subtype='FLOAT');origin='native GPU inference' if a.model=='sug' else 'native-equivalent GPU inference'
    info=sf.info(target)
    records.append({'song':sid,'source_sha256':digest(source),'path':str(target),
                    'sha256':digest(target),'frames':info.frames,'rate':info.samplerate,'origin':origin})
    print('STEM',a.model,sid,origin,flush=True)
dump(manifest_path,
     {'model':a.model,'identity':identity,'native_equivalence':{'input':'s01 first 30 seconds',
      'max_absolute_difference':error,'tolerance':limit},'records':records})

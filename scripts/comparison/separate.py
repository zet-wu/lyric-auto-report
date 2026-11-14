"""Pinned native separators. Cached stems retain source and output hashes."""
from common import *
import argparse, time, shutil, traceback, fcntl
import numpy as np, soundfile as sf, torch

p=argparse.ArgumentParser();p.add_argument('method',choices=['demucs','bs','sug','yohane','milikara']);p.add_argument('--song');a=p.parse_args()
torch.set_num_threads(8)
assert torch.cuda.is_available(), 'GPU is required'
lock=(CACHE/(a.method+'-separation.lock')).open('w')
fcntl.flock(lock,fcntl.LOCK_EX)
product_imports()
if a.method in ("demucs","yohane"):
    from lazulite.audio.io import decode_audio
for s in songs():
    sid=s['id']
    if a.song and sid!=a.song:continue
    dst=CACHE/'stems'/a.method/(sid+'.wav');rec=OUT/'separation'/a.method/(sid+'.json')
    if dst.exists() and rec.exists():continue
    final_dst=dst;dst=dst.with_name(dst.stem+'.partial.wav')
    dst.parent.mkdir(parents=True,exist_ok=True)
    t=time.monotonic();source=ROOT/s['audio'];origin='fresh CUDA';details={}
    try:
        cached=None
        if sid!='s15' and a.method in ('demucs','bs') and (ROOT/'results/timing/reference.json').exists():
            cached=ROOT/'.cache/timing/audio'/(source.stem+'.wav') if a.method=='demucs' else ROOT/'.cache/ablation/stems/bs'/(sid+'.wav')
            old=next(x for x in read(ROOT/'results/timing/reference.json') if x['id']==sid)
            assert sha(source)==old['audio_sha256']
        if cached and cached.exists():
            shutil.copyfile(cached,dst);origin='reused frozen source-matched stem';details={'source_stem':str(cached)}
        elif a.method=='demucs':
            from lazulite.audio.separation import DemucsSeparator,DemucsConfig
            sep=DemucsSeparator(DemucsConfig());v=sep.separate(decode_audio(source,sample_rate=44100,channels=2));sep.close()
            sf.write(dst,v.samples.T,v.sample_rate,subtype='FLOAT')
        elif a.method=='bs':
            timing_imports()
            from timing.bs_lead import separate
            work=CACHE/'separation/bs'/sid;work.mkdir(parents=True,exist_ok=True)
            path,details=separate(source,work);shutil.copyfile(path,dst)
        elif a.method=='sug':
            from audio_separator.separator import Separator
            import onnxruntime as ort
            assert 'CUDAExecutionProvider' in ort.get_available_providers()
            work=CACHE/'separation/sug'/sid;work.mkdir(parents=True,exist_ok=True)
            sep=Separator(model_file_dir=str(ROOT/'.models/comparison/sug'),output_dir=str(work),output_format='WAV',use_autocast=False)
            sep.load_model(model_filename='UVR-MDX-NET-Inst_HQ_3.onnx')
            paths=sep.separate(str(source));paths=[work/f for f in paths if 'Vocals' in f]
            assert len(paths)==1,paths
            shutil.copyfile(paths[0],dst)
        elif a.method=='yohane':
            # Load the unmodified audio module without CLI/codec dependencies.
            import importlib.util
            spec=importlib.util.spec_from_file_location('yohane_audio',ROOT/'.deps/comparison/yohane/yohane/audio.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
            v=decode_audio(source,sample_rate=44100,channels=2)
            samples,rate=m.HybridDemucsSeparator()(torch.from_numpy(v.samples),v.sample_rate)
            sf.write(dst,samples.detach().cpu().numpy().T,rate,subtype='FLOAT')
        else:
            os.environ['PYTHONPATH']=str(ROOT/'.deps/comparison/milikara')
            os.environ['KARA_ALIGN_MODELS']=str(ROOT/'.models/milikara-native')
            os.environ['KARA_ALIGN_HOME']=os.environ.get('COMPARISON_SEPARATION_HOME',str(CACHE/'milikara-home'))
            sys.path.insert(0,str(ROOT/'.deps/comparison/milikara'))
            from kara_align import service as S
            work=CACHE/'separation/milikara'/sid
            h=S.open_dir(work) if (work/'project.json').exists() else S.create_dir(work,s['name'],mode='plain')
            if not h.project.audio:S.add_media(h,source,role='original')
            if not S.stems_current(h.project):details=S.run_separation(h,'melband-roformer',progress=lambda f,m='':print(sid,m,flush=True))
            # Resolve the native recorded vocal media path, never choose a residual.
            dump(OUT/'separation/milikara'/(sid+'-project.json'),h.project.model_dump(mode='json'))
            candidates=[work/x.path for x in h.project.audio if x.role=='vocals']
            assert len(candidates)==1,[str(x) for x in candidates]
            shutil.copyfile(candidates[0],dst)
        meta=sf.info(dst)
        assert abs(meta.duration-s['duration'])<.2,(sid,meta.duration,s['duration'])
        dst.replace(final_dst);dst=final_dst
        dump(rec,{'song':sid,'method':a.method,'source_sha256':sha(source),'sha256':sha(dst),'path':str(dst),'origin':origin,'seconds':time.monotonic()-t,'frames':meta.frames,'rate':meta.samplerate,'details':details})
        print('DONE',a.method,sid,round(time.monotonic()-t,2),flush=True)
    except Exception:
        dump(rec.with_name(sid+'-error.json'),{'error':traceback.format_exc()});print(traceback.format_exc(),flush=True)

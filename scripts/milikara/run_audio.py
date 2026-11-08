"""Test upstream retry's original/vocals role switch with NextFire held fixed."""
from common import *
from modules import *
from fast_ctc import install
from kara_align.align.runner import AlignInputs,run_alignment
from kara_align.models import AlignConfig,Calibration,AudioAsset,BackendInfo,RetryConfig
from transformers import Wav2Vec2ForCTC
import torch,subprocess,time,itertools
install();torch.set_num_threads(8);torch.manual_seed(0)
model=Wav2Vec2ForCTC.from_pretrained(ROOT/'.models/nextfire',local_files_only=True).to('cuda').eval()
media=read(OUT/'audio-sources.json')
runtime=read(OUT/'original-audio-runtime.json') if exists(OUT/'original-audio-runtime.json') else []
for song,ev,cache in inputs():
    sid=song['id'];path=ROOT/media[sid]['audio'];assert sha(path)==media[sid]['sha256']
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','pipe:1'])
    original=np.frombuffer(raw,dtype='<f4').copy()
    for mode in MODES:
        y,mapping,env,activity=load_audio(song,ev,cache,mode)
        # decoder/resampler may differ by a few samples; retain full original source and saved sample map.
        x=original if mapping is None else concatenate(original,mapping)
        lp_path=CACHE/f'{sid}-{mode}-original.npy'
        if not lp_path.exists():
            t=time.perf_counter();x=(x-x.mean())/np.sqrt(x.var()+1e-7);n=(len(x)-400)//320+1;lp=np.empty((n,32),np.float32);covered=np.zeros(n,int)
            for core in range(0,len(x),320000):
                lo=max(0,core-32000);hi=min(len(x),core+352000)
                with torch.inference_mode():v=model(torch.from_numpy(x[lo:hi].copy()).unsqueeze(0).to('cuda')).logits[0].float().log_softmax(-1).cpu().numpy()
                ix=np.arange(len(v))+lo//320;keep=(ix>=core//320)&(ix<min((core+320000)//320,n));lp[ix[keep]]=v[keep];covered[ix[keep]]+=1
            assert (covered==1).all();np.save(lp_path,lp)
            runtime=[r for r in runtime if (r['song'],r['audio'])!=(sid,mode)]
            runtime.append({'song':sid,'audio':mode,'seconds':time.perf_counter()-t,'frames':n,'original_samples':len(original),'vocals_axis_samples':len(y),'sha256':sha(lp_path)})
        if not any((r['song'],r['audio'])==(sid,mode) for r in runtime):
            runtime.append({'song':sid,'audio':mode,'frames':len(np.load(lp_path,mmap_mode='r')),
                'original_samples':len(original),'vocals_axis_samples':len(y),'sha256':sha(lp_path),
                'note':'Existing acoustic cache; original forward timing unavailable.'})
        for delim in [False,True]:
            voc=emission(cache,sid,mode,delim);lp=np.load(lp_path)
            if delim:lp[:,29]=np.logaddexp(lp[:,29],lp[:,0]);lp[:,0]=-1e4
            orig=Emission(lp,FrameMap(16000,320,0,0),29)
            for role,retry in [('original',False),('original',True),('vocals',True)]:
                doc=document(song);cfg=AlignConfig(audio_role=role,retry=RetryConfig(enabled=retry))
                assets={r:AudioAsset(id=r,role=r,sha256=media[sid]['sha256'] if r=='original' else sha(cache/f'{sid}-vocals.npy'),duration_ms=round(len(y)/16),sample_rate=16000,channels=1,num_samples=len(y)) for r in ['original','vocals']}
                emissions={'original':orig,'vocals':voc}
                inp=AlignInputs(lyrics=doc,mode='plain',calibration=Calibration(confirmed=True),config=cfg,backend_info=BackendInfo(name='mms-ja',model_id='NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn',profile=PROFILE.name,sample_rate=16000),tokenize=tokenize,profile=PROFILE,emission_for=lambda r:emissions[r],available_roles=['original','vocals'],audio_assets=assets,audio_duration_ms=round(len(y)/16),energy_for=lambda _:env)
                t=time.perf_counter();res=run_alignment(inp);name=f'audio-{role}-r{int(retry)}-d{int(delim)}'
                dump(OUT/'predictions'/f'{sid}--{mode}--{name}.json',{'song':sid,'experiment':f'{mode}/{name}','kind':'confirmed-targets','predictions':predictions(doc,res.units,mapping),'stats':res.stats,'seconds':time.perf_counter()-t,'note':'same frozen vocal energy and target; original stereo-mean FFmpeg 16k; same concatenation sample map and legacy ±2s forward'})
        print(sid,mode,'audio role complete',flush=True)
dump(OUT/'original-audio-runtime.json',runtime)

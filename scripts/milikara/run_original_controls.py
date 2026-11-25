"""M7 native retry controls with both vocal and original-mixture emissions cached."""
from common import *
from modules import *
from kara_align.align.runner import AlignInputs, run_alignment
from kara_align.models import AlignConfig, Calibration, AudioAsset, BackendInfo, RetryConfig
from shared import portable
import time,hashlib
product_imports()
from lazulite.audio.io import decode_audio
from concat import concatenate

media = read(OUT / 'audio-sources.json')
for song,evidence,cache in inputs():
    sid=song['id']
    y,mapping,env,activity=load_audio(song,evidence,cache,'concat_core')
    vocals=emission(cache,sid,'concat_core',False)
    original=Emission(np.load(cache/f'{sid}-concat_core-original.npy'),FrameMap(16000,320,0,0),29)
    emissions={'original':original,'vocals':vocals}
    original_samples=decode_audio(ROOT/media[sid]['audio'],sample_rate=16000,channels=1).samples[0]
    signals={'vocals':concatenate(y,mapping),'original':concatenate(original_samples,mapping)}
    count=mapping[-1]['concat_end']
    # These virtual input assets live on the same native concatenated axis as the cached emissions.
    assets={role:AudioAsset(id=role,role=role,sha256=hashlib.sha256(signal.astype('<f4').tobytes()).hexdigest(),duration_ms=round(count/16),sample_rate=16000,channels=1,num_samples=count) for role,signal in signals.items()}
    for role in ('vocals','original'):
        name='retry-'+role;target=OUT/'predictions'/f'{sid}--concat_core--{name}.json.gz'
        started=time.perf_counter();record={'song':sid,'experiment':'concat_core/'+name,'kind':'confirmed-targets','status':'failed','retry':True,'initial_audio_role':role,'planning':'Native MiliKara runner; separate from the eight global-decoder soft-cost conditions.'}
        try:
            doc=document(song)
            config=AlignConfig(audio_role=role,retry=RetryConfig(enabled=True),decode=decode_config(dict.fromkeys(FACTORS,False)))
            inp=AlignInputs(lyrics=doc,mode='plain',calibration=Calibration(confirmed=True),config=config,
                            backend_info=BackendInfo(name='mms-ja',model_id='NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn',profile=PROFILE.name,sample_rate=16000),
                            tokenize=tokenize,profile=PROFILE,emission_for=lambda selected:emissions[selected],available_roles=list(emissions),audio_assets=assets,
                            audio_duration_ms=round(count/16),energy_for=lambda _:env)
            result=run_alignment(inp)
            record.update(status='ok',predictions=predictions(doc,result.units,mapping),stats=result.stats)
        except Exception as exc:
            record['error']={'type':type(exc).__name__,'message':portable(exc)[:800]}
        record['seconds']=time.perf_counter()-started
        dump(target,record);print(sid,name,record['status'],flush=True)

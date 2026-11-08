"""Conditional LRC-hint robustness; source AST isolates pure upstream fitting from project I/O."""
from common import *
from modules import *
from fast_ctc import install
from kara_align.align.runner import AlignInputs,run_alignment,AlignmentInputError
from kara_align.models import AlignConfig,Calibration,AudioAsset,BackendInfo
import ast,statistics,time
install();source=UPSTREAM/'kara_align/auto_calibrate.py'
nodes=[n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ['fit_offset','_drift_ms']]
namespace={'statistics':statistics,'MIN_LINES':4,'TIGHT_MS':300,'MIN_TIGHT':.6,'MAX_DRIFT_MS':400}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),namespace)
fit=namespace['fit_offset']
assert fit([(i*10000,500) for i in range(8)])['shift_ms']==500
assert not fit([(i*10000,i*500) for i in range(8)])['confident']
def compress(t,mapping):
    if mapping is None:return t
    p=t*16
    for m in mapping:
        if p<m['source_start']:return round(m['concat_start']/16)
        if p<=m['source_end']:return round((m['concat_start']+p-m['source_start'])/16)
    return round(mapping[-1]['concat_end']/16)
hints=read(OUT/'conditional-line-hints.json')['songs']
for song,ev,cache in inputs():
    sid=song['id']
    for mode in MODES:
        y,mapping,env,activity=load_audio(song,ev,cache,mode)
        raw=read(OUT/'predictions'/f'{sid}--{mode}--runner-plain-d1-r1.json')
        predicted_starts=[round(min(p['start'] for p in row if p)*1000) if any(row) else None for row in raw['predictions']]
        for label,ts in hints[sid].items():
            est=fit([(t,p-t) for p,t in zip(predicted_starts,ts) if p is not None])
            shift=est['shift_ms'] if est['confident'] else 0
            doc=document(song)
            for l,t in zip(doc.lines,ts):l.imported_start_ms=compress(max(0,t+shift),mapping)
            em=emission(cache,sid,mode,False);cfg=AlignConfig(audio_role='vocals')
            asset=AudioAsset(id='frozen-vocals',role='vocals',sha256=sha(cache/f'{sid}-vocals.npy'),duration_ms=round(len(y)/16),sample_rate=16000,channels=1,num_samples=len(y))
            inp=AlignInputs(lyrics=doc,mode='lrc',calibration=Calibration(confirmed=True),config=cfg,backend_info=BackendInfo(name='mms-ja',model_id='NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn',profile=PROFILE.name,sample_rate=16000),tokenize=tokenize,profile=PROFILE,emission_for=lambda _:em,available_roles=['vocals'],audio_assets={'vocals':asset},audio_duration_ms=round(len(y)/16),energy_for=lambda _:env)
            t=time.perf_counter()
            name=f'calibrated-{label}'
            try:res=run_alignment(inp)
            except AlignmentInputError as error:
                dump(OUT/'predictions'/f'{sid}--{mode}--{name}.json',{'song':sid,'experiment':f'{mode}/{name}','kind':'confirmed-targets','conditional':True,'calibration':est,'applied_shift_ms':shift,'predictions':[[None for _ in l.units()] for l in doc.lines],'error':str(error)})
                continue
            dump(OUT/'predictions'/f'{sid}--{mode}--{name}.json',{'song':sid,'experiment':f'{mode}/{name}','kind':'confirmed-targets','conditional':True,'calibration':est,'applied_shift_ms':shift,'calibration_unresolved':not est['confident'],'seconds':time.perf_counter()-t,'predictions':predictions(doc,res.units,mapping),'stats':res.stats})
        print(sid,mode,'calibration complete',flush=True)
dump(OUT/'calibration-source.json',{'source':str(source.relative_to(ROOT)),'sha256':sha(source),'functions':['fit_offset','_drift_ms'],'constants':{k:v for k,v in namespace.items() if k.isupper()},'synthetic_constant_shift_and_drift_checks':True})

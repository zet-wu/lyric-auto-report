from common import *
from modules import *
from fast_ctc import install
from kara_align.align.runner import AlignInputs,run_alignment,AlignmentInputError
from kara_align.models import AlignConfig,Calibration,AudioAsset,BackendInfo,RetryConfig
from kara_align.align.planning import TaskAnchor
import itertools,time
install()
hints=read(OUT/'conditional-line-hints.json')['songs']
def compress(t,mapping):
    if mapping is None:return t
    p=t*16
    for m in mapping:
        if p<m['source_start']:return round(m['concat_start']/16)
        if p<=m['source_end']:return round((m['concat_start']+p-m['source_start'])/16)
    return round(mapping[-1]['concat_end']/16)
for song,ev,cache in inputs():
    sid=song['id']
    for mode in MODES:
        y,mapping,env,activity=load_audio(song,ev,cache,mode);doc=document(song)
        flag0=dict(zip(FACTORS,[False,False,False,False,True]))
        base_units,base_out=global_decode(doc,emission(cache,sid,mode,False),activity,flag0)
        starts=[base_out.line_ranges[l.id][0] for l in doc.lines]
        variants=[]
        for delim,retry in itertools.product([False,True],repeat=2):variants.append((f'plain-d{int(delim)}-r{int(retry)}',None,1,4.,retry,delim))
        for context,lam,retry in itertools.product([0,1],[0.,4.],[False,True]):variants.append((f'self-c{context}-l{int(lam)}-r{int(retry)}',starts,context,lam,retry,False))
        variants.append(('self-c1-l4-r1-d1',starts,1,4.,True,True))
        for label,ts in hints[sid].items():
            ts=[compress(t,mapping) for t in ts]
            variants.append((label,ts,1,4.,True,False))
        for name,ts,context,lam,retry,delim in variants:
            dest=OUT/'predictions'/f'{sid}--{mode}--runner-{name}.json'
            if dest.exists():continue
            doc=document(song)
            if ts is not None:
                for l,t in zip(doc.lines,ts):l.imported_start_ms=t
            em=emission(cache,sid,mode,delim)
            cfg=AlignConfig(audio_role='vocals',retry=RetryConfig(enabled=retry));cfg.decode.joint_context_lines=context;cfg.decode.soft_lambda=lam
            asset=AudioAsset(id='frozen-vocals',role='vocals',sha256=sha(cache/f'{sid}-vocals.npy'),duration_ms=round(len(y)/16),sample_rate=16000,channels=1,num_samples=len(y))
            inp=AlignInputs(lyrics=doc,mode='plain' if ts is None else 'lrc',calibration=Calibration(confirmed=True),config=cfg,backend_info=BackendInfo(name='mms-ja',model_id='NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn',profile=PROFILE.name,sample_rate=16000),tokenize=tokenize,profile=PROFILE,emission_for=lambda _:em,available_roles=['vocals'],audio_assets={'vocals':asset},audio_duration_ms=round(len(y)/16),energy_for=lambda _:env)
            t=time.perf_counter()
            try:result=run_alignment(inp)
            except AlignmentInputError as error:
                dump(dest,{'song':sid,'experiment':f'{mode}/runner-{name}','kind':'confirmed-targets','conditional':name.startswith('oracle'),'seconds':time.perf_counter()-t,'predictions':[[None for _ in l.units()] for l in doc.lines],'error':str(error)})
                continue
            dump(dest,{'song':sid,'experiment':f'{mode}/runner-{name}','kind':'confirmed-targets','conditional':name.startswith('oracle'),'seconds':time.perf_counter()-t,'predictions':predictions(doc,result.units,mapping),'stats':result.stats,'issues':[i.model_dump(mode='json') for i in result.issues],'line_status':[l.model_dump(mode='json') for l in result.lines]})
        # Isolate soft anchor itself, without planning windows or retry.
        doc=document(song);prep=prepare(doc,PROFILE,tokenize);em=emission(cache,sid,mode,False)
        cfg=DecodeConfig();task=Task('soft-self','main',prep.order,prep.order,0,em.num_frames,[TaskAnchor(l.id,t,'soft') for l,t in zip(doc.lines,starts)],free_tail=True)
        out=decode_task(task,em,prep,cfg,'vocals',activity=activity)
        us=[u for lid in prep.order for u in unit_timings_for_line(prep,out,lid)]
        dump(OUT/'predictions'/f'{sid}--{mode}--self-soft-only.json',{'song':sid,'experiment':f'{mode}/self-soft-only','kind':'confirmed-targets','predictions':predictions(doc,us,mapping)})
        print(sid,mode,'runner + anchors complete',flush=True)

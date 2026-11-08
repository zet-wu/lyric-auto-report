"""Independent module runner. All target timestamps are isolated in window()."""
from ablation_common import *
product_imports(); timing_imports()
import argparse, math, time, traceback, gc
from dataclasses import asdict
import numpy as np
import soundfile as sf
import torch
from lazulite.audio.io import decode_audio, resample_audio
from lazulite.audio.preparation import prepare_existing_vocals
from lazulite.audio.concat import concatenate_cores, ConcatMap, Piece
from lazulite.models.audio import AudioBuffer, VocalSegment
from lazulite.models.japanese import JapaneseAlignmentRequest, JapaneseLine, JapaneseUnit

parser=argparse.ArgumentParser()
parser.add_argument('stage',choices=['audio','nextfire','mms_fa','mms','tifa'])
parser.add_argument('--separators',nargs='+',default=['demucs','bs','kim'])
parser.add_argument('--songs',nargs='+')
parser.add_argument('--strategies',nargs='+',default=['concat','padded','full','auto_nf','auto_mms','human','fixed_cores'])
args=parser.parse_args()
# Serialize duplicate invocations of the same matrix partition.
import fcntl
lockdir=CACHE/'locks';lockdir.mkdir(exist_ok=True)
lock=(lockdir/(args.stage+'-'+'-'.join(sorted(args.separators))+'.lock')).open('w')
fcntl.flock(lock,fcntl.LOCK_EX)
torch.set_num_threads(8)
targets=read(OUT/'targets.json')
if args.songs:targets=[s for s in targets if s['id'] in args.songs]

def context(song,sep):
    return read(OUT/'audio'/sep/(song['id']+'.json'))

def request(lines):
    return JapaneseAlignmentRequest(tuple(JapaneseLine(str(l['index']),l['text'],tuple(
        JapaneseUnit(g['key'],(0,len(l['text'])),g['reading'], 'ja' if g['lang']=='ja' else 'en' if g['lang']=='en' else 'yue','ruby')
        for g in l['groups'])) for l in lines))

def window(song,sep,line,strategy,duration):
    if strategy=='human':
        a,b=line['human_window']
        return max(0,math.floor(a/.02)*.02),min(duration,math.ceil(b/.02)*.02)
    source=(result_path(sep,'nextfire','concat',song['id']) if strategy=='auto_nf' else
            OUT/'pause-windows'/sep/(song['id']+'.json') if strategy=='auto_mms_pause' else
            OUT/'windows'/sep/(song['id']+'.json'))
    if not present(source):return None
    record=read(source)
    if strategy=='auto_nf':
        pred={r['key']:r['prediction'] for r in record.get('units',[])}
        a=pred.get(line['groups'][0]['key']);b=pred.get(line['groups'][-1]['key'])
        if a is None or b is None:return None
        a,b=a[0],b[1]
    else:
        value=record.get('windows',{}).get(str(line['index']))
        if value is None:return None
        a,b=value
        if strategy=='auto_mms_pause':return (a,b) if .1<=b-a<=60 else None
    a,b=max(0,a-.3),min(duration,b+.3)
    return (a,b) if .1<=b-a<=60 else None

def cases(song,sep,strategy):
    info=context(song,sep)
    if strategy in ('concat','padded','fixed_cores','full'):
        file=info['files'][strategy]
        wave,rate=sf.read(file,dtype='float32')
        mapping=None
        if strategy!='full':
            mapping=ConcatMap(rate,len(wave),tuple(Piece(**p) for p in info['mapping'][strategy]))
        yield {'id':'whole','lines':song['lines'],'wave':wave,'rate':rate,'offset':0,'mapping':mapping,'window':[0,len(wave)/rate]}
    else:
        wave,rate=sf.read(info['files']['full'],dtype='float32')
        for line in song['lines']:
            bounds=window(song,sep,line,strategy,len(wave)/rate)
            if bounds is None:
                yield {'id':str(line['index']),'lines':[line],'error':'automatic_window_unavailable'}
                continue
            a,b=math.floor(bounds[0]*rate),min(len(wave),math.ceil(bounds[1]*rate))
            yield {'id':str(line['index']),'lines':[line],'wave':wave[a:b],'rate':rate,'offset':a/rate,'mapping':None,'window':[a/rate,b/rate]}

def remap(span,case):
    if span is None or not np.isfinite(span).all() or span[1]<=span[0]:return None,None,False
    a,b=map(float,span)
    duration=len(case['wave'])/case['rate']
    if a < -1e-5 or b>duration+.011:return None,None,False
    a,b=max(0,a),min(duration,b)
    if b<=a:return None,None,False
    if case['mapping'] is None:
        v=[a+case['offset'],b+case['offset']]
        return v,v,False
    pieces=case['mapping'].fragments(a,b)
    if not pieces:return None,None,False
    raw=[pieces[0].start,pieces[-1].end]
    crossing=len(pieces)>1
    return None if crossing else raw,raw,crossing

def audio_stage(song,sep):
    sid=song['id'];target=OUT/'audio'/sep/(sid+'.json')
    if target.exists():return
    original=decode_audio(ROOT/song['audio'],sample_rate=44100,channels=2)
    v,r=sf.read(stem_path(song,sep),dtype='float32',always_2d=True)
    vocals=AudioBuffer(v.T.copy(),r,original.source_id)
    prepared=prepare_existing_vocals(vocals,reference=original,original_duration=original.duration)
    work=CACHE/'audio'/sep/sid;work.mkdir(parents=True,exist_ok=True)
    full=resample_audio(vocals,sample_rate=48000,channels=1)
    files={'full':str(work/'full.wav')};maps={}
    sf.write(files['full'],full.samples[0],48000,subtype='FLOAT')
    frozen=(prepared.segments if sep=='demucs' else tuple(VocalSegment(**s) for s in context(song,'demucs')['segments']))
    for name,segs in [('concat',prepared.segments),('padded',tuple(__import__('dataclasses').replace(s,core_start=s.start,core_end=s.end) for s in prepared.segments)),('fixed_cores',frozen)]:
        if name=='fixed_cores' and sep=='demucs':
            files[name]=files['concat'];maps[name]=maps['concat'];continue
        concat=concatenate_cores(vocals,segs,sample_rate=48000)
        files[name]=str(work/(name+'.wav'));maps[name]=[asdict(p) for p in concat.mapping.pieces]
        sf.write(files[name],concat.audio.samples[0],48000,subtype='FLOAT')
    dump(target,{'song':sid,'separator':sep,'files':files,'mapping':maps,'segments':[asdict(s) for s in prepared.segments],
                 'analysis':asdict(prepared.analysis),'duration':original.duration})
    print('AUDIO',sep,sid,round(sf.info(files['concat']).duration,2),flush=True)

backend=None
if args.stage in ('nextfire','mms_fa'):
    from lazulite.alignment.japanese.backend import NextFireBackend,NextFireConfig
    from lazulite.alignment.japanese.run import _profile,_intervals
    from lazulite.alignment.japanese.ctc import decode
    from lazulite.alignment.japanese.backend import open_backend
    backend=open_backend(ROOT/('.models/nextfire' if args.stage=='nextfire' else '.models/mms-fa'),'cuda')
elif args.stage=='mms':
    from timing.ctc import CtcAligner
    from timing.schema import Line,Unit
    from timing.text_localization import align_transcript
    backend=CtcAligner(log=lambda s:None);backend.load()
elif args.stage=='tifa':
    import sys
    model=UPSTREAM/'models/tifa'
    sys.path[:0]=[str(model/'deps'),str(model/'runtime')]
    from inference.api import load_inference_model
    from lib.config.schema import ConfigurationScope
    backend,vocabulary,config=load_inference_model(model/'model.pt',scope=ConfigurationScope.FA)
    backend=backend.cuda().eval()
    vocab=read(model/'vocabulary.json')['symbols']

for sep in args.separators:
    for song in targets:
        sid=song['id']
        if args.stage=='audio':
            audio_stage(song,sep);continue
        if args.stage=='mms':
            target=OUT/'windows'/sep/(sid+'.json')
            if target.exists():continue
            record={'song':sid,'separator':sep,'windows':{}};started=time.monotonic()
            try:
                if sid=='s11':raise ValueError('Yue unsupported in this shared Japanese/English coarse locator; no Mandarin substitution')
                wave,rate=sf.read(context(song,sep)['files']['full'],dtype='float32')
                probs,meta=backend.emissions(wave,sample_rate=rate)
                lines=[];prepared=[]
                for line in song['lines']:
                    texts=[g['text'] for g in line['groups']]
                    labels=[]
                    # Timing's MMS phone-to-Latin convention, with the frozen
                    # readings instead of a second automatic pronunciation pass.
                    flat=[ph.split('/',1)[1] for g in line['groups'] for ph in sum(g['phone_groups'],[])]
                    cursor=0
                    for g in line['groups']:
                        phones=[ph.split('/',1)[1] for ph in sum(g['phone_groups'],[])]
                        label=''
                        for phone in phones:
                            if phone=='cl':
                                following=flat[cursor+1] if cursor+1<len(flat) else 't'
                                label+='t' if following in {'ch','ts'} else following[0].lower()
                            else:label+='n' if phone=='N' else phone.lower()
                            cursor+=1
                        if g['lang']=='en':label=''.join(c for c in g['reading'].lower() if 'a'<=c<='z')
                        labels.append(label)
                    lines.append(Line(text=''.join(texts),language='ja'))
                    prepared.append(([Unit(text=t,spoken=t) for t in texts],labels))
                located,rows=align_transcript(lines,probs,backend.vocab,backend.model.config.pad_token_id,meta['frame_ms']/1000,len(wave)/rate,prepared=prepared)
                record.update(windows={str(l['index']):[r.start,r.end] for l,r in zip(song['lines'],located)},details=rows)
            except Exception:record['error']=traceback.format_exc()
            record['seconds']=time.monotonic()-started;dump(target,record)
            print('MMS',sep,sid,len(record['windows']),record.get('error','')[-180:],flush=True)
            continue
        for strategy in args.strategies:
            if strategy=='fixed_cores' and sep=='demucs':continue
            dependency=(result_path(sep,'nextfire','concat',sid) if strategy=='auto_nf' else
                        OUT/'pause-windows'/sep/(sid+'.json') if strategy=='auto_mms_pause' else
                        OUT/'windows'/sep/(sid+'.json') if strategy=='auto_mms' else None)
            if dependency is not None and not present(dependency):
                print('DEFER',sep,args.stage,strategy,sid,flush=True);continue
            target=result_path(sep,args.stage,strategy,sid)
            if present(target):continue
            record={'song':sid,'separator':sep,'backend':args.stage,'strategy':strategy,'units':[],'cases':[]}
            begin=time.monotonic()
            for case in cases(song,sep,strategy):
                groups=[g for l in case['lines'] for g in l['groups']]
                detail={k:case[k] for k in ('id','window','error') if k in case}
                start=time.monotonic();pred={};native=None
                try:
                    if case.get('error'):raise ValueError(case['error'])
                    torch.cuda.reset_peak_memory_stats()
                    if args.stage in ('nextfire','mms_fa'):
                        req=request(case['lines'])
                        texts,tokens,ranges,problems=_profile(req,backend.vocab,backend.blank,backend.special_tokens)
                        audio=resample_audio(AudioBuffer(case['wave'][None,:],case['rate'],sid),sample_rate=16000,channels=1)
                        probs=backend.emissions(audio)
                        spans,score=decode(probs,tokens,blank=backend.blank)
                        intervals,sources=_intervals(req,spans,ranges,backend.frames)
                        pred=intervals;detail['profile_issues']=problems
                    else:
                        ids=[];owners=[];groupids=[];gid=0
                        for owner,g in enumerate(groups):
                            for phs in g['phone_groups']:
                                gid+=1
                                for ph in phs:ids.append(vocab[ph]);owners.append(owner);groupids.append(gid)
                        with torch.inference_mode():
                            wave=torch.from_numpy(case['wave']).cuda()[None,:]
                            duration=torch.tensor([wave.shape[-1]/case['rate']],device='cuda')
                            spec=backend.spectrogram(wave,duration)
                            tokens=torch.tensor([ids],dtype=torch.long,device='cuda')
                            gids=torch.tensor([groupids],dtype=torch.long,device='cuda')
                            aligned=backend.align(spec,tokens=tokens,groups=gids,unit='second',skip_penalty=.5)
                            spans=aligned.spans[0].cpu().tolist()
                            detail.update(agreement=float(aligned.agreement[0]),frames=int(spec.mask.sum()),tokens=len(ids))
                            native={'spans':spans,'owners':owners,'groups':groupids,'tokens':ids}
                            for owner,g in enumerate(groups):
                                indices=[i for i,v in enumerate(owners) if v==owner]
                                if indices and all(spans[i][1]>spans[i][0] for i in indices):
                                    pred[g['key']]=[spans[indices[0]][0],spans[indices[-1]][1]]
                            del aligned,spec,wave,tokens,gids
                    detail['peak_gib']=torch.cuda.max_memory_allocated()/2**30
                except Exception:
                    detail['error']=traceback.format_exc();print('CASE ERROR',sep,sid,args.stage,strategy,case['id'],detail['error'][-200:],flush=True)
                for g in groups:
                    p,raw,cross=remap(pred.get(g['key']),case) if pred.get(g['key']) is not None else (None,None,False)
                    record['units'].append({'key':g['key'],'prediction':p,'raw':raw,'crosses_removed_gap':cross})
                detail['seconds']=time.monotonic()-start
                if native is not None:detail['native']=native
                record['cases'].append(detail)
                gc.collect();torch.cuda.empty_cache()
            record['seconds']=time.monotonic()-begin;dump(target,record)
            print('DONE',sep,args.stage,strategy,sid,len(record['units']),sum(u['prediction'] is not None for u in record['units']),round(record['seconds'],2),flush=True)
if backend is not None and hasattr(backend,'close'):backend.close()
if backend is not None and hasattr(backend,'release'):backend.release()

"""Exercise the pinned upstream service with plain text or untimed manual readings."""
from common import *
import argparse, copy, subprocess, time, traceback, unicodedata

DEST=ROOT/'results/milikara-native'
WORK=ROOT/'.cache/milikara-native'
os.environ['KARA_ALIGN_MODELS']=str(ROOT/'.models/milikara-native')
parser=argparse.ArgumentParser()
parser.add_argument('--song')
parser.add_argument('--condition',choices=['auto','manual'])
args=parser.parse_args()
if not args.song:
    selected=os.environ.get('BENCHMARK_SONGS','').split(',')
    for path in sorted((DEST/'inputs/text').glob('*.json')):
        if selected!=[''] and path.stem not in selected:continue
        for condition in ('auto','manual'):
            subprocess.run([sys.executable,__file__,'--song',path.stem,'--condition',condition],check=True)
    raise SystemExit(0)

sid=args.song;condition=args.condition
output=DEST/'runs'/f'{sid}-{condition}.json'
if exists(output) and read(output).get('export'):
    print('EXISTS',sid,condition,flush=True);raise SystemExit(0)
os.environ['KARA_ALIGN_HOME']=str(WORK/'home'/f'{sid}-{condition}')
from kara_align import service as S
from kara_align.models import Segment,Unit
def audit_export(h,record):
    exported=S.export(h,'alignment')
    value=json.loads(exported.content)
    assert portable(value['units'])==record['result']['units']
    assert portable(value['lines'])==record['result']['lines']
    record['export']={'format':'alignment','filename':exported.filename,
        'warnings':exported.warnings,'units_and_lines_equal':True}
if exists(output):
    record=read(output)
    if record['status']=='ok':
        audit_export(S.open_dir(WORK/'projects'/f'{sid}-{condition}'),record)
        dump(output,record)
    print('EXISTS',sid,condition,flush=True);raise SystemExit(0)
protocol=read(ROOT/'configs/milikara-native.json')
source=read(DEST/'inputs'/('manual' if condition=='manual' else 'text')/f'{sid}.json')
audio=ROOT/source['audio'];audiohash=sha(audio)
basepath=WORK/'audio'/audiohash
sepfile=DEST/'separation'/f'{audiohash}.json'
record={'song':sid,'condition':condition,'audio_sha256':audiohash,'status':'error','seconds':{}}
start=time.perf_counter();phase='import';last_progress=[None,0.0]
def progress(frac,message=''):
    now=time.perf_counter()
    if message==last_progress[0] and now-last_progress[1]<10:return
    last_progress[:]=[message,now]
    print(sid,condition,round(frac,3),message,flush=True)
try:
    if (basepath/'project.json').exists():base=S.open_dir(basepath)
    else:
        base=S.create_dir(basepath,source['name'],mode='plain')
        S.add_media(base,audio,role='original')
    if not S.stems_current(base.project):
        phase='separation';t=time.perf_counter()
        modelroot=ROOT/'.models/milikara-native/separation'
        download_needed=any(not (modelroot/name).exists() for name in ('download_checks.json',
            'model_mel_band_roformer_ep_3005_sdr_11.4360.ckpt','model_mel_band_roformer_ep_3005_sdr_11.4360.yaml'))
        separation=S.run_separation(base,protocol['separation'],progress=progress)
        dump(sepfile,{'audio_sha256':audiohash,'seconds':time.perf_counter()-t,'result':separation,
            'includes_model_download':download_needed})
    record['separation_record']=str(sepfile.relative_to(ROOT))
    projectpath=WORK/'projects'/f'{sid}-{condition}'
    if (projectpath/'project.json').exists():h=S.open_dir(projectpath)
    else:
        import shutil
        shutil.copytree(basepath,projectpath)
        h=S.open_dir(projectpath)
    phase='readings';t=time.perf_counter()
    preview=S.parse_lyrics(h,'\n'.join(l['text'] for l in source['lines']),mode='plain')
    if preview.get('error'):raise RuntimeError(preview['error'])
    record['reading_messages']=S.apply_lyrics(h,preview['preview_id'],prepare=condition=='auto')
    assert len(h.project.lyrics.lines)==len(source['lines'])
    for line,original in zip(h.project.lyrics.lines,source['lines']):
        assert line.text==original['text']
        line.id=original['id']
        assert line.imported_start_ms is None and line.imported_end_ms is None and line.anchor is None
        if condition=='manual':
            segments=[]
            for word in original['words']:
                units=[Unit(id=u['id'],reading=u['reading']) for u in word['units']]
                reading=''.join(u.reading for u in units)
                lang='en' if reading.isascii() and any(c.isalpha() for c in reading) else 'ja'
                segments.append(Segment(id=word['id'],surface=word['text'],reading=reading,lang=lang,
                    units=units,reading_source='manual',confirmed=True))
            line.segments=segments
    h.save()
    record['seconds']['readings']=time.perf_counter()-t
    record['lyrics']=h.project.lyrics.model_dump(mode='json')
    S.update_settings(h,config={**protocol['config_overrides'],'model_id':str(ROOT/protocol['model_directory'])})
    record['config']={**h.project.config.model_dump(mode='json'),'audio_role':'vocals'}
    phase='alignment';t=time.perf_counter()
    result=S.run_align(h,audio_role='vocals',progress=progress)
    record['seconds']['alignment']=time.perf_counter()-t
    record['result']=result.model_dump(mode='json')
    phase='export';audit_export(h,record)
    record['status']='ok'
except Exception as exc:
    record['error']={'phase':phase,'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
    print('FAILED',sid,condition,phase,repr(exc),flush=True)
finally:
    record['seconds']['process']=time.perf_counter()-start
    dump(output,record)
    print('DONE',sid,condition,record['status'],record['seconds'],flush=True)

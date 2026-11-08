from common import *
timing_imports()
import argparse, time, traceback, torch
from timing.pipeline import run

parser=argparse.ArgumentParser()
parser.add_argument('--songs',nargs='*')
parser.add_argument('--modes',nargs='+',default=['untimed','trusted'])
args=parser.parse_args()
torch.set_num_threads(8)
assert torch.cuda.is_available()
for song in read(OUT/'reference.json'):
    sid=song['id']
    if args.songs and sid not in args.songs: continue
    shared=CACHE/'audio'/f'{Path(song["audio"]).stem}.wav'
    if not shared.exists():
        print('WAITING FOR STEM',sid,flush=True); continue
    # Chinese dialect surface text is deliberately an out-of-scope stress test,
    # not a claim of Mandarin or Japanese recognition.
    language='zh' if song['name'].startswith('骹车') else 'mixed'
    for mode in args.modes:
        target=OUT/'timing'/f'{sid}-{mode}.json'
        if exists(target): continue
        folder=CACHE/'timing'/f'{sid}-{mode}'; folder.mkdir(parents=True,exist_ok=True)
        input_mode='untimed' if mode=='lead_untimed' else mode
        lyrics=(CACHE/'inputs'/f'{sid}-{input_mode}.json').read_text()
        started=time.monotonic()
        with (folder/'evaluation.log').open('w') as log:
            def say(message):
                print(message,file=log,flush=True)
                print(sid,mode,message,flush=True)
            try:
                source=ROOT/song['audio'] if mode=='lead_untimed' else shared
                run(source,lyrics,folder,language=language,audio_mode='lead' if mode=='lead_untimed' else 'source',aligner='tifa',
                    trust_line_timestamps=mode=='trusted',log=say)
                report=read(folder/'alignment.json')
                dump(target,{'song':sid,'mode':mode,'seconds':time.monotonic()-started,'report':report})
            except Exception:
                error=traceback.format_exc(); say(error)
                dump(OUT/'timing'/f'{sid}-{mode}-error.json',{'song':sid,'mode':mode,'seconds':time.monotonic()-started,'error':error})

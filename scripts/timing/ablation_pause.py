"""Additional window ablation, motivated by the recorded MMS tail truncation.

Unmodified Timing quiet_crop_end; horizon from NEXT predicted onset, no gold.
"""
from ablation_common import *
timing_imports()
import soundfile as sf
from timing.tifa import quiet_crop_end
for sep in ('demucs','bs','kim'):
    for song in read(OUT/'targets.json'):
        sid=song['id'];target=OUT/'pause-windows'/sep/(sid+'.json')
        info=read(OUT/'windows'/sep/(sid+'.json'))
        record={'song':sid,'separator':sep,'windows':{},'details':{}}
        if info.get('windows'):
            wave,rate=sf.read(read(OUT/'audio'/sep/(sid+'.json'))['files']['full'],dtype='float32')
            for i,line in enumerate(song['lines']):
                a,b=info['windows'][str(line['index'])]
                next_start=info['windows'][str(song['lines'][i+1]['index'])][0] if i+1<len(song['lines']) else len(wave)/rate
                left=max(0,a-.3)
                limit=min(len(wave)/rate,left+60,max(b+.35,next_start+.35))
                right,gate=quiet_crop_end(wave,rate,b,limit,a)
                if .1<=right-left<=60:record['windows'][str(line['index'])]=[left,right]
                record['details'][str(line['index'])]={'coarse':[a,b],'limit':limit,'gate':gate}
        else:record['upstream_error']=info.get('error')
        dump(target,record)
dump(OUT/'pause-protocol.json',{'reason':'Post-matrix diagnosis: MMS lexical ends often precede sustained vowel offsets; test existing pause finder rather than only fixed +300ms.',
 'separators':['demucs','bs','kim'],'backends':['nextfire','tifa','mms_fa'],'strategy':'auto_mms_pause',
 'start':'max(0, MMS start - 0.3)',
 'end':'Unmodified Timing quiet_crop_end(coarse_start, coarse_end, limit). limit=min(duration, left+60, max(coarse_end+0.35, next predicted line onset+0.35)); final line next onset=duration.',
 'reference_use':'None during window generation. Same frozen targets and scoring as primary matrix; original failed MMS songs remain failures.',
 'scope':'Separate pause-window conditions. Not the full Timing neighbour-context pipeline; no threshold tuning.'})
print('pause windows prepared')

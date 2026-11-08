from common import *
from modules import *
from fast_ctc import install
from kara_align.reading.profiles import JaHepburnProfile,is_hold
install();kana={s['id']:s for s in read(OUT/'phonetic-targets.json')};profile=JaHepburnProfile();audit=[]
for song,ev,cache in inputs():
    sid=song['id'];doc=document(song)
    for mode in MODES:
        y,mapping,env,activity=load_audio(song,ev,cache,mode)
        for variant in ['wo_to_o','sokuon','holds','profile','profile_no_hold_fill']:
            for code in ['00000','01111']:
                prep=prepare(doc,PROFILE,tokenize);changes=[]
                for li,l in enumerate(kana[sid]['lines']):
                    readings=[u['reading'] for u in l['units']];langs=['ja' if u['language']=='japanese' else 'en' for u in l['units']]
                    native=profile.unit_texts(readings,langs,[[] for _ in readings])
                    for j,(u,native_text) in enumerate(zip(l['units'],native)):
                        uid=f'u{li}_{j}';info=prep.units[uid];text=u['text']
                        if variant=='wo_to_o' and text=='wo':text='o'
                        if variant=='sokuon' and u['reading'] in ['っ','ッ']:text=native_text
                        if variant=='holds' and is_hold(u['reading']):text='';info.reading=u['reading']
                        if variant in ['profile','profile_no_hold_fill']:
                            text=native_text
                            if variant=='profile':info.reading=u['reading']
                        if text!=u['text']:changes.append({'line':l['index'],'unit':j+1,'reading':u['reading'],'before':u['text'],'after':text})
                        tok=tokenize([uid],[text])[0];info.text=text;info.token_ids=tok.token_ids;info.unknown=tok.unknown
                flags=dict(zip(FACTORS,[c=='1' for c in code]));em=emission(cache,sid,mode,False)
                task=Task('text','main',prep.order,prep.order,0,em.num_frames,free_tail=flags['free_tail'])
                out=decode_task(task,em,prep,decode_config(flags),'vocals',activity=activity)
                us=[u for lid in prep.order for u in unit_timings_for_line(prep,out,lid)]
                name=f'text-{variant}-f{code}'
                dump(OUT/'predictions'/f'{sid}--{mode}--{name}.json',{'song':sid,'experiment':f'{mode}/{name}','kind':'confirmed-targets','predictions':predictions(doc,us,mapping),'changed_targets':changes,'note':'same reference unit ids/groups, only supplied readings transliteration changed; no reference times'})
        print(sid,mode,'text module complete',flush=True)

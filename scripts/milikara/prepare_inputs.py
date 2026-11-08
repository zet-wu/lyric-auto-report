from common import *
product_imports()
import re,subprocess,unicodedata
reference=read(ROOT/'results/timing/reference.json')
records=[]
for song in reference:
    if song['id'] in ('s11','s14'):continue
    rows=[]
    for line in song['lines']:
        units=[]
        for leaf in line['leaves']:
            value=''.join(c for c in unicodedata.normalize('NFKC',leaf['text']) if c.isalnum() or c in "ー'’")
            if not value or not any(c.isalnum() for c in value) and value!='ー':continue
            language='japanese' if re.fullmatch('[ぁ-ゖァ-ヺー]+',value) else 'latin'
            units.append({'id':leaf['id'],'source_reading':leaf['text'],'reading':value,'language':language,'start':leaf['start'],'end':leaf['end']})
        if not units:continue
        rows.append({'id':line['id'],'index':line['index'],'text':line['text'],'start':line['vocal_start'],'end':line['vocal_end'],'units':units})
    records.append({'id':song['id'],'name':song['name'],'cohort':'teochew_kana' if song['id']=='s13' else 'japanese','lines':rows})
dump(OUT/'reading-input.json',records)
subprocess.run(['node',str(ROOT/'scripts/milikara/romanize.cjs')],check=True)
records=read(OUT/'romanized.json')
references=[];targets=[]
for song in records:
    ref={**song,'lines':[]};target={**song,'lines':[]}
    for line in song['lines']:
        ref['lines'].append({**line,'reference':line['units']})
        target['lines'].append({'id':line['id'],'index':line['index'],'text':line['text'],
            'units':[{k:v for k,v in u.items() if k not in ('start','end')} for u in line['units']]})
    references.append(ref);targets.append(target)
dump(OUT/'references.json',references);dump(OUT/'confirmed-targets.json',targets);dump(OUT/'phonetic-targets.json',targets)
dump(OUT/'audio-sources.json',{s['id']:{'audio':s['audio'],'sha256':s['audio_sha256']} for s in reference})
print('Prepared targets',[(s['id'],sum(len(l['units']) for l in s['lines'])) for s in targets])

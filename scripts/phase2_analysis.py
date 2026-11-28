"""Post-processing analyses for M2/M3/M4/M5/M7/M8; no model inference."""
import collections
import unicodedata
import re
from shared import ROOT,read,dump,exists
from phase2_metrics import measure,publish,reading_items,item,span,table,primary_reference_unit
import numpy as np


def phonetic_tags(text,language):
    raw=unicodedata.normalize('NFKC',text).lower()
    value=re.sub(r'[0-9\s]','',raw)
    tags=[]
    if any('\u3400'<=char<='\u9fff' for char in value):return ['unclassified']
    if re.search(r'(ng|[nm])$',value):tags.append('nasal_coda')
    elif re.search(r'[ptkh]$',value):tags.append('stop_coda')
    else:tags.append('open_cv')
    if re.search(r'zh|ch|sh|[rü]|er|eo|oe|yu|aa',value) or any(mark in unicodedata.normalize('NFD',text) for mark in ('\u0303','ⁿ')) or language=='teochew' and re.search(r'bh|gh|chh|o͘|ọ',value):tags.append('non_ja_phoneme')
    return tags


def tone_normalize(text,without=False):
    text=unicodedata.normalize('NFKC',text).lower()
    if without:
        text=''.join(char for char in unicodedata.normalize('NFD',text) if char not in '\u0300\u0301\u0304\u030c\u0302' and not char.isdigit())
        text=unicodedata.normalize('NFC',text)
    return ''.join(char for char in text if char.isalnum() or unicodedata.combining(char))


def m2(config,refs,leaf):
    groups=[]
    languages={line['id']:line['language'] for song in refs.values() for line in song['lines']}
    line_lang={(song['id'],line['index']):line['language'] for song in refs.values() for line in song['lines']}
    for row in leaf:
        if 'dictionary' in row['condition'] or line_lang[row['song'],row['line']]=='ja':continue
        for tag in (phonetic_tags(row['text'],line_lang[row['song'],row['line']]) if row.get('reference_kind')=='ruby' else ['unclassified']):groups.append(dict(row,phonetic_group=tag))
    metrics=[]
    for condition,group in sorted({(row['condition'],row['phonetic_group']) for row in groups}):
        metrics.append({'condition':condition,'phonetic_group':group,**measure([row for row in groups if row['condition']==condition and row['phonetic_group']==group])})
    table(ROOT/'results/M2/phonetic-groups.csv',metrics);dump(ROOT/'results/M2/phonetic-groups.json',{'metrics':metrics,'classification':'Reference reading spelling; groups overlap. Coda categories partition the romanized input; missing native predictions remain misses.','non_ja_phoneme':'Predeclared orthographic proxies, not expert phonetic annotation. Japanese-context lines in jy01 are excluded from these non-Japanese phonetic groups; plain body units without an annotated phonetic reading are unclassified.'})
    rows=[]
    for sid in config['modules']['M2']['dictionary_songs'].values():
        for song_id in sid:
            native=read(ROOT/'results/M2/dictionary/inputs'/f'{song_id}.json');song=refs[song_id]
            for line,source in zip(song['lines'],native['lines'],strict=True):
                proposals=[proposal for proposal in native['proposals'] if proposal['line_id']==source['id']]
                gold=[];pos=0
                for word in line['words']:
                    text=word['text'].replace('\n','').replace('\r','').replace('\t','');reading=''.join(leaf['text'] for leaf in line['leaves'] if leaf['word_id']==word['id'])
                    gold.append({'a':pos,'b':pos+len(text),'reading':reading});pos+=len(text)
                # Dictionaries analyze the same outer-trimmed product text.
                trim=len(line['text'].replace('\n','').replace('\r','').replace('\t',''))-len(line['text'].replace('\n','').replace('\r','').replace('\t','').lstrip())
                for part in gold:part['a']-=trim;part['b']-=trim
                edges=sorted(({max(0,part['a']) for part in gold}|{part['b'] for part in gold}) & ({part['base_start'] for part in proposals}|{part['base_end'] for part in proposals}))
                for a,b in zip(edges,edges[1:]):
                    reference=''.join(part['reading'] for part in gold if a<=part['a'] and part['b']<=b)
                    prediction=''.join(''.join(part['units']) if part['units'] else part['base'] for part in proposals if a<=part['base_start'] and part['base_end']<=b)
                    if not reference or any('\u3400'<=char<='\u9fff' for char in reference):continue
                    for without in (False,True):
                        rows.append({'song':song_id,'line':line['index'],'a':a,'b':b,'tone_mode':'without_tone' if without else 'with_tone','reference':reference,'prediction':prediction,'exact':tone_normalize(reference,without)==tone_normalize(prediction,without)})
    summary=[]
    for sid in ['ALL',*config['modules']['M2']['dictionary_songs']['zh-pinyin'],*config['modules']['M2']['dictionary_songs']['yue-jyutping'],*config['modules']['M2']['dictionary_songs']['teochew-chaozhou-puj']]:
        for mode in ('with_tone','without_tone'):
            selected=[row for row in rows if (sid=='ALL' or row['song']==sid) and row['tone_mode']==mode]
            summary.append({'song':sid,'tone_mode':mode,'n':len(selected),'exact':sum(row['exact'] for row in selected),'accuracy_pct':100*sum(row['exact'] for row in selected)/len(selected) if selected else None})
    dump(ROOT/'results/M2/dictionary/summary.json',summary);table(ROOT/'results/M2/dictionary/metrics.csv',summary);dump(ROOT/'results/M2/dictionary/items.json.gz',rows)


def m3(native,config):
    rows=[];tokens=[]
    for sep in ('demucs','bs'):
        for sid in config['modules']['M3']['songs']:
            base=native.get(('M3',f'{sep}-float-nextfire',sid),{})
            encoded=native.get(('M3',f'{sep}-aac-nextfire',sid),{})
            a=base.get('core_segments',[]);b=encoded.get('core_segments',[])
            row={'song':sid,'separator':sep,'float_segments':len(a),'aac_segments':len(b),'status':'ok' if a and b else 'failed'}
            for endpoint in ('core_start','core_end'):
                first=np.array([part[endpoint] for part in a]);second=np.array([part[endpoint] for part in b])
                shifts=np.r_[np.min(np.abs(first[:,None]-second),axis=1),np.min(np.abs(first[:,None]-second),axis=0)]*1000 if len(first) and len(second) else np.array([])
                row.update({endpoint+'_mean_abs_ms':float(shifts.mean()) if len(shifts) else None,endpoint+'_p95_abs_ms':float(np.percentile(shifts,95)) if len(shifts) else None,endpoint+'_max_abs_ms':float(shifts.max()) if len(shifts) else None})
            rows.append(row)
        for fmt in ('float','aac'):
            for backend in ('nextfire','mms-fa'):
                data=native.get(('M3',f'{sep}-{fmt}-{backend}','t01'),{})
                tokens.append({'separator':sep,'format':fmt,'backend':backend,'status':data.get('status','pending'),'input_count':len(data['input_tokens']) if 'input_tokens' in data else None,'empty_model_text_count':sum(not unit['model_text'] for unit in data['input_tokens']) if 'input_tokens' in data else None,'empty_model_text_units':[unit for unit in data.get('input_tokens',[]) if not unit['model_text']],'inputs':data.get('input_tokens',[])})
    cohort_metrics=[]
    summary=read(ROOT/'results/M3/summary.json')
    leaf=read(ROOT/'results/M3/reading-items.json')
    for condition in sorted({row['condition'] for row in leaf}):
        for cohort,songs in config['modules']['M3']['cohorts'].items():
            cohort_metrics.append({'condition':condition,'cohort':cohort,**measure([row for row in leaf if row['primary_reading_unit'] and row['condition']==condition and row['song'] in songs])})
    summary['persistence_recipe']='Original float/wav vs current Studio AAC encoder, including its peak-overflow prevention gain; both decoded to float32 for alignment. Per-song gain is retained in prediction details.';summary['cohorts']=cohort_metrics;dump(ROOT/'results/M3/summary.json',summary);table(ROOT/'results/M3/cohorts.csv',cohort_metrics)
    dump(ROOT/'results/M3/core-boundaries.json',{'matching':'Bidirectional nearest endpoint distances; segment-count changes reported separately; no forced one-to-one correspondence.','songs':rows});table(ROOT/'results/M3/core-boundaries.csv',rows)
    dump(ROOT/'results/M2/t01-input-tokens.json.gz',tokens)


def m4(config,refs,leaf):
    from scipy.stats import pearsonr,spearmanr
    features=[]
    for sid in config['modules']['M4']['songs']:
        reference=[unit for line in refs[sid]['lines'] for unit in line['leaves'] if primary_reference_unit(line,unit)]
        durations=np.array([unit['end']-unit['start'] for unit in reference])*1000
        merged=[]
        for unit in sorted(reference,key=lambda unit:unit['start']):
            if merged and unit['start']<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],unit['end'])
            else:merged.append([unit['start'],unit['end']])
        active=sum(b-a for a,b in merged)
        features.append({'song':sid,'unit_count':len(reference),'mean_duration_ms':float(durations.mean()),'median_duration_ms':float(np.median(durations)),'p10_duration_ms':float(np.percentile(durations,10)),'p90_duration_ms':float(np.percentile(durations,90)),'syllables_per_second':len(reference)/active if active else None})
    rows=[row for row in leaf if row['primary_reading_unit']];song_rows=[];correlations=[];bins=[]
    for condition in sorted({row['condition'] for row in rows}):
        for feature in features:song_rows.append({**feature,'condition':condition,**measure([row for row in rows if row['condition']==condition and row['song']==feature['song']])})
        selected=[row for row in song_rows if row['condition']==condition]
        for feature in config['modules']['M4']['song_features']:
            for outcome in config['modules']['M4']['outcomes']:
                pairs=[(row[feature],row[outcome]) for row in selected if row[feature] is not None and row[outcome] is not None]
                valid=len(pairs)>=3 and len({pair[0] for pair in pairs})>1 and len({pair[1] for pair in pairs})>1
                for method,function in [('pearson',pearsonr),('spearman',spearmanr)]:
                    result=function(*zip(*pairs)) if valid else None
                    correlations.append({'condition':condition,'feature':feature,'outcome':outcome,'method':method,'n':len(pairs),'coefficient':float(result.statistic) if valid else None,'p_value':float(result.pvalue) if valid else None,'unavailable_reason':None if valid else 'Fewer than three paired songs or constant feature/outcome'})
        for name,lo,hi in [('<120',0,120),('120-250',120,250),('250-500',250,500),('500-1000',500,1000.0000001),('>1000',1000.0000001,float('inf'))]:
            selected=[row for row in rows if row['condition']==condition and lo<=(row['end']-row['start'])*1000<hi]
            bins.append({'condition':condition,'duration_bin_ms':name,**measure(selected)})
    publish('M4',{'song_features':features,'correlations':correlations,'duration_bins':bins,'effective_rate_denominator':'Union duration of positive timed human reading units; overlapping intervals counted once.'},song_rows)
    table(ROOT/'results/M4/correlations.csv',correlations);table(ROOT/'results/M4/duration-bins.csv',bins)
    dump(ROOT/'results/M4/spica-paired.json.gz',{'songs':['j14','j15'],'pairing':'Source line and unit index; texts retained for inspection without assuming identical readings.','units':[row for row in rows if row['song'] in ('j14','j15')]})


def m5(config):
    rows=[]
    for model in config['modules']['M5']['models']:
        for device in ('cuda','cpu'):
            path=ROOT/'results/separation-resources'/f'{model}{"-cpu" if device=="cpu" else ""}.json'
            data=read(path) if exists(path) else {'status':'pending','records':[]}
            for record in data.get('records',[]):rows.append({'model':model,'device':device,**record,'cpu_energy_unavailable_reason':record.get('cpu_energy_unavailable_reason') if device=='cpu' else None})
    table(ROOT/'results/M5/resources.csv',rows);dump(ROOT/'results/M5/resources.json',{'records':rows,'gpu_energy_scope':'GPU board energy including idle; serial warm inference; decode, model load, file encoding excluded.','cpu_energy':'CPU package RAPL counter differences when readable; unavailable counter reasons are recorded with null, never zero.'})
    aggregates=[]
    for model in config['modules']['M5']['models']:
        for device in ('cuda','cpu'):
            records=[row for row in rows if row['model']==model and row['device']==device]
            for song in ['ALL',*dict.fromkeys(row['song'] for row in records)]:
                selected=[row for row in records if song=='ALL' or row['song']==song]
                if not selected:continue
                seconds=np.array([row['seconds'] for row in selected]);duration=sum(row['duration'] for row in selected)
                def complete_sum(key):
                    values=[row.get(key) for row in selected]
                    return sum(values) if all(value is not None for value in values) else None
                def peak(key):
                    values=[row[key] for row in selected if row.get(key) is not None]
                    return max(values) if values else None
                energy=complete_sum('board_energy_joules')
                aggregates.append({'model':model,'device':device,'song':song,'measurements':len(selected),
                    'mean_seconds':float(seconds.mean()),'std_seconds':float(seconds.std(ddof=1)) if len(seconds)>1 else None,
                    'min_seconds':float(seconds.min()),'max_seconds':float(seconds.max()),
                    'total_inference_seconds':float(seconds.sum()),'total_audio_seconds':duration,
                    'rtf':float(seconds.sum()/duration) if duration else None,
                    'max_rss_bytes':peak('rss_bytes'),'max_process_gpu_bytes':peak('process_gpu_bytes'),'max_allocated_bytes':peak('allocated_bytes'),
                    'total_board_energy_joules':energy,'mean_board_power_w':energy/float(seconds.sum()) if energy is not None else None,
                    'total_cpu_package_energy_joules':complete_sum('cpu_package_energy_joules'),
                    'cpu_energy_unavailable_reason':'; '.join(dict.fromkeys(row['cpu_energy_unavailable_reason'] for row in selected if row.get('cpu_energy_unavailable_reason'))) or None})
    table(ROOT/'results/M5/resources-summary.csv',aggregates)
    dump(ROOT/'results/M5/resources-summary.json',{'metrics':aggregates,'aggregation':'Per song and ALL measured repeats; warm-ups excluded. Sample standard deviation uses ddof=1. RTF is total inference time / total audio duration. Energy totals cover all listed measurements; unavailable energy remains null.'})
    summary=read(ROOT/'results/M5/summary.json');summary['resources']=rows;summary['resource_summary']=aggregates
    summary['completion']=[row for row in summary['completion'] if not row['condition'].startswith(('resources-','separation-'))]
    for model in config['modules']['M5']['models']:
        for device in ('cuda','cpu'):
            path=ROOT/'results/separation-resources'/f'{model}{"-cpu" if device=="cpu" else ""}.json'
            data=read(path) if exists(path) else {'status':'pending'}
            summary['completion'].append({'condition':'resources-'+model+'-'+device,'status':data.get('status','ok'),'error':data.get('error'),'records':len(data.get('records',[]))})
    for folder in (ROOT/'results/M5/separation').glob('*'):
        for path in folder.glob('*.json.gz'):
            data=read(path);summary['completion'].append({'condition':'separation-'+folder.name,'song':data.get('song',path.name.split('.')[0]),'status':data['status'],'error':data.get('error'),'failed_stage':data.get('failed_stage')})
    dump(ROOT/'results/M5/summary.json',summary)


def m7(config):
    references={song['id']:song for song in read(ROOT/'results/milikara/references.json')}
    rows=[];states=[]
    paths=sorted((ROOT/'results/milikara/predictions').glob('*.json.gz'))
    for path in paths:
        data=read(path);sid=data.get('song',path.name.split('--')[0]);name=data.get('experiment','--'.join(path.name.removesuffix('.json.gz').split('--')[1:]))
        states.append({'song':sid,'condition':name,'status':data.get('status','ok'),'error':data.get('error')})
        predictions=data.get('predictions',[])
        for li,line in enumerate(references[sid]['lines']):
            for ui,ref in enumerate(line['reference']):
                if ref['start'] is None or ref['end'] is None or ref['end']<=ref['start']:continue
                p=predictions[li][ui] if li<len(predictions) and ui<len(predictions[li]) else None
                valid=p and not p.get('crosses_removed_gap')
                rows.append(item(sid,line['index'],ref['id'],(ref['start'],ref['end']),(p['start'],p['end']) if valid else (None,None),condition=name,language=ref['language']))
    metrics=[{'condition':condition,'song':sid,'scope':scope,**measure([row for row in rows if row['condition']==condition and (sid=='ALL' or row['song']==sid) and (scope=='all' or row['language']=='japanese')])} for condition in sorted({row['condition'] for row in rows}) for sid in ['ALL',*config['dataset']['ja']] for scope in ('japanese','all')]
    publish('M7',{'metrics':metrics,'completion':states,'soft_factorial':8,'single_controls':2,'original_mix_controls':2,'reading_policy':'Japanese primary units and all-unit secondary scope follow Phase 1.','decoder':'Unmodified native MiliKara decoder; shared cached emissions.'},metrics,rows)


def m8(config,refs):
    rows=[];metrics=[];states=[]
    separators=[('demucs','G1-studio-demucs-nextfire','')]
    if (ROOT/'results/M8/predictions/bs-short_unit_30ms-nextfire_baseline').exists():
        separators.append(('bs','G1-studio-bs-nextfire','bs-'))
    for sep,base_dir,prefix in separators:
        baselines={sid:reading_items(refs[sid],read(ROOT/'results/M1/predictions'/base_dir/f'{sid}.json')) for sid in config['dataset']['ja']}
        for trigger in config['modules']['M8']['triggers']:
            for strategy in config['modules']['M8']['strategies']:
                all_items=[];fixed=broken=triggered=lines=0
                for sid in config['dataset']['ja']:
                    path=ROOT/'results/M8/predictions'/f'{prefix}{trigger}-{strategy}'/f'{sid}.json'
                    data=read(path) if exists(path) else {'status':'pending'}
                    states.append({'separator':sep,'song':sid,'trigger':trigger,'strategy':strategy,'status':data['status'],'error':data.get('error'),'line_failures':{key:value for key,value in data.get('local_results',{}).items() if value.get('status')=='failed'}})
                    current=reading_items(refs[sid],data);before={row['unit']:row for row in baselines[sid]}
                    for row in current:
                        if not row['primary_reading_unit']:continue
                        base=before[row['unit']];was=base['valid'] and max(abs(base['ds']),abs(base['de']))<=.100000001
                        now=row['valid'] and max(abs(row['ds']),abs(row['de']))<=.100000001
                        fixed+=int(now and not was);broken+=int(was and not now)
                        all_items.append(dict(row,separator=sep,trigger=trigger,strategy=strategy))
                    triggered+=len(data.get('triggered_lines',[]));lines+=data.get('line_count',len(refs[sid]['lines']))
                metrics.append({'separator':sep,'trigger':trigger,'strategy':strategy,'triggered_lines':triggered,'line_count':lines,'triggered_fraction':triggered/lines if lines else None,'fixed_count':fixed,'broken_count':broken,'net_gain':fixed-broken,**measure(all_items)})
                rows.extend(all_items)
    publish('M8',{'metrics':metrics,'completion':states,'oracle_top_k':'Reference-error top K; K equals combined_30ms selected count for the same song. Excluded from deployable triggers.'},metrics,rows)


def m10(config,refs):
    import xml.etree.ElementTree as ET
    from comparison.score_reading import kana,unique_boundaries,segment,row as rrow
    from comparison import score as legacy
    m10_cfg=config['modules']['M10']
    songs=m10_cfg['songs']
    ja_songs=m10_cfg.get('japanese_songs',[s for s in songs if s!='jy01'])
    bg_songs=m10_cfg.get('background_songs',['j15','j16','j19'])
    stages=m10_cfg['stages']
    eng_cfg=m10_cfg.get('english_syllable_mappings',{})
    def parse_ts(val):
        if not val:return None
        parts=val.split(':')
        if len(parts)==2:return int(parts[0])*60+float(parts[1])
        if len(parts)==3:return int(parts[0])*3600+int(parts[1])*60+float(parts[2])
        return float(val)
    def parse_bg_refs(sid):
        NS={'ttml':'http://www.w3.org/ns/ttml','ttm':'http://www.w3.org/ns/ttml#metadata','tts':'http://www.w3.org/ns/ttml#styling'}
        tree=ET.parse(ROOT/refs[sid]['ttml'])
        out=[]
        for li,bg in enumerate(tree.findall('.//ttml:span[@ttm:role="x-bg"]',NS),1):
            leaves=[]
            for ch in bg:
                if ch.attrib.get('{http://www.w3.org/ns/ttml#styling}ruby')=='container':
                    for tc in ch:
                        if tc.attrib.get('{http://www.w3.org/ns/ttml#styling}ruby')=='textContainer':
                            for rt in tc:
                                t=''.join(rt.itertext()).strip()
                                if t and any(c.isalnum() for c in t):
                                    leaves.append({'text':t,'start':parse_ts(rt.attrib.get('begin')),'end':parse_ts(rt.attrib.get('end'))})
                else:
                    t=''.join(ch.itertext()).strip()
                    clean=''.join(c for c in t if c.isalnum())
                    if clean:
                        leaves.append({'text':clean,'start':parse_ts(ch.attrib.get('begin')),'end':parse_ts(ch.attrib.get('end'))})
            out.append({'index':li,'text':''.join(bg.itertext()),'leaves':leaves})
        return out
    def to_parts(line_obj):
        parts=[]
        for word in line_obj['words']:
            units=[rrow(u['reading'],u['begin_ms'],u['end_ms'],1000) for u in word.get('ruby_units',[])]
            if not units and legacy.norm(word['text']):
                units=[rrow(word['text'],word.get('begin_ms'),word.get('end_ms'),1000)]
            parts.append(segment(word['text'],units,word['begin_ms']/1000 if word.get('begin_ms') is not None else None,word['end_ms']/1000 if word.get('end_ms') is not None else None))
        return parts
    def load_stage(sid,stage):
        data=read(ROOT/'results/M10/predictions'/stage/f'{sid}.json')
        if sid=='j19':
            main_raw=data['lines'][:50];bg_raw=data['lines'][50:]
        else:
            main_raw=[l for l in data['lines'] if not l.get('background_of')]
            bg_raw=[l for l in data['lines'] if l.get('background_of')]
        return data,[to_parts(l) for l in main_raw],[to_parts(l) for l in bg_raw]
    def score_song(sid,stage,pred_lines):
        song=refs[sid];eng_map={(e['line'],e['surface']):(e['reference'],e['prediction']) for e in eng_cfg.get(sid,[])}
        items=[]
        for li,line in enumerate(song['lines']):
            gold=legacy.positioned(line['words'],line['text']);parts=legacy.positioned(pred_lines[li],line['text'])
            edges=sorted({0,*[w['b'] for w in gold]} & {0,*[p['b'] for p in parts]})
            leaf_rows={}
            line_lang=line.get('language','ja')
            for idx,u in enumerate(line['leaves']):
                if not legacy.valid(u['start'],u['end']) or not any(c.isalnum() for c in u['text']):continue
                pri=primary_reference_unit(line,u)
                leaf_rows[u['id']]={'condition':stage,'song':sid,'line':line['index'],'line_language':line_lang,'unit':u['id'],'unit_index':idx,'text':u['text'],'start':u['start'],'end':u['end'],
                    'pred_start':None,'pred_end':None,'ds':None,'de':None,'valid':False,'missing_reason':'reading_mapping',
                    'primary_reading_unit':pri,'language':line_lang if pri else 'en','sokuon':kana(u['text'])=='っ','over1s_ref':(u['end']-u['start'])>1.0}
            for left,right in zip(edges,edges[1:]):
                gw=[w for w in gold if left<=w['a'] and w['b']<=right];pw=[p for p in parts if left<=p['a'] and p['b']<=right]
                gids={w['id'] for w in gw};gu=[u for u in line['leaves'] if u['word_id'] in gids and u['id'] in leaf_rows]
                native_units=[]
                for p in pw:native_units.extend(p['units'])
                alias_map={}
                for w in gw:
                    key=(line['index'],w['text'])
                    if key in eng_map:
                        expected,aliases=eng_map[key]
                        w_leaves=[u for u in gu if u['word_id']==w['id']]
                        assert [u['text'].strip() for u in w_leaves]==expected,(sid,stage,key)
                        for u,al in zip(w_leaves,aliases):alias_map[u['id']]=al
                pu=[];pos=0
                for u in native_units:
                    rd=kana(u['text'])
                    if rd:pu.append({**u,'a':pos,'b':pos+len(rd)});pos+=len(rd)
                ga=[];pos=0
                for u in gu:
                    rd=kana(alias_map.get(u['id'],u['text']))
                    if rd:ga.append({**u,'a':pos,'b':pos+len(rd),'normalized':rd});pos+=len(rd)
                gs=''.join(u['normalized'] for u in ga);ps=''.join(kana(u['text']) for u in pu)
                if not gs or not ps:continue
                mapping=unique_boundaries(gs,ps);pe={0,*[u['b'] for u in pu]}
                for u in ga:
                    out=leaf_rows[u['id']];a,b=mapping.get(u['a']),mapping.get(u['b'])
                    if a is None or b is None or b<=a:continue
                    if a not in pe or b not in pe:out['missing_reason']='merged';continue
                    us=[p for p in pu if a<=p['a'] and p['b']<=b];x,y=legacy.envelope(us)
                    ok=bool(us) and us[0]['a']==a and us[-1]['b']==b and legacy.valid(x,y)
                    out.update(pred_start=x,pred_end=y,valid=ok,ds=x-u['start'] if ok else None,de=y-u['end'] if ok else None,missing_reason=None if ok else 'invalid_time')
            items.extend(leaf_rows.values())
        return items
    def score_bg(sid,stage,bg_pred_lines):
        bg_refs=parse_bg_refs(sid);bg_items=[]
        for li,(ref_bg,pred_parts) in enumerate(zip(bg_refs,bg_pred_lines,strict=True),1):
            nu=[u for p in pred_parts for u in p['units']]
            pu=[];pos=0
            for u in nu:
                rd=kana(u['text'])
                if rd:pu.append({**u,'a':pos,'b':pos+len(rd)});pos+=len(rd)
            ga=[];pos=0
            for idx,u in enumerate(ref_bg['leaves']):
                rd=kana(u['text'])
                if rd:ga.append({**u,'id':f'{sid}:bg:{li}:{idx}','a':pos,'b':pos+len(rd),'normalized':rd});pos+=len(rd)
            gs=''.join(u['normalized'] for u in ga);ps=''.join(kana(u['text']) for u in pu)
            mapping=unique_boundaries(gs,ps) if gs and ps else {};pe={0,*[u['b'] for u in pu]}
            for u in ga:
                a,b=mapping.get(u['a']),mapping.get(u['b'])
                x,y=(None,None);ok=False
                if a is not None and b is not None and b>a and a in pe and b in pe:
                    us=[p for p in pu if a<=p['a'] and p['b']<=b]
                    if us and us[0]['a']==a and us[-1]['b']==b:
                        x,y=legacy.envelope(us);ok=legacy.valid(x,y)
                bg_items.append({'condition':stage,'song':sid,'line':li,'unit':u['id'],'text':u['text'],'start':u['start'],'end':u['end'],
                    'pred_start':x,'pred_end':y,'valid':ok,'ds':x-u['start'] if ok else None,'de':y-u['end'] if ok else None})
        return bg_items
    all_items=[];bg_all_items=[];completion=[];loaded={}
    for stage in stages:
        for sid in songs:
            data,lines,bg_lines=load_stage(sid,stage);loaded[stage,sid]=(data,lines,bg_lines)
            items=score_song(sid,stage,lines);all_items.extend(items)
            if sid in bg_songs:
                bg_all_items.extend(score_bg(sid,stage,bg_lines))
            completion.append({'condition':stage,'song':sid,'status':'ok','project_id':data.get('project_id'),'revision':data.get('revision'),'lines':len(lines),'bg_lines':len(bg_lines),'units':len(items)})
    by_stage_unit={(r['condition'],r['song'],r['unit']):r for r in all_items}
    by_bg_unit={(r['condition'],r['song'],r['unit']):r for r in bg_all_items}
    metrics=[];changes=[]
    for sid in songs:
        init_rows=[r for r in all_items if r['condition']=='initial' and r['song']==sid]
        for r in init_rows:
            fin=by_stage_unit['final',sid,r['unit']]
            was=r['valid'] and max(abs(r['ds']),abs(r['de']))<=.100000001
            now=fin['valid'] and max(abs(fin['ds']),abs(fin['de']))<=.100000001
            if (r['pred_start'],r['pred_end'])!=(fin['pred_start'],fin['pred_end']):
                changes.append({'song':sid,'line':r['line'],'unit':r['unit'],'text':r['text'],'language':r['language'],'start':r['start'],'end':r['end'],
                    'initial_start':r['pred_start'],'initial_end':r['pred_end'],'final_start':fin['pred_start'],'final_end':fin['pred_end'],
                    'initial_hit100':was,'final_hit100':now,'final_ds_ms':round(fin['ds']*1000,3) if fin['valid'] else None,'final_de_ms':round(fin['de']*1000,3) if fin['valid'] else None})
    def add_metric(cond,sid,scope,rows,ref_map=by_stage_unit):
        if not rows:return
        base_rows=[ref_map['initial',r['song'],r['unit']] for r in rows]
        fixed=broken=changed=0
        for b,c in zip(base_rows,rows):
            was=b['valid'] and max(abs(b['ds']),abs(b['de']))<=.100000001
            now=c['valid'] and max(abs(c['ds']),abs(c['de']))<=.100000001
            fixed+=int(now and not was);broken+=int(was and not now)
            changed+=int((b['pred_start'],b['pred_end'])!=(c['pred_start'],c['pred_end']))
        metrics.append({'condition':cond,'song':sid,'scope':scope,'changed_units':changed,'fixed_count':fixed,'broken_count':broken,'net_gain':fixed-broken,**measure(rows)})
    for stage in stages:
        ja_sel=[r for r in all_items if r['condition']==stage and r['song'] in ja_songs]
        add_metric(stage,'ALL','reading_units',[r for r in ja_sel if r['primary_reading_unit']])
        add_metric(stage,'ALL','all_reading_units',ja_sel)
        add_metric(stage,'ALL','sokuon',[r for r in ja_sel if r['sokuon']])
        add_metric(stage,'ALL','reference_duration_over1s',[r for r in ja_sel if r['over1s_ref']])
        for sid in songs:
            sel=[r for r in all_items if r['condition']==stage and r['song']==sid]
            add_metric(stage,sid,'reading_units',[r for r in sel if r['primary_reading_unit']])
            add_metric(stage,sid,'all_reading_units',sel)
            if sid=='j18':
                add_metric(stage,sid,'english_units',[r for r in sel if r['language']=='en'])
            if sid=='jy01':
                add_metric(stage,sid,'ja_segment',[r for r in sel if r['line_language']=='ja'])
                add_metric(stage,sid,'yue_segment',[r for r in sel if r['line_language']=='yue'])
            if sid in ja_songs:
                sokuon_rows=[r for r in sel if r['sokuon']]
                over1s_rows=[r for r in sel if r['over1s_ref']]
                if sokuon_rows:add_metric(stage,sid,'sokuon',sokuon_rows)
                if over1s_rows:add_metric(stage,sid,'reference_duration_over1s',over1s_rows)
        add_metric(stage,'ALL_BG','background_lines',[r for r in bg_all_items if r['condition']==stage],by_bg_unit)
        for sid in bg_songs:
            add_metric(stage,sid,'background_lines',[r for r in bg_all_items if r['condition']==stage and r['song']==sid],by_bg_unit)
    # jy01 common body spans vs M2 demucs-mms-fa
    jy01_surface=[]
    m2_items=read(ROOT/'results/M2/items.json.gz')
    m2_jy01_surface=[r for r in m2_items if r['song']=='jy01' and r['condition']=='demucs-mms-fa']
    from phase2_metrics import common_rows
    jy01_pred_conds={stage:[legacy.positioned(p,l['text']) for p,l in zip(loaded[stage,'jy01'][1],refs['jy01']['lines'],strict=True)] for stage in stages}
    jy01_common=common_rows(refs['jy01'],jy01_pred_conds)
    jy01_lang={l['index']:l.get('language','ja') for l in refs['jy01']['lines']}
    for cond_name,src_mod,rows in [('initial','M10',[r for r in jy01_common if r['condition']=='initial']),('final','M10',[r for r in jy01_common if r['condition']=='final']),('demucs-mms-fa','M2',m2_jy01_surface)]:
        for sc,pred in [('all',lambda r:True),('ja',lambda r:jy01_lang[r['line']]=='ja'),('yue',lambda r:jy01_lang[r['line']]=='yue')]:
            sel=[r for r in rows if pred(r)]
            if sel:jy01_surface.append({'source_module':src_mod,'condition':cond_name,'song':'jy01','scope':sc,**measure(sel)})
    baselines=[]
    m1_items=read(ROOT/'results/M1/reading-items.json.gz')
    m1_all_conds=sorted({r['condition'] for r in m1_items})
    for cond in ('G3-studio-bs-nextfire','G3-studio-demucs-nextfire','G3-studio-demucs-mms_fa-smart','G1-studio-bs-nextfire','G2-studio-demucs-mms_fa-smart'):
        for sid in ['ALL',*ja_songs]:
            sel=[r for r in m1_items if r['condition']==cond and r['primary_reading_unit'] and (r['song'] in ja_songs if sid=='ALL' else r['song']==sid)]
            if sel:baselines.append({'source_module':'M1','condition':cond,'song':sid,'scope':'reading_units',**measure(sel)})
    for sid in ja_songs:
        best_m1=max((measure([r for r in m1_items if r['condition']==c and r['primary_reading_unit'] and r['song']==sid])|{'condition':c} for c in m1_all_conds if any(r['condition']==c and r['song']==sid for r in m1_items)),key=lambda d:d['hit100_pct'])
        baselines.append({'source_module':'M1','best_route':best_m1['condition'],'condition':'M1_per_song_best','song':sid,'scope':'reading_units',**{k:v for k,v in best_m1.items() if k!='condition'}})
    m6_items=read(ROOT/'results/M6/reading-items.json.gz')
    for cond in ('bs-nextfire-core','bs-mms-fa-smart','demucs-mms-fa-smart'):
        for sid in ['ALL',*ja_songs]:
            sel=[r for r in m6_items if r['condition']==cond and r['primary_reading_unit'] and (r['song'] in ja_songs if sid=='ALL' else r['song']==sid)]
            if sel:baselines.append({'source_module':'M6','condition':cond,'song':sid,'scope':'reading_units',**measure(sel)})
    m8_items=read(ROOT/'results/M8/items.json.gz')
    for trig in ('combined_40ms','same_vowel_imbalance','oracle_top_k'):
        for strat in ('nextfire_baseline','mms_fa_local','mms_fa_global_swap'):
            for sid in ['ALL',*ja_songs]:
                sel=[r for r in m8_items if r.get('separator')=='bs' and r['trigger']==trig and r['strategy']==strat and (r['song'] in ja_songs if sid=='ALL' else r['song']==sid)]
                if sel:baselines.append({'source_module':'M8','condition':f'bs-{trig}-{strat}','song':sid,'scope':'reading_units',**measure(sel)})
    m8_combos=sorted({(r.get('separator'),r['trigger'],r['strategy']) for r in m8_items})
    for sid in ja_songs:
        best_m8=max((measure([r for r in m8_items if (r.get('separator'),r['trigger'],r['strategy'])==c and r['song']==sid])|{'condition':f'{c[0]}-{c[1]}-{c[2]}'} for c in m8_combos),key=lambda d:d['hit100_pct'])
        baselines.append({'source_module':'M8','best_route':best_m8['condition'],'condition':'M8_per_song_best','song':sid,'scope':'reading_units',**{k:v for k,v in best_m8.items() if k!='condition'}})
    m2_reading=read(ROOT/'results/M2/reading-items.json.gz')
    for cond in ('demucs-mms-fa','bs-mms-fa','demucs-nextfire','bs-nextfire'):
        sel=[r for r in m2_reading if r['song']=='jy01' and r['condition']==cond]
        if sel:
            baselines.append({'source_module':'M2','condition':cond,'song':'jy01','scope':'reading_units',**measure(sel)})
            baselines.append({'source_module':'M2','condition':cond,'song':'jy01','scope':'ja_segment',**measure([r for r in sel if r['line']<=10])})
            baselines.append({'source_module':'M2','condition':cond,'song':'jy01','scope':'yue_segment',**measure([r for r in sel if r['line']>=11])})
    publish('M10',{'metrics':metrics,'baselines':baselines,'jy01_surface':jy01_surface,'changed_units':changes,'completion':completion,'reading_policy':'Fixed human reading units on common body spans; 15 Japanese non-overlap primary reading units (n=6,500), mixed ja/yue jy01 (n=251), and 3-song background lines (6 lines, n=32). No timestamp interpolation.'},metrics,all_items)

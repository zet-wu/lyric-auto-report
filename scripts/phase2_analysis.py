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
    baselines={sid:reading_items(refs[sid],read(ROOT/'results/M1/predictions/G1-studio-demucs-nextfire'/f'{sid}.json')) for sid in config['dataset']['ja']}
    for trigger in config['modules']['M8']['triggers']:
        for strategy in config['modules']['M8']['strategies']:
            all_items=[];fixed=broken=triggered=lines=0
            for sid in config['dataset']['ja']:
                path=ROOT/'results/M8/predictions'/f'{trigger}-{strategy}'/f'{sid}.json'
                data=read(path) if exists(path) else {'status':'pending'}
                states.append({'song':sid,'trigger':trigger,'strategy':strategy,'status':data['status'],'error':data.get('error'),'line_failures':{key:value for key,value in data.get('local_results',{}).items() if value.get('status')=='failed'}})
                current=reading_items(refs[sid],data);before={row['unit']:row for row in baselines[sid]}
                for row in current:
                    if not row['primary_reading_unit']:continue
                    base=before[row['unit']];was=base['valid'] and max(abs(base['ds']),abs(base['de']))<=.100000001
                    now=row['valid'] and max(abs(row['ds']),abs(row['de']))<=.100000001
                    fixed+=int(now and not was);broken+=int(was and not now)
                    all_items.append(dict(row,trigger=trigger,strategy=strategy))
                triggered+=len(data.get('triggered_lines',[]));lines+=data.get('line_count',len(refs[sid]['lines']))
            metrics.append({'trigger':trigger,'strategy':strategy,'triggered_lines':triggered,'line_count':lines,'triggered_fraction':triggered/lines if lines else None,'fixed_count':fixed,'broken_count':broken,'net_gain':fixed-broken,**measure(all_items)})
            rows.extend(all_items)
    publish('M8',{'metrics':metrics,'completion':states,'oracle_top_k':'Reference-error top K; K equals combined_30ms selected count for the same song. Excluded from deployable triggers.'},metrics,rows)

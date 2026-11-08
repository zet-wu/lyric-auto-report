"""Score native application outputs without upstream code, models or inference caches."""
from common import *
import collections, unicodedata, numpy as np

DEST=ROOT/'results/milikara-native'
PRIMARY=set(read(ROOT/'configs/milikara-native.json')['primary_songs'])
def canonical(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())
def language(line,text):
    if line['language']!='ja_en':return line['language']
    text=canonical(text)
    return 'latin' if text.isascii() and any(c.isalpha() for c in text) else 'ja'
def valid(p):return p is not None and p[0] is not None and p[1] is not None and p[1]>p[0]
def envelope(values):
    return [values[0][0],values[-1][1]] if values and all(valid(p) for p in values) else None
def summary(rows):
    good=[r for r in rows if valid(r['prediction'])]
    errors=np.array([[p-g for p,g in zip(r['prediction'],r['reference'])] for r in good]).reshape(-1,2)*1000
    return {'n':len(rows),'valid':len(good),'missing':len(rows)-len(good),
        'hit100':int(np.all(np.abs(errors)<=100.000001,axis=1).sum()),
        'hit200':int(np.all(np.abs(errors)<=200.000001,axis=1).sum()),
        'over_1s':int(np.any(np.abs(errors)>1000,axis=1).sum()),
        'start_mae_ms':float(np.abs(errors[:,0]).mean()) if len(good) else None,
        'end_mae_ms':float(np.abs(errors[:,1]).mean()) if len(good) else None}
def spans(words):
    cursor=0;out=[]
    for word in words:
        n=len(canonical(word['text']))
        if n:out.append({**word,'a':cursor,'b':cursor+n})
        cursor+=n
    return out
def cover(words,a,b):
    chosen=[w for w in words if w['b']>a and w['a']<b]
    if not chosen or chosen[0]['a']!=a or chosen[-1]['b']!=b:return None
    return envelope([w['time'] for w in chosen])
def studio_predictions(base):
    units={u['unit_id']:u for u in base['result']['units']};groups=collections.defaultdict(list)
    for m in base['projection']['mapping']:
        p=units[m['unit_id']]['proposed_timing']
        groups[m['object_id']].append([p['start']['time'],p['end']['time']] if p['start'] and p['end'] else None)
    # Match the established Studio leaf projection: envelope of projected endpoints.
    return {k:([v[0][0],v[-1][1]] if v and v[0] and v[-1] else None) for k,v in groups.items()}
def native_predictions(run):
    return {u['unit_id']:([u['start_ms']/1000,u['end_ms']/1000] if u['start_ms'] is not None and u['end_ms'] is not None and u['status']=='ok' else None)
        for u in run.get('result',{}).get('units',[])}

rows=[];coverage=[]
for song in read(ROOT/'results/timing/reference.json'):
    sid=song['id']
    selected=os.environ.get('BENCHMARK_SONGS','').split(',')
    if selected!=[''] and sid not in selected:continue
    studio=studio_predictions(read(ROOT/'results/timing/baseline'/f'{sid}.json'))
    runs={c:read(DEST/'runs'/f'{sid}-{c}.json') for c in ('auto','manual')}
    predictions={c:native_predictions(run) for c,run in runs.items()}
    docs={c:{l['id']:l for l in run.get('lyrics',{}).get('lines',[])} for c,run in runs.items()}
    for c,run in runs.items():
        coverage.append({'song':sid,'condition':c,'status':run['status'],'seconds':run['seconds'],
            'reading_audit':read(DEST/'inputs/manual'/f'{sid}.json')['reading_audit'] if c=='manual' else None,
            'error':run.get('error'),'issues':collections.Counter(i['code'] for i in run.get('result',{}).get('issues',[])),
            'line_status':collections.Counter(l['status'] for l in run.get('result',{}).get('lines',[])),
            'candidates':len(run.get('result',{}).get('candidates',[])),
            'stats':run.get('result',{}).get('stats',{})})
    for line in song['lines']:
        for leaf in line['leaves']:
            truth=[leaf['start'],leaf['end']]
            if not canonical(leaf['text']) or not valid(truth):continue
            for method,pred in [('studio',studio),('manual',predictions['manual'])]:
                rows.append({'song':sid,'line':line['id'],'comparison':'leaf','language':language(line,leaf['text']),
                    'method':method,'id':leaf['id'],'text':leaf['text'],'reference':truth,'prediction':pred.get(leaf['id'])})
        gold=spans([{'id':w['id'],'text':w['text'],'time':[w['start'],w['end']]} for w in line['words']])
        baseline=[]
        for w in gold:
            children=[u for u in line['leaves'] if u['word_id']==w['id'] and canonical(u['text'])]
            baseline.append({**w,'time':envelope([studio.get(u['id']) for u in children])})
        native={}
        for condition in runs:
            doc=docs[condition].get(line['id'])
            if doc is None:
                native[condition]=[{**w,'time':None} for w in gold]
                continue
            assert canonical(doc['text'])==canonical(line['text'])
            native[condition]=spans([{'text':s['surface'],'time':envelope([predictions[condition].get(u['id']) for u in s['units']])}
                for s in doc['segments']])
            assert ''.join(canonical(w['text']) for w in native[condition])==canonical(line['text']),(sid,line['id'],condition)
        boundaries=lambda words:{w['a'] for w in words}|{w['b'] for w in words}
        common=sorted(boundaries(gold)&boundaries(native['auto'])&boundaries(native['manual']))
        for a,b in zip(common,common[1:]):
            truth=cover(gold,a,b)
            if not valid(truth):continue
            text=''.join(w['text'] for w in gold if w['a']>=a and w['b']<=b)
            for method,words in [('studio',baseline),*native.items()]:
                rows.append({'song':sid,'line':line['id'],'comparison':'common_text','language':language(line,text),
                    'method':method,'a':a,'b':b,'text':text,'reference':truth,'prediction':cover(words,a,b)})
groups=collections.defaultdict(list)
for row in rows:groups[(row['song'],row['comparison'],row['language'],row['method'])].append(row)
by_song=[{'song':k[0],'comparison':k[1],'language':k[2],'method':k[3],**summary(v)} for k,v in groups.items()]
aggregate=[]
for comparison in ('leaf','common_text'):
    for lang in ('ja','latin'):
        for method in ('studio','manual') if comparison=='leaf' else ('studio','auto','manual'):
            selected=[r for r in rows if r['song'] in PRIMARY and (r['comparison'],r['language'],r['method'])==(comparison,lang,method)]
            per=[r for r in by_song if r['song'] in PRIMARY and (r['comparison'],r['language'],r['method'])==(comparison,lang,method)]
            aggregate.append({'comparison':comparison,'language':lang,'method':method,**summary(selected),
                'songs':len(per),'macro100':float(np.mean([r['hit100']/r['n'] for r in per])) if per else None})
dump(DEST/'metrics.json',{'aggregate':aggregate,'by_song':by_song,'completion':coverage})
with gzip.GzipFile(filename=str(DEST/'scored-units.json.gz'),mode='wb',mtime=0) as stream:
    stream.write((json.dumps(rows,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode())
for row in aggregate:print(row)

references={s['id']:s for s in read(ROOT/'results/timing/reference.json')}
index={(r['song'],r['comparison'],r['language'],r['method']):r for r in by_song}
lines=['# 原生 MiliKara：逐曲对照','',
    '所有命中均要求起止同时在 100 ms 内。主报告按歌曲等权；本表逐曲列出计数和比例。','',
    '## 人工读音、原标注日语叶级单元','',
    '| 歌曲 | 单元数 | Studio 命中 | MiliKara 命中 | Studio / MiliKara 缺失 | Studio / MiliKara >1s |',
    '| --- | ---: | ---: | ---: | ---: | ---: |']
fmt=lambda r:f"{r['hit100']} ({100*r['hit100']/r['n']:.2f}%)"
for sid in sorted(PRIMARY):
    if (sid,'leaf','ja','studio') not in index:continue
    a,b=[index[(sid,'leaf','ja',m)] for m in ('studio','manual')]
    lines.append(f"| {sid} {references[sid]['name']} | {a['n']} | {fmt(a)} | {fmt(b)} | {a['missing']} / {b['missing']} | {a['over_1s']} / {b['over_1s']} |")
lines+=['','## 共同文本区间、日语主组','',
    '| 歌曲 | 区间数 | Studio 人工 | MiliKara 自动 | MiliKara 人工 |',
    '| --- | ---: | ---: | ---: | ---: |']
for sid in sorted(PRIMARY):
    if (sid,'common_text','ja','studio') not in index:continue
    a,b,c=[index[(sid,'common_text','ja',m)] for m in ('studio','auto','manual')]
    lines.append(f"| {sid} | {a['n']} | {fmt(a)} | {fmt(b)} | {fmt(c)} |")
lines+=['','## 压力测试、共同文本区间','',
    's11 粤语部分的 147 个汉字和 s14 的 300 个汉字没有人工语音转写；“原标注”列保留这些原文，缺失正常计入分母。s13 使用人工假名。固定日语对齐模型。','',
    '| 歌曲 / 语种 | 区间数 | Studio 原标注 | MiliKara 自动 | MiliKara 原标注 |',
    '| --- | ---: | ---: | ---: | ---: |']
for sid,comparison,lang,method in sorted(index):
    if sid in PRIMARY or comparison!='common_text' or method!='studio':continue
    a,b,c=[index[(sid,comparison,lang,m)] for m in ('studio','auto','manual')]
    lines.append(f"| {sid} / {lang} | {a['n']} | {fmt(a)} | {fmt(b)} | {fmt(c)} |")
lines+=['','## 原生执行耗时','',
    '单位为秒。分离列包含上游模型加载、分离、分轨同步检查及导入。对齐列包含模型加载、声学推理和原生解码／重试；两组使用独立声学缓存。s01 分离标 *，含首次模型下载。s13/s14 共享同一音频及分离结果。以下为单次质量运行记录。','',
    '| 歌曲 | 原生分离 | 自动组对齐 | 人工组对齐 |',
    '| --- | ---: | ---: | ---: |']
for sid in sorted({r['song'] for r in coverage}):
    auto,manual=[read(DEST/'runs'/f'{sid}-{c}.json') for c in ('auto','manual')]
    sep=read(ROOT/auto['separation_record'])
    value=lambda r:f"{r['seconds']['alignment']:.2f}" if 'alignment' in r['seconds'] else '失败'
    lines.append(f"| {sid} | {sep['seconds']:.2f}{'*' if sep['includes_model_download'] else ''} | {value(auto)} | {value(manual)} |")
(DEST/'tables.md').write_text('\n'.join(lines)+'\n')

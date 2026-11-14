"""Freeze full lyric targets before acoustic results; old paired subset stays fixed."""
from ablation_common import *
timing_imports()
import sys, re, unicodedata, hashlib, subprocess
sys.path.insert(0, str(UPSTREAM/'models/tifa/deps'))
from timing.llm_direct import compile_parts
from g2pflow.converters.lstm import LSTMConverter

english = LSTMConverter(dict_path=str(UPSTREAM/'models/tifa/dictionaries/ds_cmudict-07b.txt'),
                       model_path=str(UPSTREAM/'models/tifa/assets/LstmG2p-Eng'), beam_size=16)
old = {(r['song'], r['line']): r for r in read(PREVIOUS/'controlled-input-audit.json')['rows']}
yue = {int(r['id']):r for r in read(PREVIOUS/'yue-native.json')}
records, adaptations = [], []
small = str.maketrans('ァィゥェォャュョヮヵヶ', 'アイウエオヤユヨワカケ')

for song in songs():
    lines=[]
    for line in song['lines']:
        source = old.get((song['id'], line['index']))
        if source:
            groups = [{**g, 'paired':True} for g in source['groups']]
        else:
            groups=[]
            for leaf in line['leaves']:
                value=''.join(c for c in unicodedata.normalize('NFKC', leaf['text']) if c.isalnum() or c=='ー')
                if not value: continue
                kana=''.join(chr(ord(c)+96) if 'ぁ'<=c<='ゖ' else c for c in value)
                if kana=='ー' and groups:
                    groups[-1]['reading']+=kana; groups[-1]['text']+=kana
                    groups[-1]['ids'].append(leaf['id']);groups[-1]['end']=leaf['end']
                    continue
                lang='yue' if line['language']=='yue' else 'ja' if re.fullmatch('[ァ-ヺー]+',kana) else 'en'
                groups.append({'text':kana,'lang':lang,'reading':kana,'ids':[leaf['id']],
                               'start':leaf['start'],'end':leaf['end'],'paired':False})
        for index,g in enumerate(groups):
            g['key']=f'{song["id"]}:{line["index"]}:{index}'
            if g['lang']=='yue':
                native=yue[line['index']]
                assert len(native['texts'])==len(groups)
                assert native['texts'][index]==g['text']
                g['phone_groups']=[native['selected'][index]['phonemes']]
                g['reading']=' '.join(native['selected'][index]['scripts'])
            elif g['lang']=='en':
                words=english.convert(g['reading'].lower())
                phones=[p for w in words for group in w.readings[0].paths[0] for p in group.phonemes]
                if not phones: raise ValueError(g)
                g['phone_groups']=[['en/'+p for p in phones]]
                adaptations.append({'key':g['key'],'kind':'context_english_first_dictionary_or_g2p_candidate','reading':g['reading'],'phones':phones})
            else:
                try:
                    part=compile_parts(g['text'],[{k:g[k] for k in ('text','lang','reading')}])[0]
                except ValueError:
                    revised=g['reading'].translate(small)
                    if revised==g['reading']: raise
                    adaptations.append({'key':g['key'],'kind':'standalone_small_kana_context','before':g['reading'],'after':revised})
                    g['reading']=revised
                    part=compile_parts(g['text'],[{k:g[k] for k in ('text','lang','reading')}])[0]
                g['phone_groups']=[['ja/'+p for p in x['phones']] for x in part['groups']]
            g['tags']=[]
            if g['end']-g['start']>=.6-1e-9:g['tags'].append('sustained_600ms')
            if 'ー' in g['reading']:g['tags'].append('written_long_mark')
        for i,g in enumerate(groups):
            phones=sum(g['phone_groups'],[])
            if (i and phones==sum(groups[i-1]['phone_groups'],[])) or (i+1<len(groups) and phones==sum(groups[i+1]['phone_groups'],[])):
                g['tags'].append('adjacent_identical_phones')
            if i+1<len(groups) and phones[-1]==sum(groups[i+1]['phone_groups'],[])[0]:
                g['tags'].append('same_phone_at_next_boundary')
        lines.append({'index':line['index'],'text':line['text'],'language':line['language'],'groups':groups,
                      'human_window':[line['vocal_start'],line['vocal_end']]})
    records.append({'id':song['id'],'name':song['name'],'audio':song['audio'],'lines':lines})
dump(OUT/'targets.json', records)
dump(OUT/'target-adaptations.json', adaptations)
identities={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'datasets').rglob('*') if p.is_file()}
dump(OUT/'input-hashes.json',identities)
dump(OUT/'protocol.json',{
 'scope':'Module factorial, no project source edits. Frozen human readings; no LLM and no score-driven selection.',
 'separators':['demucs','bs','kim'], 'backends':['nextfire','tifa','mms_fa'],
 'strategies':['concat','padded','full','auto_mms','auto_nf','human','fixed_cores','auto_mms_pause'],
 'concat':'Per-stem current Lazulite automatic vocal core union, single ordered target chain, source-axis mapping.',
 'full':'Full stem single chain without core removal, controls concat effect.',
 'auto_mms':'Generic MMS whole-song global CTC on full stem with frozen readings. Valid line endpoints +/-0.30 s, 0.1..60 s; no reference times.',
 'auto_nf':'Same-stem NextFire concat predicted first/last endpoints +/-0.30 s, 0.1..60 s; no reference times.',
 'human':'Reference sung first/last endpoints rounded outward to 20 ms, no padding, individual line without neighbours. Diagnostic, not an upper bound.',
 'fixed_cores':'Extra BS/Kim concat condition reusing Demucs acoustic core boundaries to separate stem changes from activity detector changes.',
 'phonemes':'Full lyric chains include context outside scoring subset. Existing paired kana groups unchanged; English first G2P candidate frozen, standalone small kana normalized only in previously excluded context.',
 'primary':'11 Japanese recordings, fixed pure-kana paired units; equal-song macro primary, pooled unit micro secondary. No favoured songs.',
 'secondary':'s13 Teochew kana proxy separate; s11 Japanese/Yue mixed separate. Yue context uses selected fixed pronunciation, not a new autonomous G2P result. s14 same recording not double counted.',
 'failure':'Missing/invalid/cross-removed-gap spans retained as misses; no oracle fallback, no interpolation. Raw remapped spans also saved.',
 'subsets':['duration >=600ms proxy for sustained singing (not expert phonetic annotation)','written ー','adjacent groups with identical complete phoneme sequence','equal last/first phone across neighbouring groups'],
 'metrics':['both100/200ms','start/end MAE P95 signed bias','missing and >1s errors','duration ratio and short-collapse','repeat boundary end/start errors'],
 'sources':{str(p):subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip() for p in [STUDIO,STUDIO.parent/'lazulite',UPSTREAM]},
})
print('prepared',len(records),'songs;',sum(g['paired'] for s in records if s['id'] in PRIMARY for l in s['lines'] for g in l['groups']),'primary units')

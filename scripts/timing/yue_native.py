"""Native TIFA Yue route diagnostic; this route is NOT exposed by Timing."""
from common import *
import sys, math, traceback
MODEL=UPSTREAM/'models/tifa'
sys.path[:0]=[str(MODEL/'deps'),str(MODEL/'runtime')]
import torch, yaml, numpy as np, soundfile as sf
from inference.api import load_inference_model, load_g2p_config
from inference.data import AudioTextDataset
from lib.path_traversal import materialize_paths
from lib.config.schema import ConfigurationScope

torch.set_num_threads(8)
folder=CACHE/'yue-native';folder.mkdir(exist_ok=True)
song=next(s for s in read(OUT/'reference.json') if s['id']=='s11')
wave,rate=sf.read(CACHE/'audio'/f'{Path(song["audio"]).stem}.wav',dtype='float32',always_2d=True)
wave=wave.mean(axis=1); offsets={};filemap={}
for line in song['lines']:
    if line['language']!='yue':continue
    name=f'{line["index"]:03}';a=math.floor(line['vocal_start']/.02)*.02;b=math.ceil(line['vocal_end']/.02)*.02
    path=folder/f'{name}.wav';sf.write(path,wave[round(a*rate):round(b*rate)],rate,subtype='FLOAT')
    path.with_suffix('.txt').write_text(line['text']);filemap[name]=path;offsets[name]=a
backend,vocabulary,config=load_inference_model(MODEL/'model.pt',scope=ConfigurationScope.FA)
backend=backend.cuda().eval()
cfg={'preprocessors':[{'id':'filter-punctuation'},{'id':'strip-whitespace'}],
     'converters':[{'id':'yue-jyutping','language':'yue','kwargs':{'dict_path':str(MODEL/'dictionaries/jyutping_dict.txt')}}]}
config_path=folder/'g2p.yaml';config_path.write_text(yaml.safe_dump(cfg))
dataset=AudioTextDataset(filemap=filemap,g2p_config=load_g2p_config(config_path),g2p_root=MODEL,
                         vocabulary=vocabulary,audio_sample_rate=backend.sample_rate,language=['yue'],oov_handling='raise')
rows=[]
with torch.inference_mode():
    for index in range(len(dataset)):
        try:
            item=dataset[index]
            if item.get('skip'):raise ValueError(str(item))
            batch=dataset.collate([item]);batch={k:v.cuda() if isinstance(v,torch.Tensor) else v for k,v in batch.items()}
            spec=backend.spectrogram(batch['waveform'],batch['duration'])
            scored=backend.score(spec,paths=batch['paths'],words=batch['words'],candidates=batch['candidates'],unit='levenshtein')
            tokens,owners,groups=materialize_paths(batch['paths'],batch['words'],batch['groups'],scored.choices)
            aligned=backend.align(spec,tokens=tokens,groups=groups,unit='second',skip_penalty=.5)
            rows.append({'id':item['identifier'],'offset':offsets[item['identifier']],'texts':item['texts'],
                         'owners':owners[0].tolist(),'spans':aligned.spans[0].cpu().tolist(),'agreement':float(aligned.agreement[0]),
                         'selected':[candidates[c-1] if c>0 else None for candidates,c in zip(item['lexicon'],scored.choices[0].tolist())]})
        except Exception: rows.append({'index':index,'error':traceback.format_exc()})
        dump(OUT/'yue-native.json',rows)
        print('yue',index+1,len(dataset),flush=True)

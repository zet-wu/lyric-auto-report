from common import *
product_imports()
import numpy as np,soundfile as sf,torch,time,traceback
from dataclasses import asdict
from lazulite.audio.io import decode_audio
from lazulite.audio.preparation import prepare_existing_vocals
from lazulite.audio.concat import concatenate_cores
from lazulite.models.audio import AudioBuffer
from lazulite.models.japanese import JapaneseAlignmentRequest
from lazulite.alignment.japanese.backend import open_backend
from lazulite.alignment.japanese.stages import AcousticResult
from lazulite.alignment.japanese.run import align_japanese,JapaneseConfig
from server.alignment_projection import project_alignment
from server.alignment_postprocessing import object_timings
torch.set_num_threads(8);assert torch.cuda.is_available()
for model in ('nextfire','mms-fa'):
    backend=open_backend(ROOT/'.models'/model,'cuda')
    for sep,conditions in [('demucs',['manual','auto']),('bs',['manual'])]:
        for s in songs():
            sid=s['id'];stem=CACHE/'stems'/sep/(sid+'.wav')
            if not stem.exists():raise FileNotFoundError(stem)
            if all(exists(OUT/'studio'/f'{sid}-{sep}-{model}-{c}.json') for c in conditions):continue
            original=decode_audio(ROOT/s['audio'],sample_rate=44100,channels=2)
            samples,rate=sf.read(stem,dtype='float32',always_2d=True);v=AudioBuffer(samples.T.copy(),rate,sid)
            prepared=prepare_existing_vocals(v,reference=original,original_duration=original.duration)
            concat=concatenate_cores(v,prepared.analysis.segments,sample_rate=16000)
            probfile=CACHE/'emissions'/f'{sid}-{sep}-{model}.npy';probfile.parent.mkdir(exist_ok=True)
            if probfile.exists():probs=np.load(probfile)
            else:probs=backend.emissions(concat.audio);np.save(probfile,probs)
            acoustic=AcousticResult(probs,backend.vocab,backend.blank,backend.frames,concat.mapping,v.duration,special_tokens=backend.special_tokens)
            for condition in conditions:
                target=OUT/'studio'/f'{sid}-{sep}-{model}-{condition}.json'
                if exists(target):continue
                start=time.monotonic()
                record={'song':sid,'model':model,'separator':sep,'condition':condition,'duration':v.duration,'status':'error','stem_sha256':sha(stem)}
                try:
                    projection=project_alignment(read(CACHE/'inputs'/f'{sid}-studio-{condition}.json'),False,model={'vocabulary':backend.vocab,'blank':backend.blank})
                    result=align_japanese(None,JapaneseAlignmentRequest.from_dict(projection['request']),acoustic=acoustic,config=JapaneseConfig(hint_mode='off'))
                    record.update(status='ok',projection=projection,result=asdict(result),analysis=asdict(prepared.analysis),object_timings=object_timings(result,projection['mapping'],v,model=='mms-fa',segments=prepared.segments))
                except Exception:record['error']=traceback.format_exc();print(record['error'],flush=True)
                record['seconds']=time.monotonic()-start;dump(target,record);print('DONE',sid,sep,model,condition,record['status'],flush=True)
    backend.close()

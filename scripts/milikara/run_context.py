from common import *
from modules import *
from fast_ctc import install
import torch,time,itertools
from transformers import Wav2Vec2ForCTC
from kara_align.align.backends.chunking import chunked_forward,conv_output_length,receptive_field
install();torch.set_num_threads(8);torch.manual_seed(0)
model=Wav2Vec2ForCTC.from_pretrained(ROOT/'.models/nextfire',local_files_only=True).to('cuda').eval()
k=model.config.conv_kernel;s=model.config.conv_stride
runtime=read(OUT/'context-runtime.json')['records'] if exists(OUT/'context-runtime.json') else []
for song,ev,cache in inputs():
    sid=song['id'];doc=document(song)
    for mode,ctx in itertools.product(MODES,['2u',3]):
        y,mapping,env,activity=load_audio(song,ev,cache,mode)
        dest=CACHE/f'{sid}-{mode}-context{ctx}.npy'
        if not dest.exists():
            x=(y-y.mean())/np.sqrt(y.var()+1e-7)
            def forward(seg):
                with torch.inference_mode():return model(torch.from_numpy(np.ascontiguousarray(seg)).unsqueeze(0).to('cuda')).logits[0].float().log_softmax(-1).cpu().numpy()
            t=time.perf_counter();lp=chunked_forward(x,forward,hop=320,rf=receptive_field(k,s),n_frames=lambda n:conv_output_length(n,k,s),chunk_samples=320000,context_samples=32000 if ctx=='2u' else 48000)
            np.save(dest,lp)
            runtime=[r for r in runtime if (r['song'],r['audio'],r['context'])!=(sid,mode,ctx)]
            runtime.append({'song':sid,'audio':mode,'context':ctx,'forward_seconds':time.perf_counter()-t,'frames':len(lp),'sha256':sha(dest)})
        for code in ['00000','00001','11111']:
            flags=dict(zip(FACTORS,[c=='1' for c in code]));em=emission(cache,sid,mode,flags['delimiter'],context=ctx)
            units,outcome=global_decode(doc,em,activity,flags)
            dump(OUT/'predictions'/f'{sid}--{mode}--context{ctx}-f{code}.json',{'song':sid,'experiment':f'{mode}/context{ctx}-f{code}','kind':'confirmed-targets','predictions':predictions(doc,units,mapping)})
        print(sid,mode,ctx,'context complete',flush=True)
dump(OUT/'context-runtime.json',{'records':runtime,'device':torch.cuda.get_device_name(),'dtype':'float32','seed':0})

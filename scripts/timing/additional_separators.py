"""Generate fresh stems with the five additional historical separation models."""
from ablation_common import *
product_imports()
import time, dataclasses, hashlib, inspect, sys, argparse, random
PROCESS_START=time.perf_counter()
import numpy as np, torch, yaml, soundfile as sf
sys.path.insert(0,str(ROOT/'.deps/msst-packages'))
from ml_collections import ConfigDict
from lazulite.audio.io import decode_audio
sys.path.insert(0,str(ROOT/'.deps/msst'))
def sync(device):
    if device=='cuda':torch.cuda.synchronize()

def load(name,device):
    start=time.perf_counter()
    if name=='demucs':
        from lazulite.audio.separation import DemucsConfig,DemucsSeparator
        sep=DemucsSeparator(DemucsConfig(device=device));model=sep._load()
        cfg=dataclasses.asdict(sep.config)
        def infer(x):return sep.separate(AudioBuffer(x,44100,'research')).samples
    else:
        cfg=yaml.load((ROOT/'.models/separation'/name/'config.yaml').read_text(),Loader=yaml.FullLoader)
        cfg['inference']['batch_size']=1
        cfg.setdefault('training',{})['use_amp']=device=='cuda'
        config=ConfigDict(cfg)
        if name=='scnet':
            from models.scnet import SCNet
            model=SCNet(**config.model)
        elif name=='dttnet':
            from models.DTTNet import DPTDFNet
            model=DPTDFNet(config)
        elif name=='bs_roformer':
            from models.bs_roformer import BSRoformer
            model=BSRoformer(**config.model)
        elif name=='mel_roformer':
            from models.bs_roformer import MelBandRoformer
            model=MelBandRoformer(**config.model)
        else:
            sys.path.insert(0,str(ROOT/'.deps/windowed'))
            from model import MelBandRoformerWSA
            model=MelBandRoformerWSA()
        state=torch.load(ROOT/'.models/separation'/name/'model.ckpt',map_location='cpu',weights_only=True)
        if 'state_dict' in state:state=state['state_dict']
        model.load_state_dict(state,strict=True);del state
        model=model.to(device).eval()
        if name=='windowed':
            # Same non-overlapping 8s chunks as author main.py; no CUDA autocast on CPU.
            def infer(x):
                blocks=[];size=352800
                with torch.inference_mode(),torch.autocast(device_type=device,enabled=device=='cuda'):
                    for start in range(0,x.shape[-1],size):
                        piece=torch.from_numpy(x[:,start:start+size].copy()).to(device)
                        length=piece.shape[-1];piece=torch.nn.functional.pad(piece,(0,size-length))
                        out=model(piece[None])[0,:,:length].float().cpu().numpy()
                        blocks.append(out)
                return np.concatenate(blocks,axis=-1)
        else:
            import utils.model_utils as mu
            # Preserve upstream inference, but reject nonfinite audio instead of hiding it.
            source=inspect.getsource(mu.demix)
            old='np.nan_to_num(estimated_sources, copy=False, nan=0.0)'
            assert old in source
            namespace=dict(vars(mu))
            exec(compile(source.replace(old,'assert np.isfinite(estimated_sources).all(), "nonfinite model output"'),inspect.getfile(mu),'exec'),namespace)
            demix=namespace['demix']
            def infer(x):
                mean=0.;std=1.
                if config.inference.get('normalize',False):
                    mono=x.mean(0);mean=mono.mean();std=mono.std();x=(x-mean)/std
                result=demix(config,model,x,torch.device(device),name,False)['vocals']
                return result*std+mean
    sync(device)
    load_seconds=time.perf_counter()-start
    weights=hashlib.sha256()
    for key,value in sorted(model.state_dict().items()):
        weights.update(key.encode());weights.update(value.detach().cpu().numpy().tobytes())
    identity={'model':name,'device':device,'config':cfg,'parameters':sum(p.numel() for p in model.parameters()),
              'state_sha256':weights.hexdigest(),'model_load_seconds':load_seconds,'load_and_identity_seconds':time.perf_counter()-start,
              'process_import_load_seconds':time.perf_counter()-PROCESS_START}
    return model,infer,identity


if __name__=='__main__':
 parser=argparse.ArgumentParser()
 parser.add_argument('model',choices=['scnet','dttnet','bs_roformer','mel_roformer','windowed'])
 args=parser.parse_args()
 torch.set_num_threads(8)
 assert torch.cuda.is_available()
 model,infer,identity=load(args.model,'cuda')
 dump(OUT/'additional-separation'/f'{args.model}-identity.json',identity)
 for song in songs():
  path=stem_path(song,args.model)
  if path.exists():continue
  x=decode_audio(ROOT/song['audio'],sample_rate=44100,channels=2)
  random.seed(0);np.random.seed(0);torch.manual_seed(0)
  started=time.perf_counter()
  y=infer(x.samples)
  torch.cuda.synchronize()
  assert y.shape==x.samples.shape and np.isfinite(y).all()
  path.parent.mkdir(parents=True,exist_ok=True)
  sf.write(path,y.T,44100,subtype='FLOAT')
  dump(OUT/'additional-separation'/args.model/(song['id']+'.json'),{'song':song['id'],'seconds':time.perf_counter()-started,'stem':str(path),'sha256':hashlib.sha256(y.tobytes()).hexdigest()})
  print(args.model,song['id'],flush=True)

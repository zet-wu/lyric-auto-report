"""In-memory adapters preserving the fixed native separation algorithms.

Only decoding, weight loading, and encoding are moved outside inference. Native
source checkouts and installed packages are never edited.
"""
from common import *
from separator_registry import LEGACY
import hashlib, importlib.util, importlib.metadata, inspect, logging
import numpy as np
import torch

def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def state_identity(model):
    h = hashlib.sha256()
    for key, value in sorted(model.state_dict().items()):
        h.update(key.encode()); h.update(value.detach().cpu().numpy().tobytes())
    return {'parameters': sum(p.numel() for p in model.parameters()), 'state_sha256': h.hexdigest()}

def load(name, device):
    product_imports()
    if name in LEGACY:
        import additional_separators as old
        from lazulite.models.audio import AudioBuffer
        old.AudioBuffer = AudioBuffer
        return old.load(name, device)
    identity = {'model': name, 'device': device}
    for asset in read(ROOT/'configs/separation-models.json'):
        if asset['model']==name:assert digest(ROOT/asset['path'])==asset['sha256'],asset['path']
    if name == 'bs':
        import yaml
        from types import SimpleNamespace
        folder = ROOT / '.deps/timing/models/bs-karaoke'
        assets = read(folder / 'assets.json')
        for path, asset in assets['assets'].items():
            assert digest(folder / path) == asset['sha256'], path
        sys.path.insert(0, str(folder / 'runtime'))
        from models.bs_roformer.bs_roformer import BSRoformer
        import mel_band_roformer.utils as utils
        cfg = yaml.load((folder / 'config_karaoke_frazer_becruily.yaml').read_text(), Loader=yaml.FullLoader)
        config = SimpleNamespace(**{k: SimpleNamespace(**v) for k,v in cfg.items()})
        model = BSRoformer(**cfg['model'])
        weight = folder / 'bs_roformer_karaoke_frazer_becruily.ckpt'
        model.load_state_dict(torch.load(weight, map_location='cpu', weights_only=True), strict=True)
        model.to(device).eval()
        # Native demix_track processes one chunk at a time, irrespective of the
        # unused inference.batch_size=2 field in the published YAML.
        source = inspect.getsource(utils.demix_track)
        assert "torch.amp.autocast('cuda')" in source
        source = source.replace("torch.amp.autocast('cuda')", "torch.amp.autocast('cuda', enabled=device == 'cuda')")
        source = source.replace('np.nan_to_num(estimated_sources, copy=False, nan=0.0)',
                                'assert np.isfinite(estimated_sources).all()')
        ns = dict(vars(utils)); exec(compile(source, inspect.getfile(utils), 'exec'), ns)
        def infer(x):
            return ns['demix_track'](config, model, torch.from_numpy(x.copy()), device)[0]['Vocals']
        identity.update(config=cfg, effective_batch_size=1, weight_sha256=digest(weight))
    elif name == 'yohane':
        spec = importlib.util.spec_from_file_location('frozen_yohane_audio', ROOT / '.deps/comparison/yohane/yohane/audio.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        sep = module.HybridDemucsSeparator(); sep.device = torch.device(device)
        model = sep.bundle.get_model().to(device)
        # The native __call__ also leaves the model in its bundle's default mode.
        def infer(x):
            wave = torch.from_numpy(x.copy()).to(device)
            ref = wave.mean(0); mean = ref.mean(); std = ref.std()
            wave = (wave - mean) / std
            sources = sep.separate_sources(wave[None], 44100, model)[0] * std + mean
            return sources[list(model.sources).index('vocals')].detach().cpu().numpy()
        identity.update(config={'bundle':'HDEMUCS_HIGH_MUSDB_PLUS', 'segment':sep.segment, 'overlap':sep.overlap,
                                'training': model.training},
                        weight_sha256=digest(ROOT / '.models/torch/hub/torchaudio/models/hdemucs_high_trained.pt'))
    else:
        if device == 'cpu':
            assert not torch.cuda.is_available(), 'Launch CPU jobs with CUDA_VISIBLE_DEVICES empty'
        # Enforce CPU thread count in ONNX too; native defaults otherwise create
        # a machine-wide thread pool. Provider choice is verified after loading.
        sessions = []
        if name == 'sug':
            import onnxruntime as ort
            original_session = ort.InferenceSession
            def session(*a, **kw):
                options = kw.get('sess_options') or ort.SessionOptions()
                options.intra_op_num_threads = 8; options.inter_op_num_threads = 1
                kw['sess_options'] = options
                result = original_session(*a, **kw); sessions.append(result)
                return result
            ort.InferenceSession = session
        from audio_separator.separator import Separator
        from audio_separator.separator.uvr_lib_v5 import spec_utils
        weight = (ROOT / '.models/comparison/sug/UVR-MDX-NET-Inst_HQ_3.onnx' if name == 'sug' else
                  ROOT / '.models/milikara-native/separation/model_mel_band_roformer_ep_3005_sdr_11.4360.ckpt')
        sep = Separator(model_file_dir=str(weight.parent), output_dir=str(ROOT / '.cache/separator-adapter'),
                        output_format='WAV', use_autocast=False, log_level=logging.ERROR)
        sep.load_model(model_filename=weight.name)
        native = sep.model_instance
        assert str(native.torch_device).split(':')[0] == device
        if name == 'sug':
            ort.InferenceSession = original_session
            assert sessions
            expected = 'CUDAExecutionProvider' if device == 'cuda' else 'CPUExecutionProvider'
            assert sessions[0].get_providers()[0] == expected, sessions[0].get_providers()
            identity['providers'] = sessions[0].get_providers()
            identity['onnx_threads'] = {'intra':8, 'inter':1}
        captured = {}
        def write_audio(path, source):
            # Keep native output normalization, excluding PCM encoding and I/O.
            normalized = spec_utils.normalize(wave=source, max_peak=native.normalization_threshold,
                                              min_peak=native.amplification_threshold)
            captured[path] = np.asarray(normalized, dtype=np.float32).T.copy()
        native_write = native.write_audio
        native_prepare = native.prepare_mix
        native.write_audio = write_audio
        def infer(x):
            captured.clear()
            native.primary_source = None; native.secondary_source = None
            native.prepare_mix = lambda _: x.copy()
            paths = native.separate('memory.wav')
            paths = [p for p in paths if '(vocals)' in p.lower()]
            assert len(paths) == 1, paths
            output = captured[paths[0]]
            # Native MiliKara only trims/pads the end, never shifts/stretching.
            assert abs(output.shape[-1] - x.shape[-1]) <= 44100
            if output.shape[-1] < x.shape[-1]:
                output = np.pad(output, ((0,0),(0,x.shape[-1]-output.shape[-1])))
            return output[:, :x.shape[-1]]
        model = native.model_run if isinstance(native.model_run, torch.nn.Module) else None
        identity.update(weight_sha256=digest(weight), audio_separator=importlib.metadata.version('audio-separator'),
                        config={k:getattr(native,k,None) for k in ('model_data','segment_size','overlap','batch_size',
                            'normalization_threshold','amplification_threshold','use_autocast','override_model_segment_size')})
    if name in ('sug', 'milikara'):
        def native_file(source, folder):
            import soundfile as sf
            folder.mkdir(parents=True,exist_ok=True)
            native.prepare_mix = native_prepare; native.write_audio = native_write
            native.output_dir = str(folder)
            native.primary_source = None; native.secondary_source = None
            try:
                paths = native.separate(str(source))
                vocal = next(p for p in paths if '(vocals)' in p.lower())
                y, rate = sf.read(folder / vocal, dtype='float32', always_2d=True)
                assert rate == 44100
                return y.T
            finally:
                native.write_audio = write_audio
        def native_check(x, folder):
            import soundfile as sf
            source=folder/'input.wav'
            sf.write(source,x.T,44100,subtype='FLOAT')
            return native_file(source,folder)
        infer.native_check = native_check
        infer.native_file = native_file
    elif name == 'yohane':
        def native_check(x, folder):
            torch.manual_seed(0)
            return sep(torch.from_numpy(x.copy()), 44100)[0].detach().cpu().numpy()
        infer.native_check = native_check
    elif name == 'bs':
        def native_check(x, folder):
            return utils.demix_track(config, model, torch.from_numpy(x.copy()), device)[0]['Vocals']
        infer.native_check = native_check
    if model is not None:
        identity.update(state_identity(model))
    else:
        import onnx, math
        elements = sum(math.prod(t.dims) for t in onnx.load(weight).graph.initializer)
        identity.update(parameters=elements, parameters_basis='onnx_initializer_elements', state_sha256=None)
    return model, infer, identity

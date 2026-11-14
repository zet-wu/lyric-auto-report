"""Stable identities and execution environments for the separator experiment."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MODELS = {
    'demucs': ('Demucs htdemucs', 'research'),
    'scnet': ('SCNet Small', 'research'),
    'dttnet': ('DTTNet', 'research'),
    'bs_roformer': ('BS-RoFormer viperx', 'research'),
    'mel_roformer': ('MelBand RoFormer Kim', 'research'),
    'windowed': ('Windowed RoFormer', 'research'),
    'bs': ('BS Karaoke', 'research'),
    'sug': ('MDX-Net Inst HQ 3', 'sug'),
    'milikara': ('MelBand RoFormer ep_3005', 'milikara'),
    'yohane': ('HybridDemucs MUSDB Plus', 'native5'),
}
LEGACY = tuple(MODELS)[:6]
NEW = tuple(MODELS)[6:]
def interpreter(name):
    return ROOT / '.venvs' / MODELS[name][1] / 'bin/python'

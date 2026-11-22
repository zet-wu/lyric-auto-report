"""Shared repository root, local cache environment, and JSON/gzip I/O helpers."""
from enum import Enum
from pathlib import Path
import gzip, hashlib, json, os, re

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ.update(
    XDG_CACHE_HOME=str(ROOT / '.cache'),
    TORCHINDUCTOR_CACHE_DIR=str(ROOT / '.cache/torchinductor'),
    TRITON_CACHE_DIR=str(ROOT / '.cache/triton'),
    TORCH_HOME=str(ROOT / '.models/torch'),
    HF_HOME=str(ROOT / '.cache/huggingface'),
    NUMBA_CACHE_DIR=str(ROOT / '.cache/numba'),
    MPLCONFIGDIR=str(ROOT / '.cache/matplotlib'),
    NODE_PATH=str(ROOT / '.deps/node/node_modules'),
    PYTHONDONTWRITEBYTECODE='1',
    OMP_NUM_THREADS='8',
)

def portable(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, str):
        value = value.replace(str(ROOT) + '/', '').replace(str((ROOT / 'datasets').resolve().parent) + '/', '')
        value = re.sub(r'/(?:opt)/Miniconda3/', '<python>/', value)
        value = re.sub(r'\x1b\[[0-9;]*m', '', value)
        value = re.sub(r'(?m)^20\d\d-\d\d-\d\d \d\d:\d\d:\d\d(?:\.\d+)? \| ', '', value)
        return value
    if isinstance(value, dict):
        return {portable(k): portable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [portable(v) for v in value]
    return value

def dump(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f'.{os.getpid()}.part')
    temporary.write_text(json.dumps(portable(data), ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8', newline='\n')
    temporary.replace(path)

def read(path):
    path = Path(path)
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    with gzip.open(str(path) + '.gz', 'rt', encoding='utf-8') as f:
        return json.load(f)

def exists(path):
    return Path(path).exists() or Path(str(path) + '.gz').exists()

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def plain_line(text):
    """Remove XML layout whitespace, retaining the lyric's internal spaces."""
    return text.replace('\n', '').replace('\r', '').replace('\t', '').strip()

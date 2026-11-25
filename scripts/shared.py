"""Shared repository root, local cache environment, and JSON/gzip I/O helpers."""
from enum import Enum
from pathlib import Path
import gzip, hashlib, json, os

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
    """Format captured exception text with repository-relative paths."""
    return str(value).replace(str(ROOT) + '/', '')

def _json_default(value):
    if isinstance(value, Enum):
        return value.value
    raise TypeError(f'Not JSON serializable: {type(value).__name__}')

def dump(path, data):
    path = Path(path)
    if path.suffix == '.md':
        raise ValueError('Experiment outputs must be data files')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f'.{os.getpid()}.part')
    text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False, default=_json_default) + '\n'
    if path.name.endswith('.json.gz'):
        with gzip.open(temporary, 'wt', encoding='utf-8', newline='\n') as stream:
            stream.write(text)
    else:
        temporary.write_text(text, encoding='utf-8', newline='\n')
    temporary.replace(path)

def read(path):
    path = Path(path)
    if path.name.endswith('.gz') or not path.exists():
        with gzip.open(path if path.name.endswith('.gz') else Path(str(path) + '.gz'), 'rt', encoding='utf-8') as stream:
            return json.load(stream)
    return json.loads(path.read_text(encoding='utf-8'))

def exists(path):
    return Path(path).exists() or Path(str(path) + '.gz').exists()

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def plain_line(text):
    """Remove XML layout whitespace, retaining the lyric's internal spaces."""
    return text.replace('\n', '').replace('\r', '').replace('\t', '').strip()

"""Store verbose per-condition predictions as deterministic, lossless gzip files."""
from pathlib import Path
import gzip, json

ROOT = Path(__file__).resolve().parents[1]
count = before = after = 0
folders=[ROOT/'results'/group/'predictions' for group in ('ablation','milikara','separation-alignment')]
folders.append(ROOT/'results/milikara-native/runs')
for folder in folders:
    for source in sorted(folder.rglob('*.json')):
        raw = source.read_bytes()
        target = source.with_suffix('.json.gz')
        packed = gzip.compress(raw, compresslevel=9, mtime=0)
        assert json.loads(gzip.decompress(packed)) == json.loads(raw)
        temporary = target.with_suffix('.gz.part')
        temporary.write_bytes(packed)
        temporary.replace(target)
        source.unlink()
        count += 1
        before += len(raw)
        after += len(packed)
print(f'Packed {count} predictions: {before / 1048576:.2f} -> {after / 1048576:.2f} MiB')

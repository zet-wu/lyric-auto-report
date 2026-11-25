"""Import the 26-song corpus and prepare CPU-only Phase 2 inputs."""
import argparse
import shutil
from shared import ROOT, dump, sha
from timing.prepare import prepare_dataset
from reading.prepare import prepare

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_root', type=__import__('pathlib').Path)
    args = parser.parse_args()
    audio = sorted((args.dataset_root / 'audio').glob('*.m4a'))
    ttml = sorted((args.dataset_root / 'TTML').glob('*.ttml'))
    expected = {f'j{i:02}' for i in range(1, 21)} | {'m01', 'm02', 'y01', 'y02', 'jy01', 't01'}
    for paths in (audio, ttml):
        if len(paths) != 26 or {p.stem.split(' - ', 1)[0] for p in paths} != expected:
            raise ValueError('Expected exactly the 26 Phase 2 song IDs')
    if {p.stem for p in audio} != {p.stem for p in ttml}:
        raise ValueError('Audio and annotation filenames do not match')
    backup = ROOT / '.runs/phase1'
    if not backup.exists():
        backup.mkdir(parents=True)
        for name in ('results', '.cache'):
            source = ROOT / name
            if source.exists():
                source.rename(backup / name.lstrip('.'))
    for dirname, paths in [('audio', audio), ('annotations', ttml)]:
        dest = ROOT / 'datasets' / dirname
        dest.mkdir(parents=True, exist_ok=True)
        names = {p.name for p in paths}
        for old in dest.iterdir():
            if old.is_file() and old.suffix in ('.m4a', '.ttml') and old.name not in names:
                old.unlink()
        for path in paths:
            shutil.copy2(path, dest / path.name)
    dump(ROOT / 'configs/dataset-ids.json', {p.name: p.stem.split(' - ', 1)[0] for p in ttml})
    manifest = []
    for dirname in ('audio', 'annotations'):
        for path in sorted((ROOT / 'datasets' / dirname).iterdir()):
            if path.suffix in ('.m4a', '.ttml'):
                manifest.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    dump(ROOT / 'datasets/files.json', manifest)
    prepare_dataset(ROOT / 'results/timing', ROOT / '.cache/timing')
    prepare()
    print('Imported 26 song pairs and prepared 20 Japanese text inputs.')

if __name__ == '__main__':
    main()

"""Prepare native Studio dictionary readings without alignment inference."""
import argparse
import shutil
import sys
import zipfile
from pathlib import Path
from shared import ROOT, read, dump, sha, plain_line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('packages', type=Path, help='Directory containing the native dictionary ZIPs')
    args = parser.parse_args()
    sys.path[:0] = [str(ROOT / '.deps/comparison/studio'), str(ROOT / '.deps/comparison/lazulite/src')]
    from server.dictionary_engine import DictionaryIndex
    refs = {song['id']: song for song in read(ROOT / 'results/timing/reference.json')}
    config = read(ROOT / 'configs/phase2.json')['modules']['M2']['dictionary_songs']
    assets = []
    for name, ids in config.items():
        matches = sorted(args.packages.glob(name + '-*.zip'))
        if len(matches) != 1:
            raise ValueError(f'Expected exactly one {name} dictionary package')
        archive = matches[0]
        folder = ROOT / '.models/dictionaries' / archive.stem
        folder.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive) as package:
            for item in package.infolist():
                path = Path(item.filename)
                if path.is_absolute() or '..' in path.parts:
                    raise ValueError('Unsafe package member')
                if item.is_dir() or path.suffix.lower() == '.md':
                    continue
                target = folder / path
                target.parent.mkdir(parents=True, exist_ok=True)
                with package.open(item) as source, target.open('wb') as dest:
                    shutil.copyfileobj(source, dest)
        index = DictionaryIndex(folder, installed=True)
        assets.append({'dictionary': name, 'version': index.manifest['version'], 'sha256': sha(archive),
                       'path': folder.relative_to(ROOT).as_posix(), 'songs': ids})
        for sid in ids:
            song = refs[sid]
            lines = [{'id': line['id'], 'text': plain_line(line['text'])} for line in song['lines']]
            proposals = index.snapshot(lines)
            dump(ROOT / 'results/M2/dictionary/inputs' / f'{sid}.json.gz',
                 {'song': sid, 'dictionary': name, 'version': index.manifest['version'],
                  'lines': lines, 'proposals': proposals})
            print(name, sid, len(proposals), flush=True)
    dump(ROOT / 'configs/dictionaries.json', assets)


if __name__ == '__main__':
    main()

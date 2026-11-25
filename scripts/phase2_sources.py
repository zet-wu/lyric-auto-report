"""Fetch configured source commits without editing upstream files."""
import argparse
import subprocess
from shared import ROOT, read

def checkout(folder, item, local=None):
    if not (folder / '.git').exists():
        folder.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'init', str(folder)], check=True)
    dirty = subprocess.check_output(['git', '-C', str(folder), 'status', '--porcelain', '--untracked-files=no'], text=True)
    if dirty.strip():
        raise RuntimeError(f'Upstream has local modifications: {folder.relative_to(ROOT)}')
    available = subprocess.run(['git', '-C', str(folder), 'cat-file', '-e', item['commit'] + '^{commit}'], capture_output=True).returncode == 0
    if not available:
        subprocess.run(['git', '-C', str(folder), 'fetch', '--depth', '1', str((ROOT / local).resolve()) if local else item['url'], item['commit']], check=True)
    subprocess.run(['git', '-C', str(folder), 'checkout', '--detach', item['commit']], check=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--studio', help='Optional local Studio repository')
    parser.add_argument('--lazulite', help='Optional local Lazulite repository')
    args = parser.parse_args()
    for config, base in [('sources', ROOT / '.deps'), ('comparison-sources', ROOT / '.deps/comparison')]:
        for name, item in read(ROOT / f'configs/{config}.json').items():
            checkout(base / name, item, getattr(args, name, None))

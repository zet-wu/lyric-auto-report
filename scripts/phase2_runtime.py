"""Update CPU dependencies required by the newly pinned Studio interfaces."""
import subprocess
from shared import ROOT

if __name__ == '__main__':
    python = ROOT / '.venvs/research/bin/python'
    subprocess.run([str(python), '-m', 'pip', 'install', 'msgspec==0.19.0', 'beartype==0.23.1'], check=True, cwd=ROOT)

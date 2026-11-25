"""Update native runtime overlays required by the pinned upstream interfaces."""
import os
import subprocess
import sys
from pathlib import Path
from shared import ROOT


def overlay(name,parents):
    target=ROOT/'.venvs'/name
    if not (target/'bin/python').exists():
        subprocess.run([str(ROOT/'.venvs/research/bin/python'),'-m','venv','--without-pip',str(target)],check=True)
    version=f'python{sys.version_info.major}.{sys.version_info.minor}'
    site=target/'lib'/version/'site-packages'
    (site/'shared-runtime.pth').write_text(''.join(str(ROOT/'.venvs'/parent/'lib'/version/'site-packages')+'\n' for parent in parents))
    return target/'bin/python'


def main():
    python=ROOT/'.venvs/research/bin/python'
    env=dict(os.environ,PIP_CACHE_DIR=str(ROOT/'.cache/pip'))
    subprocess.run([str(python),'-m','pip','install','msgspec==0.19.0','beartype==0.23.1'],check=True,env=env,cwd=ROOT)
    yohane=overlay('yohane',['native5','research'])
    subprocess.run([str(python),'-m','pip','--python',str(yohane),'install','torch==2.15.0','torchaudio==2.11.1','torchcodec==0.17.0'],check=True,env=env,cwd=ROOT)


if __name__=='__main__':main()

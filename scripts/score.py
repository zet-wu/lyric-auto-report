"""Recompute metrics and static tables without downloading model weights."""
from pathlib import Path
import subprocess,sys,os
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
for script in ('timing/metrics.py','timing/ablation_score.py','timing/ablation_tables.py','milikara/evaluate.py','milikara/score_separation.py'):
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],check=True,cwd=ROOT)

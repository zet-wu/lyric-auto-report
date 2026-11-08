"""Recompute metrics and static tables without downloading model weights."""
from pathlib import Path
import subprocess,sys,os
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
for script in ('timing/metrics.py','timing/ablation_score.py','timing/ablation_tables.py','timing/mms_gap_fill.py','milikara/evaluate.py','milikara/score_separation.py','milikara/score_local.py','milikara/score_native.py','reading/score.py'):
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],check=True,cwd=ROOT)

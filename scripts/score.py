"""Recompute metrics and static figures without downloading model weights."""
from pathlib import Path
import subprocess, sys, os
ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
if (ROOT / 'configs/phase2.json').exists():
    raise SystemExit('The historical Phase 1 scorer is disabled for Phase 2. The M1-M9 score/index integration is not implemented yet.')
for script in (
    'timing/metrics.py',
    'timing/ablation_score.py',
    'timing/ablation_tables.py',
    'timing/mms_gap_fill.py',
    'milikara/evaluate.py',
    'milikara/score_separation.py',
    'milikara/score_local.py',
    'reading/score.py',
    'comparison/score.py',
    'comparison/score_reading.py',
    'comparison/score_studio.py',
):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], check=True, cwd=ROOT)

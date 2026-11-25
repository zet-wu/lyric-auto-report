"""Reproduce the research in dependency order; results and caches are repository-local."""
from pathlib import Path
import argparse, json, os, subprocess, sys
from shared import ROOT

os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')

if (ROOT / 'configs/phase2.json').exists():
    raise SystemExit('This runner is the historical Phase 1 matrix. Phase 2 preparation uses phase2_prepare.py, phase2_sources.py and phase2_runtime.py; the Phase 2 GPU matrix is not enabled yet.')

groups = {
    'prepare': [
        ('timing/prepare.py',),
        ('timing/baseline.py',),
        ('timing/controlled.py',),
        ('timing/english.py',),
        ('timing/yue_native.py',),
        ('timing/ablation_prepare.py',),
    ],
    'separate': [('timing/ablation_separate.py', x) for x in ('bs', 'kim')],
    'matrix': (
        [('timing/ablation_run.py', 'audio')]
        + [('timing/ablation_run.py', x) for x in ('mms', 'nextfire', 'tifa', 'mms_fa')]
        + [('timing/ablation_product.py',), ('timing/ablation_pause.py',)]
        + [('timing/ablation_run.py', x, '--strategies', 'auto_mms_pause') for x in ('nextfire', 'tifa', 'mms_fa')]
        + [('timing/ablation_hold_probe.py',), ('timing/ablation_score.py',), ('timing/ablation_tables.py',)]
    ),
    'pipeline': [('timing/run_timing.py',), ('timing/run_timing.py', '--modes', 'lead_untimed'), ('timing/hybrid.py',), ('timing/metrics.py',)],
    'milikara': [
        ('milikara/prepare_inputs.py',),
        ('milikara/prepare_audio.py',),
        ('milikara/prepare_anchors.py',),
        ('milikara/run_factorial.py',),
        ('milikara/run_text.py',),
        ('milikara/run_context.py',),
        ('milikara/run_runner.py',),
        ('milikara/run_calibration.py',),
        ('milikara/run_audio.py',),
        ('milikara/run_original_controls.py',),
        ('milikara/evaluate.py',),
    ],
    'reading': [('reading/prepare.py',), ('reading/local.py',), ('reading/sug.py',), ('reading/reuse_llm.py',), ('reading/score.py',)],
    'local-refinement': [('milikara/local_refinement.py',), ('milikara/score_local.py',)],
    'mms-gap-fill': [('timing/mms_gap_fill.py',)],
    'comparison': [('comparison/run_all.py',)],
    'additional': (
        [('timing/additional_separators.py', model) for model in ('scnet', 'dttnet', 'bs_roformer', 'mel_roformer', 'windowed')]
        + [('timing/ablation_run.py', stage, '--separators', 'scnet', 'dttnet', 'bs_roformer', 'mel_roformer', 'windowed', '--strategies', 'concat', 'padded', 'full') for stage in ('audio', 'nextfire')]
        + [('timing/ablation_score.py',), ('timing/ablation_tables.py',)]
    ),
    'separation-alignment': [('timing/separation_stems.py', name) for name in ('bs', 'sug', 'milikara', 'yohane')] + [('milikara/run_separation.py',), ('milikara/score_separation.py',)],
    'resources': [('timing/resource_benchmark.py', model, str(repeat)) for repeat in (1, 2) for model in ('demucs', 'bs', 'kim')] + [('timing/separation_suite.py',), ('milikara/score_separation.py',)],
}

parser = argparse.ArgumentParser()
parser.add_argument('stage', choices=[*groups, 'all'])
parser.add_argument('--start-at', help='Resume at a script basename within the selected stage')
parser.add_argument('--fresh', action='store_true', help='For all: move existing results/cache into an ignored numbered backup and rerun')
args = parser.parse_args()
if args.fresh:
    if args.stage != 'all' or args.start_at:
        parser.error('--fresh requires all without --start-at')
    backups = ROOT / '.runs'; backups.mkdir(exist_ok=True)
    number = 1
    while (backups / f'run-{number:03}').exists():
        number += 1
    backup = backups / f'run-{number:03}'; backup.mkdir()
    for name in ('results', '.cache'):
        source = ROOT / name
        if source.exists():
            source.rename(backup / name.lstrip('.'))
    (ROOT / '.cache').mkdir(exist_ok=True)
    (ROOT / '.cache/reading-reuse.json').write_text(json.dumps({'source': str((backup / 'results/reading').relative_to(ROOT))}))
    print('Previous outputs saved in', backup.relative_to(ROOT), flush=True)
elif args.stage == 'all' and (ROOT / 'results/timing/baseline').exists() and not (ROOT / '.cache/timing/audio').exists():
    parser.error('Published predictions have no acoustic cache. Use all --fresh to regenerate inference, or scripts/score.py to rescore.')

started = args.start_at is None
logdir = ROOT / '.cache/logs'; logdir.mkdir(parents=True, exist_ok=True)
for group in groups if args.stage == 'all' else [args.stage]:
    for index, task in enumerate(groups[group]):
        if not started:
            if Path(task[0]).stem != args.start_at:
                continue
            started = True
        print('RUN', group, *task, flush=True)
        path = logdir / f'{group}-{index:02}-{Path(task[0]).stem}.log'
        with path.open('w') as stream:
            interpreter = str(ROOT / '.venvs/sug/bin/python') if task[0] == 'reading/sug.py' else sys.executable
            if task[0] == 'timing/separation_stems.py':
                runtime = {'bs': 'research', 'sug': 'sug', 'milikara': 'milikara', 'yohane': 'native5'}[task[1]]
                interpreter = str(ROOT / '.venvs' / runtime / 'bin/python')
            subprocess.run([interpreter, str(ROOT / 'scripts' / task[0]), *task[1:]], check=True, stdout=stream, stderr=subprocess.STDOUT, cwd=ROOT)
        print('DONE', group, *task, flush=True)

if not started:
    raise SystemExit('Unknown script in this stage: ' + args.start_at)

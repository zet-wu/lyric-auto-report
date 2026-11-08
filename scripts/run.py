"""Reproduce the research in dependency order; results and caches are repository-local."""
from pathlib import Path
import argparse, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ.update(XDG_CACHE_HOME=str(ROOT/'.cache'),TORCHINDUCTOR_CACHE_DIR=str(ROOT/'.cache/torchinductor'),TRITON_CACHE_DIR=str(ROOT/'.cache/triton'),TORCH_HOME=str(ROOT/'.models/torch'),HF_HOME=str(ROOT/'.cache/huggingface'),
    NUMBA_CACHE_DIR=str(ROOT/'.cache/numba'),MPLCONFIGDIR=str(ROOT/'.cache/matplotlib'),
    NODE_PATH=str(ROOT/'.deps/node/node_modules'),PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='8',
    HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
groups={
 'prepare': [('timing/prepare.py',),('timing/baseline.py',),('timing/import_audit.py',),
             ('timing/controlled.py',),('timing/english.py',),('timing/yue_native.py',),('timing/ablation_prepare.py',)],
 'separate': [('timing/ablation_separate.py',x) for x in ('bs','kim')],
 'matrix': [('timing/ablation_run.py','audio')]+[
     ('timing/ablation_run.py',x) for x in ('mms','nextfire','tifa','mms_fa')]+
     [('timing/ablation_product.py',),('timing/ablation_pause.py',)]+
     [('timing/ablation_run.py',x,'--strategies','auto_mms_pause') for x in ('nextfire','tifa','mms_fa')]+
     [('timing/ablation_hold_audit.py',),('timing/ablation_hold_probe.py',),('timing/ablation_score.py',),('timing/ablation_window_audit.py',),('timing/ablation_tables.py',)],
 'pipeline': [('timing/run_timing.py',),('timing/run_timing.py','--modes','lead_untimed'),('timing/hybrid.py',),('timing/metrics.py',)],
 'milikara': [('milikara/prepare_inputs.py',),('milikara/prepare_audio.py',),('milikara/validate_real.py',),('milikara/prepare_anchors.py',),
              ('milikara/run_factorial.py',),('milikara/run_text.py',),('milikara/run_context.py',),
              ('milikara/run_runner.py',),('milikara/run_calibration.py',),('milikara/run_audio.py',),
              ('milikara/run_original_controls.py',),('milikara/prepare_auto.py',),('milikara/run_auto.py',),
              ('milikara/auto_iteration.py','--resume'),('milikara/auto_iteration.py','--gpu','--resume'),
              ('milikara/auto_self_fresh.py',),('milikara/export_iterations.py',),('milikara/evaluate.py',)],
 'additional': [('timing/additional_separators.py',model) for model in ('scnet','dttnet','bs_roformer','mel_roformer','windowed')]+[
     ('timing/ablation_run.py',stage,'--separators','scnet','dttnet','bs_roformer','mel_roformer','windowed','--strategies','concat','padded','full')
     for stage in ('audio','nextfire')]+[('timing/ablation_score.py',),('timing/ablation_tables.py',)],
 'separation-alignment': [('milikara/run_separation.py',),('milikara/score_separation.py',)],
 'resources': [('timing/resource_benchmark.py', model, str(repeat)) for repeat in (1,2) for model in ('demucs','bs','kim')],
}
parser=argparse.ArgumentParser()
parser.add_argument('stage',choices=[*groups,'all'])
parser.add_argument('--start-at',help='Resume at a script basename within the selected stage')
parser.add_argument('--fresh',action='store_true',help='For all: move existing results/cache into an ignored numbered backup and rerun')
args=parser.parse_args()
if args.fresh:
    if args.stage!='all' or args.start_at:parser.error('--fresh requires all without --start-at')
    backups=ROOT/'.runs';backups.mkdir(exist_ok=True)
    number=1
    while (backups/f'run-{number:03}').exists():number+=1
    backup=backups/f'run-{number:03}';backup.mkdir()
    for name in ('results','.cache'):
        source=ROOT/name
        if source.exists():source.rename(backup/name.lstrip('.'))
    print('Previous outputs saved in',backup.relative_to(ROOT),flush=True)
elif args.stage=='all' and (ROOT/'results/timing/baseline').exists() and not (ROOT/'.cache/timing/audio').exists():
    parser.error('Published predictions have no acoustic cache. Use all --fresh to regenerate inference, or scripts/score.py to rescore.')
started=args.start_at is None
logdir=ROOT/'.cache/logs';logdir.mkdir(parents=True,exist_ok=True)
for group in groups if args.stage=='all' else [args.stage]:
    for index,task in enumerate(groups[group]):
        if not started:
            if Path(task[0]).stem!=args.start_at:continue
            started=True
        print('RUN',group,*task,flush=True)
        path=logdir/f'{group}-{index:02}-{Path(task[0]).stem}.log'
        with path.open('w') as stream:
            subprocess.run([sys.executable,str(ROOT/'scripts'/task[0]),*task[1:]],check=True,
                           stdout=stream,stderr=subprocess.STDOUT,cwd=ROOT)
        print('DONE',group,*task,flush=True)

if not started:raise SystemExit('Unknown script in this stage: '+args.start_at)

"""Run Phase 2 partitions serially after the Stage 0 GPU confirmation."""
import argparse
import os
import re
import subprocess
from shared import ROOT, read, dump, exists, portable
from phase2_jobs import build_jobs


def failure_outputs(job, detail):
    matches = list(re.finditer(r'([\w.]+(?:Error|Exception)):\s*([^\n]+)', detail))
    match = matches[-1] if matches else None
    error = {'type':match.group(1) if match else 'SubprocessError','message':portable(match.group(2) if match else detail[-800:])[:800]}
    for index, relative in enumerate(job['outputs']):
        path = ROOT / relative
        if exists(path):
            record = read(path)
            if record.get('status') == 'ok':
                continue
        else:
            record = {}
        record.update(status='failed', error=error, failed_stage='worker_execution', job=job['id'])
        if path.name.split('.')[0] in job['songs']:
            record['song'] = path.name.split('.')[0]
        elif len(job['outputs']) == len(job['songs']):
            record['song'] = job['songs'][index]
        dump(path, record)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['prepare','matrix','score','all','list','gpu-benchmarks'])
    parser.add_argument('--gpu-confirmed', action='store_true', help='Use only after the user confirms the completed Stage 0 handoff')
    parser.add_argument('--start-at')
    args = parser.parse_args()
    if args.stage == 'prepare':
        subprocess.run([str(ROOT/'.venvs/research/bin/python'),str(ROOT/'scripts/phase2_inputs.py')],check=True,cwd=ROOT)
        return
    if args.stage == 'score':
        subprocess.run([str(ROOT/'.venvs/research/bin/python'),str(ROOT/'scripts/score.py')],check=True,cwd=ROOT)
        return
    jobs, views = build_jobs()
    if args.stage == 'list':
        for job in jobs:print(job['id'],job['runtime'],len(job['songs']),job.get('execution','automatic'))
        return
    if not args.gpu_confirmed:
        parser.error('Complete Stage 0 and obtain user confirmation before GPU batch inference')
    if args.stage=='gpu-benchmarks':
        jobs=[job for job in jobs if job['kind']=='benchmark' and job.get('device')=='cuda']
    else:
        jobs=[job for job in jobs if job.get('execution')!='manual']
    logs = ROOT/'.cache/phase2/logs'; logs.mkdir(parents=True,exist_ok=True)
    started = args.start_at is None
    for job in jobs:
        if not started:
            started = job['id']==args.start_at
            if not started:continue
        env = dict(os.environ,PHASE2_SONGS=','.join(job['songs']),PYTHONDONTWRITEBYTECODE='1')
        log = logs/(job['id']+'.log')
        print('RUN',job['id'],flush=True)
        with log.open('w') as stream:
            process = subprocess.run([str(ROOT/'.venvs'/job['runtime']/'bin/python'),str(ROOT/'scripts'/job['script']),*job['args']],cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT)
        if process.returncode:
            failure_outputs(job,log.read_text(errors='replace'))
            print('FAILED',job['id'],'see',log.relative_to(ROOT),flush=True)
        else:print('DONE',job['id'],flush=True)
    if not started:parser.error('Unknown --start-at partition')
    if args.stage == 'all':
        subprocess.run([str(ROOT/'.venvs/research/bin/python'),str(ROOT/'scripts/score.py'),'--allow-missing-winrt','--allow-pending-gpu-benchmarks'],check=True,cwd=ROOT)


if __name__ == '__main__':main()

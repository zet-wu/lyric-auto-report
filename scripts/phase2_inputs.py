"""Prepare all native app inputs before any GPU inference."""
import os
import subprocess
import sys
from shared import ROOT, read, dump, portable


def main():
    songs = read(ROOT / 'results/timing/reference.json')
    dump(ROOT / 'results/comparison/reference.json.gz', songs)
    for song in songs:
        dump(ROOT / '.cache/comparison/inputs' / f"{song['id']}-studio.json", read(ROOT / '.cache/timing/inputs' / f"{song['id']}-studio.json"))
    env = dict(os.environ, PHASE2_SONGS=','.join(song['id'] for song in songs))
    python = ROOT / '.venvs/research/bin/python'
    for script in ('prepare_milikara.py', 'prepare_studio.py'):
        subprocess.run([str(python), str(ROOT / 'scripts/comparison' / script)], check=True, env=env, cwd=ROOT)
    front = ROOT / '.deps/comparison/studio/frontend'
    build = next((front / 'node_modules/.pnpm').glob('esbuild@*/node_modules/esbuild/bin/esbuild'))
    env['NODE_PATH'] = str(front / 'node_modules')
    for script, action in [('studio_frontend.ts', 'prepare'), ('romanize.ts', None)]:
        output = ROOT / '.cache/comparison' / (script + '.cjs')
        subprocess.run([str(build), str(ROOT / 'scripts/comparison' / script), '--bundle', '--platform=node', '--format=cjs', '--packages=external', '--external:../../.deps/comparison/studio/frontend/node_modules/jsdom/lib/api.js', '--outfile=' + str(output)], check=True, env=env, cwd=ROOT)
        subprocess.run(['node', str(output), *([action] if action else [])], check=True, env=env, cwd=ROOT)
    subprocess.run([str(python), str(ROOT / 'scripts/milikara/prepare_inputs.py')], check=True, cwd=ROOT)
    sys.path[:0]=[str(ROOT/'.deps/comparison/studio'),str(ROOT/'.deps/comparison/lazulite/src')]
    from server.alignment_projection import project_alignment
    from lazulite.alignment.japanese.backend import MMS_VOCAB
    from phase2_native import snapshot_for
    vocab=read(ROOT/'.models/nextfire/vocab.json');blank=read(ROOT/'.models/nextfire/config.json')['pad_token_id']
    models={'nextfire':{'vocabulary':vocab,'blank':blank},'mms-fa':{'vocabulary':MMS_VOCAB,'blank':0}}
    count=failed=0
    for song in songs:
        sid=song['id']
        conditions=['manual']+(['auto'] if sid in read(ROOT/'configs/reading.json')['songs'] else [])+(['dictionary'] if sid in ('m01','m02','y01','y02','t01') else [])
        for condition in conditions:
            for model,options in models.items():
                target=ROOT/'.cache/phase2/projections'/f'{sid}-{condition}-{model}.json.gz'
                try:
                    projection=project_alignment(snapshot_for(sid,condition),False,model=options,strip_tone_digits=sid in ('y01','y02','jy01'))
                    record={'status':'ok','projection':projection};count+=1
                except Exception as exc:
                    record={'status':'failed','error':{'type':type(exc).__name__,'message':portable(exc)[:800]}};failed+=1
                dump(target,record)
    print(f'Prepared {count} native model inputs; {failed} explicit input failures.')



if __name__ == '__main__':
    main()

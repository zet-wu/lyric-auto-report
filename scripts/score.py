"""Rebuild Phase 2 metrics and the data index; never run model inference."""
import argparse
import subprocess
from shared import ROOT, read, dump, exists
from phase2_jobs import build_jobs
from phase2_metrics import publish,table,score_alignment_modules
from phase2_analysis import m2,m3,m4,m5,m7,m8


def score_reading(allow_missing):
    command=[str(ROOT/'.venvs/research/bin/python'),str(ROOT/'scripts/reading/score.py')]
    if allow_missing:command.append('--allow-missing-winrt')
    subprocess.run(command,check=True,cwd=ROOT)
    summary=read(ROOT/'results/reading/summary.json')
    publish('M9',summary,summary['metrics'])
    return summary


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--allow-missing-winrt',action='store_true')
    parser.add_argument('--reading-only',action='store_true')
    parser.add_argument('--allow-pending-gpu-benchmarks',action='store_true',help='Publish completed experiments while the operator-run GPU resource benchmark is pending')
    args=parser.parse_args()
    reading=score_reading(args.allow_missing_winrt)
    if args.reading_only:return
    config=read(ROOT/'configs/phase2.json');jobs,views=build_jobs()
    pending_gpu=[job for job in jobs if job['kind']=='benchmark' and job.get('device')=='cuda' and any(not exists(ROOT/path) for path in job['outputs'])]
    allowed={path for job in pending_gpu for path in job['outputs']} if args.allow_pending_gpu_benchmarks else set()
    missing=[relative for job in jobs for relative in job['outputs'] if relative not in allowed and not exists(ROOT/relative)]
    if missing:raise FileNotFoundError(f'{len(missing)} planned experiment outputs are missing; first: {missing[0]}')
    refs={song['id']:song for song in read(ROOT/'results/timing/reference.json')}
    native,datasets,states=score_alignment_modules(config,jobs,views,refs)
    m2(config,refs,datasets['M2']);m3(native,config)
    source_map={'G1-studio-demucs-nextfire':'demucs-nextfire','G1-studio-bs-nextfire':'bs-nextfire','G1-studio-demucs-mms_fa-smart':'demucs-mms-fa','G2-studio-demucs-mms_fa-smart':'bs-mms-fa'}
    m4_rows=[dict(row,condition=source_map[row['condition']]) for row in datasets['M1'] if row['condition'] in source_map]
    m4_rows += [row for row in datasets['M2'] if row['condition'] in ('demucs-nextfire','bs-nextfire','demucs-mms-fa','bs-mms-fa')]
    m4(config,refs,m4_rows);m5(config);m7(config);m8(config,refs)
    dictionaries=read(ROOT/'results/M2/dictionary/summary.json')
    summary=read(ROOT/'results/M2/summary.json');summary['dictionary_reading']=dictionaries
    paired=[]
    for sep in ('demucs','bs'):
        for sid in ('m01','m02','y01','y02','t01'):
            conditions={row['condition']:row for row in summary['surface'] if row['song']==sid and row['scope']=='all'}
            human=conditions.get(sep+'-mms-fa');automatic=conditions.get(sep+'-dictionary-mms-fa')
            if human and automatic:
                paired.append({'separator':sep,'song':sid,**{name+'_delta_auto_minus_human':automatic[name]-human[name] if automatic[name] is not None and human[name] is not None else None for name in ('hit100_pct','start_mae_ms','end_mae_ms')}})
    summary['dictionary_alignment_change']=paired;dump(ROOT/'results/M2/summary.json',summary);table(ROOT/'results/M2/dictionary/alignment-change.csv',paired)
    index={'dataset':[],'sources':{**read(ROOT/'configs/sources.json'),**read(ROOT/'configs/comparison-sources.json')},'modules':{},'stage':'interim' if reading['missing_methods'] or pending_gpu else 'complete','missing_reading_methods':reading['missing_methods'],'pending_gpu_benchmarks':[{'id':job['id'],'songs':job['songs'],'outputs':job['outputs']} for job in pending_gpu]}
    import json,subprocess
    for sid,song in refs.items():
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=sample_rate','-of','json',str(ROOT/song['audio'])]))
        index['dataset'].append({'id':sid,'audio':song['audio'],'annotation':song['ttml'],'language_group':'ja' if sid in config['dataset']['ja'] else 'mixed_ja_yue' if sid=='jy01' else 'cmn' if sid.startswith('m') else 'teochew' if sid=='t01' else 'yue','duration':song['duration'],'sample_rate':int(probe['streams'][0]['sample_rate']),'lines':len(song['lines']),'reference_units':sum(leaf['start'] is not None and leaf['end'] is not None and leaf['end']>leaf['start'] and any(char.isalnum() for char in leaf['text']) for line in song['lines'] for leaf in line['leaves']),'has_overlap':bool(song['background_intervals'])})
    for module in config['modules']:
        summary=read(ROOT/'results'/module/'summary.json')
        failures=[state for state in summary.get('completion',[]) if state['status'] in ('failed','unsupported')]
        index['modules'][module]={'summary':f'results/{module}/summary.json','metrics':f'results/{module}/metrics.csv','songs':config['modules'][module]['songs'],'fields':config['modules'][module]['field_descriptions'],'status':'pending_gpu_benchmarks' if module=='M5' and pending_gpu else 'waiting_for_winrt' if module=='M9' and reading['missing_methods'] else 'complete_with_failures' if failures else 'complete','failed_or_unsupported':failures,'additional_data':[path.relative_to(ROOT).as_posix() for path in sorted((ROOT/'results'/module).glob('*')) if path.is_file() and path.name not in ('summary.json','metrics.csv')]}
    dump(ROOT/'results/EXPERIMENT_INDEX.json',index)
    print('Rebuilt M1-M9 summaries and results/EXPERIMENT_INDEX.json ('+index['stage']+').')


if __name__=='__main__':main()

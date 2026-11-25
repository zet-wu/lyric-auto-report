"""Build the finite Phase 2 execution matrix, without running inference."""
from shared import ROOT, read, dump


def build_jobs():
    config = read(ROOT / 'configs/phase2.json'); ja = config['dataset']['ja']; other = config['dataset']['non_ja']; all_songs = ja + other
    jobs = []
    def add(key, module, script, args, songs, runtime='research', outputs=None, **metadata):
        jobs.append({'id':key,'module':module,'script':script,'args':list(map(str,args)),'songs':songs,'runtime':runtime,'outputs':outputs or [],**metadata})
    for model in config['modules']['M5']['models']:
        songs = all_songs if model in ('demucs','bs','sug','milikara','yohane') else ja
        add('separate-'+model,'M5','phase2_separate.py',[model,'--songs',*songs],songs,
            {'sug':'sug','milikara':'milikara','yohane':'yohane'}.get(model,'research'),
            [f'results/M5/separation/{model}/{sid}.json.gz' for sid in songs],kind='separation',separator=model)
    def native(module, name, songs, sep='demucs', backend='nextfire', condition='manual', mode='core', audio_format='float', smart=False):
        folder=f'results/{module}/predictions/{name}'
        args=['--separator',sep,'--backend',backend,'--condition',condition,'--mode',mode,'--audio-format',audio_format,'--songs',*songs,'--output-dir',folder]
        if smart:args+=['--smart']
        add(module+'-'+name,module,'phase2_native.py',args,songs,outputs=[f'{folder}/{sid}.json.gz' for sid in songs],kind='native',condition=name,separator=sep,backend=backend,input_condition=condition,mode=mode,audio_format=audio_format,smart=smart)
    def external(module,name,songs,tool,sep,condition='manual'):
        runtime={'milikara':'milikara','timing':'native5','sug':'sug','yohane':'yohane','fa-kara':'fakara'}[tool]
        script={'fa-kara':'run_fakara','milikara':'run_milikara','timing':'run_timing','sug':'run_sug','yohane':'run_yohane'}[tool]
        args=['--sep',sep,'--condition',condition]
        model='-nextfire' if tool=='sug' else ''
        folder='milikara/runs' if tool=='milikara' else tool
        outputs=[f'results/comparison/{folder}/{sid}-{sep}{model}-{condition}.json.gz' for sid in songs]
        # The same native export serves multiple module views; infer it once.
        key='external-'+tool+'-'+sep+'-'+condition
        existing=next((job for job in jobs if job['id']==key),None)
        if existing:
            for sid,path in zip(songs,outputs):
                if sid not in existing['songs']:existing['songs'].append(sid);existing['outputs'].append(path)
        else:
            add(key,module,'comparison/'+script+'.py',args,songs[:],runtime,outputs,kind='external',tool=tool,separator=sep,input_condition=condition)
        return {'job':key,'module':module,'condition':name,'songs':songs,'tool':tool,'separator':sep,'input_condition':condition}
    views=[]
    routes=[('studio-demucs-nextfire','demucs','nextfire',False),('studio-bs-nextfire','bs','nextfire',False),('studio-demucs-mms_fa-smart','demucs','mms-fa',True)]
    for group in ('G1','G2','G3'):
        for route,sep,backend,smart in routes:
            native('M1',group+'-'+route,ja,sep='bs' if group=='G2' else sep,backend=backend,smart=smart,condition='auto' if group=='G3' else 'manual')
        for tool,own in [('fa-kara','bs'),('sug','sug'),('milikara','milikara'),('timing','bs'),('yohane','yohane')]:
            views.append(external('M1',group+'-'+tool,ja,tool,'bs' if group=='G2' else own,'auto' if group=='G3' else 'manual'))
    for sep in ('demucs','bs'):
        for backend in ('nextfire','mms-fa'):
            native('M2',f'{sep}-{backend}',other,sep=sep,backend=backend,smart=backend=='mms-fa')
        for tool in ('fa-kara','sug','milikara','timing','yohane'):
            views.append(external('M2',sep+'-'+tool,other,tool,sep))
        native('M2',sep+'-dictionary-mms-fa',[sid for sid in other if sid!='jy01'],sep=sep,backend='mms-fa',smart=True,condition='dictionary')
    for sep in ('demucs','bs'):
        for audio_format in ('float','aac'):
            for backend in ('nextfire','mms-fa'):
                native('M3',f'{sep}-{audio_format}-{backend}',all_songs,sep=sep,backend=backend,audio_format=audio_format,smart=backend=='mms-fa')
    for model in config['modules']['M5']['models']:
        for mode in (['global','core'] if model in config['modules']['M5']['core_models'] else ['core']):
            native('M5',model+'-'+mode,ja,sep=model,mode=mode)
        for device in ('cuda','cpu'):
            add(f'benchmark-{model}-{device}','M5','timing/separation_resources.py',[model,'--device',device],config['modules']['M5']['benchmark_cpu_songs'] if device=='cpu' else config['modules']['M5']['benchmark_songs'],
                {'sug':'sug','milikara':'milikara','yohane':'yohane'}.get(model,'research'),
                [f'results/separation-resources/{model}{"-cpu" if device=="cpu" else ""}.json.gz'],kind='benchmark',separator=model,device=device,execution='manual' if device=='cuda' and config['modules']['M5'].get('gpu_benchmark_execution')=='manual_after_other_experiments' else 'automatic')
    for sep in ('demucs','bs'):
        for mode in ('core','human'):
            native('M6',f'{sep}-nextfire-{mode}',ja,sep=sep,mode=mode)
        for smart in (False,True):
            native('M6',f'{sep}-mms-fa-{"smart" if smart else "raw"}',ja,sep=sep,backend='mms-fa',smart=smart)
        folder=f'results/M6/predictions/{sep}-tifa-human'
        add('M6-'+sep+'-tifa-human','M6','phase2_tifa.py',['--sep',sep,'--songs',*ja,'--output-dir',folder],ja,'native5',[f'{folder}/{sid}.json.gz' for sid in ja],kind='tifa',condition=sep+'-tifa-human',separator=sep)
        views.append(external('M6',sep+'-timing-two-stage',ja,'timing',sep))
    for script in ('prepare_audio','run_factorial','prepare_original','run_original_controls'):
        outputs=[]
        if script=='run_factorial':
            import itertools
            cases=['soft-'+''.join(map(str,bits)) for bits in itertools.product([0,1],repeat=3)]+['delimiter','free_tail']
            outputs=[f'results/milikara/predictions/{sid}--concat_core--{case}.json.gz' for sid in ja for case in cases]
        elif script=='run_original_controls':outputs=[f'results/milikara/predictions/{sid}--concat_core--{name}.json.gz' for sid in ja for name in ['retry-vocals','retry-original']]
        add('M7-'+script,'M7','milikara/'+script+'.py',[],ja,outputs=outputs,kind='decoder')
    add('M8-refine','M8','phase2_refine.py',['--songs',*ja],ja,outputs=[f'results/M8/predictions/{trigger}-{strategy}/{sid}.json.gz' for trigger in config['modules']['M8']['triggers'] for strategy in config['modules']['M8']['strategies'] for sid in ja],kind='refinement')
    return jobs, views


if __name__ == '__main__':
    jobs, views = build_jobs()
    dump(ROOT / 'configs/phase2-jobs.json', {'jobs':jobs,'external_views':views})
    print(f'{len(jobs)} executable partitions; {sum(len(job["songs"]) for job in jobs)} song/partition entries; {len(views)} native-export views.')

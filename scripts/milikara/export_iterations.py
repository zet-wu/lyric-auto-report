"""Export terminal states for common scoring; all raw rounds remain available."""
from common import *
for name in ('cached-results','gpu-results','self-fresh-results'):
    last={}
    for record in read(OUT/(name+'.json'))['records']:
        last[(record['song'],record['mode'])]=record
    for (sid,mode),record in last.items():
        variants={'terminal':record['predictions']}
        if 'unguarded_predictions' in record:variants['terminal-unguarded']=record['unguarded_predictions']
        for variant,pred in variants.items():
            key=f'iteration/{mode}/{variant}'
            dump(OUT/'predictions'/f"{sid}--{mode}--{variant}.json",
                {'song':sid,'kind':'auto-readings','experiment':key,'predictions':pred,'terminal_round':record['round']})

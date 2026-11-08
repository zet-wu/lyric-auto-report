from common import *
timing_imports()
from timing.ttml_input import parse_ttml

results=[]
for song in read(OUT/'reference.json'):
    try:
        lines=[line for line in parse_ttml((ROOT/song['ttml']).read_text()) if line.role=='main']
        mismatches=[{'line':i+1,'expected':ref['text'],'parsed':got.text}
                    for i,(ref,got) in enumerate(zip(song['lines'],lines)) if ref['text']!=got.text]
        results.append({'song':song['id'],'rows':len(lines),'expected_rows':len(song['lines']),'mismatches':mismatches})
    except Exception as error:
        results.append({'song':song['id'],'error':str(error)})
dump(OUT/'timing-ttml-import-audit.json',results)
print([(r['song'],r.get('error') or len(r['mismatches'])) for r in results])

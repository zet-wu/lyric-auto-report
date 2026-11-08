"""Generate text-only reading inputs with the pinned Studio reading functions."""
from common import *
product_imports()
import subprocess
from server.reading import SudachiReadingProposer, ReadingSnapshot, analyze_snapshot

inputs_only=[{'id':s['id'],'lines':[{'id':l['id'],'index':l['index'],'text':l['text']} for l in s['lines']]}
             for s in read(OUT/'confirmed-targets.json') if s['id']!='s13']
dump(OUT/'text-only-input.json',inputs_only)
proposer=SudachiReadingProposer()
if not proposer.available:raise RuntimeError(proposer.unavailable_reason)
ranges=[]
for song in inputs_only:
    body=ReadingSnapshot(lines=[{'id':l['id'],'text':l['text']} for l in song['lines']])
    ranges.append({'id':song['id'],'ranges':analyze_snapshot(body,proposer).model_dump()['ranges']})
dump(OUT/'studio-reading-ranges.json',ranges)
subprocess.run(['node',str(ROOT/'scripts/milikara/auto_readings.cjs')],check=True)

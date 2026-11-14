"""Read the smallest persisted checkpoint intervals from native .sug files."""
from common import *

def saved_segments(record):
 data=read(ROOT/record['sug_project']['path'])
 assert data.get('global_offset_ms') in (None,0)
 lines=[]
 for line in data['sentences']:
  chars=line['characters'];points=[]
  for ci,c in enumerate(chars):
   assert len(c['timestamps'])<=c['check_count']
   for cp,ts in enumerate(c['timestamps']):points.append((ci,cp,ts))
   if c['sentence_end_ts'] is not None:points.append((ci,None,c['sentence_end_ts']))
  intervals={}
  for i,(ci,cp,ts) in enumerate(points):
   if cp is not None:intervals[ci,cp]=(ts/1000,points[i+1][2]/1000 if i+1<len(points) else None)
  parts=[]
  for ci,c in enumerate(chars):
   spans=[intervals[ci,cp] for cp in range(len(c['timestamps']))]
   ruby=c.get('ruby',{}).get('parts',[]);units=[]
   for cp,(a,b) in enumerate(spans):
    reading=ruby[cp]['text'] if cp<len(ruby) else c['char'] if len(spans)==1 and not re.search('[\u3400-\u9fff]',c['char']) else ''
    if reading:units.append({'text':reading,'start':a,'end':b})
   parts.append({'text':c['char'],'units':units,'start':spans[0][0] if spans else None,'end':spans[-1][1] if spans else None})
  lines.append(parts)
 return lines

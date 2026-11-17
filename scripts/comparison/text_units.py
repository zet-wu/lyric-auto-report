"""Project native timed reading units to unambiguous original-text boundaries."""
import re
from functools import lru_cache

def split_timed_text(surface, units, normalize, envelope):
 """Keep native unit times; never interpolate or use reference pronunciations.

 Explicit unit surfaces take precedence. Otherwise literal kana anchor opaque
 kanji runs; retain only boundaries shared by every exact matching alignment.
 """
 text=normalize(surface)
 def kana(s):return ''.join(chr(ord(c)-96) if 'ァ'<=c<='ヶ' else c for c in normalize(s))
 def whole():
  a,b=envelope(units)
  return [{'text':surface,'start':a,'end':b}]
 if not text or not units:return whole()
 surfaces=[normalize(u.get('surface','')) for u in units]
 if all(surfaces) and ''.join(surfaces)==text:
  return [{'text':s,'start':u['start'],'end':u['end']} for s,u in zip(surfaces,units)]
 readings=[kana(u['text']) for u in units]
 if not all(readings):return whole()
 reading=''.join(readings);unit_edges={0:0};pos=0
 for i,r in enumerate(readings):pos+=len(r);unit_edges[pos]=i+1
 atoms=re.findall('[\u3400-\u9fff々]+|.',text)
 @lru_cache(None)
 def ends(i,j):
  if i==len(atoms):return ()
  atom=atoms[i]
  if re.fullmatch('[\u3400-\u9fff々]+',atom):return range(j+1,len(reading)+1)
  token=kana(atom)
  return (j+len(token),) if reading.startswith(token,j) else ()
 @lru_cache(None)
 def possible(i,j):
  if i==len(atoms):return j==len(reading)
  return any(possible(i+1,k) for k in ends(i,j))
 if not possible(0,0):return whole()
 frontier={0};cuts=[(0,0)];offset=0
 for i,atom in enumerate(atoms):
  frontier={k for j in frontier for k in ends(i,j) if possible(i+1,k)}
  offset+=len(atom)
  if len(frontier)==1:
   k=next(iter(frontier))
   if k in unit_edges:cuts.append((offset,unit_edges[k]))
 result=[]
 for (a,u),(b,v) in zip(cuts,cuts[1:]):
  start,end=envelope(units[u:v]);result.append({'text':text[a:b],'start':start,'end':end})
 return result

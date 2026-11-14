from pathlib import Path
import json,sys,os,unicodedata,re
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/reading'
os.chdir(ROOT)
os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
deps=ROOT/'.deps/comparison' if (ROOT/'.deps/comparison/studio').exists() else ROOT/'.deps'
sys.path[:0]=[str(deps/name) for name in ('studio','milikara','timing')]
def read(p):return json.loads(Path(p).read_text())
def dump(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def hira(s):
 s=unicodedata.normalize('NFKC',s)
 return ''.join(chr(ord(c)-96) if 'ァ'<=c<='ヶ' else c for c in s)
def clean(s):return ''.join(c for c in hira(s) if c.isalnum() or c=='ー')
def kana(s):return bool(clean(s)) and bool(re.fullmatch('[ぁ-ゖー]+',clean(s)))
def segments(text,pairs):
 result=[];pos=0
 for surface,reading in pairs:
  start=text.find(surface,pos)
  if start<0:raise ValueError('source surface mismatch '+repr(surface))
  if start>pos:result.append({'a':pos,'b':start,'text':text[pos:start],'reading':text[pos:start]})
  result.append({'a':start,'b':start+len(surface),'text':surface,'reading':hira(reading or '')});pos=start+len(surface)
 if pos<len(text):result.append({'a':pos,'b':len(text),'text':text[pos:],'reading':text[pos:]})
 assert ''.join(p['text'] for p in result)==text
 return result

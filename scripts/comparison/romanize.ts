import {readFileSync,writeFileSync,readdirSync,mkdirSync} from 'node:fs';
import {createLyricDocument,createLine,createWord} from '../../.deps/comparison/studio/frontend/src/domain/lyric-document';
import {proposeRomanization} from '../../.deps/comparison/studio/frontend/src/domain/romanization-generation';
const dir='results/comparison/milikara/inputs/manual';mkdirSync('results/comparison/yohane/inputs',{recursive:true});
for(const f of readdirSync(dir)){
 const s=JSON.parse(readFileSync(`${dir}/${f}`,'utf8'));
 for(const l of s.lines){
  const units=l.words.flatMap((w:any)=>w.units.map((u:any)=>({...u,word_id:w.id})));
  const doc=createLyricDocument(),line=createLine('',l.id);line.words=units.map((u:any)=>createWord(u.reading,u.id));doc.lines=[line];
  const p=proposeRomanization(doc,[line.id],'timed')[0];if(p.groups.length!==units.length)throw Error(l.id);
  units.forEach((u:any,i:number)=>u.roman=(/^[\x00-\x7F]+$/.test(u.reading)?u.reading:p.groups[i].text).trim().toLowerCase());
  for(const w of l.words){
   w.roman=units.filter((u:any)=>u.word_id===w.id).map((u:any)=>u.roman).join('');
   for(const u of w.units)u.roman=units.find((x:any)=>x.id===u.id)!.roman;
  }
 }
 writeFileSync(`results/comparison/yohane/inputs/${f}`,JSON.stringify(s,null,2));
}

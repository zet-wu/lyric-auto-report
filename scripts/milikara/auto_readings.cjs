// Read-only calls into Studio. Input contains only raw lines, no original word or time structure.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');global.crypto=crypto.webcrypto;
const root=path.resolve(__dirname,'../..'),front=path.resolve(root,'.deps/studio/frontend'),out=path.join(root,'results/milikara');
const ts=require(path.join(root,'.deps/node/node_modules/typescript'));
require.extensions['.ts']=(module,filename)=>module._compile(ts.transpileModule(fs.readFileSync(filename,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,filename);
const {createLyricDocument,createLine,createWord}=require(path.join(front,'src/domain/lyric-document.ts'));
const {proposeJapaneseRuby,japaneseRubyCommand}=require(path.join(front,'src/domain/japanese-ruby.ts'));
const {proposeRomanization}=require(path.join(front,'src/domain/romanization-generation.ts'));
const {splitReadingMora}=require(path.join(front,'src/domain/ruby-editing.ts'));
const inputs=JSON.parse(fs.readFileSync(path.join(out,'text-only-input.json'))),ranges=JSON.parse(fs.readFileSync(path.join(out,'studio-reading-ranges.json')));
const output=inputs.map(song=>{
 let doc=createLyricDocument();doc.lines=song.lines.map(l=>createLine(l.text,l.id));
 const proposals=proposeJapaneseRuby(doc,doc.lines.map(l=>l.id),ranges.find(s=>s.id===song.id).ranges);
 const command=japaneseRubyCommand(doc,doc,proposals);doc=command.document;
 const native=proposeRomanization(doc,doc.lines.map(l=>l.id),'timed');
 const lines=doc.lines.map((line,i)=>{
  const pieces=line.words.flatMap(w=>splitReadingMora(w.rubyUnits.length?w.rubyUnits.map(u=>u.reading).join(''):w.text)).filter(x=>/[\p{L}\p{N}ー]/u.test(x));
  const japanese=/[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]/u.test(song.lines[i].text);
  // Pure English lyrics retain their source words. Japanese mora segmentation is
  // deterministic Studio splitReadingMora, never reference-driven.
  const readings=japanese?pieces:song.lines[i].text.match(/[A-Za-z]+(?:'[A-Za-z]+)?/g)||[];
  const phonetic={...line,words:readings.map((s,n)=>createWord(s,`${line.id}:auto-${n}`))};
  const groups=japanese?proposeRomanization({...doc,lines:[phonetic]},[line.id],'timed')[0].groups:readings.map(text=>({text,beginMs:null,endMs:null,hint:''}));
  if(groups.some(g=>g.beginMs!==null||g.endMs!==null))throw Error('Reference timing leak');
  return {...song.lines[i],japanese,readings,units:groups.map((g,n)=>({text:g.text.trim().toLowerCase(),reading:readings[n],hint:g.hint})),native_groups:native[i].groups,unresolved:proposals[i].blocks.filter(b=>b.editable&&!b.reading)};
 });
 return {id:song.id,lines,proposals};
});
fs.writeFileSync(path.join(out,'auto-readings.json'),JSON.stringify(output,null,2)+'\n');
const files=['lyric-document.ts','japanese-ruby.ts','ruby-editing.ts','romanization-generation.ts'];
fs.writeFileSync(path.join(out,'studio-frontend-identity.json'),JSON.stringify(Object.fromEntries(files.map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(path.join(front,'src/domain',f))).digest('hex')])),null,2)+'\n');
console.log(output.map(s=>({song:s.id,units:s.lines.reduce((n,l)=>n+l.units.length,0),unresolved:s.lines.flatMap(l=>l.unresolved),empty:s.lines.flatMap(l=>l.units.filter(u=>!u.text))})));

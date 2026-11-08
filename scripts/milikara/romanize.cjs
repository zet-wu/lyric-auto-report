const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..'),front=path.join(root,'.deps/studio/frontend');
const ts=require(path.join(root,'.deps/node/node_modules/typescript'));
require.extensions['.ts']=(module,filename)=>module._compile(ts.transpileModule(fs.readFileSync(filename,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,filename);
const {createLyricDocument,createLine,createWord}=require(path.join(front,'src/domain/lyric-document.ts'));
const {proposeRomanization}=require(path.join(front,'src/domain/romanization-generation.ts'));
const songs=JSON.parse(fs.readFileSync(path.join(root,'results/milikara/reading-input.json')));
for(const song of songs)for(const row of song.lines){
 const doc=createLyricDocument(),line=createLine('',row.id);line.words=row.units.map((u,i)=>createWord(u.reading,`${row.id}:${i}`));doc.lines=[line];
 const p=proposeRomanization(doc,[line.id],'timed')[0];
 if(p.groups.length!==row.units.length)throw Error('Unexpected romanization grouping');
 row.units.forEach((u,i)=>u.text=(u.language==='latin'?u.reading:p.groups[i].text).trim().toLowerCase());
}
fs.writeFileSync(path.join(root,'results/milikara/romanized.json'),JSON.stringify(songs,null,2));

import {readFileSync,writeFileSync,existsSync,readdirSync} from 'node:fs';
import {gunzipSync} from 'node:zlib';
import {JSDOM} from '../../.deps/comparison/studio/frontend/node_modules/jsdom/lib/api.js';
import {parseLyricTtml,serializeLyricTtml} from '../../.deps/comparison/studio/frontend/src/adapters/ttml/lyric-codec';
import {createLyricDocument,createLine,createWord} from '../../.deps/comparison/studio/frontend/src/domain/lyric-document';
import {segmentText,DEFAULT_SEGMENT_OPTIONS} from '../../.deps/comparison/studio/frontend/src/domain/segmentation';
import {proposeJapaneseRuby,japaneseRubyCommand,hasJapaneseRubyChanges} from '../../.deps/comparison/studio/frontend/src/domain/japanese-ruby';
import {createProjectDocument} from '../../.deps/comparison/studio/frontend/src/domain/project-document';
import {mergeAlignment} from '../../.deps/comparison/studio/frontend/src/domain/alignment';
const win=new JSDOM('').window;Object.assign(globalThis,{NodeFilter:win.NodeFilter,Node:win.Node,DOMParser:win.DOMParser,XMLSerializer:win.XMLSerializer});
const C='.cache/comparison',O='results/comparison';const read=(p:string)=>JSON.parse(existsSync(p)?readFileSync(p,'utf8'):gunzipSync(readFileSync(p+'.gz')).toString('utf8')),write=(p:string,x:any)=>writeFileSync(p,JSON.stringify(x));
if(process.argv[2]==='prepare')for(const s of read(`${O}/reference.json`).filter((s:any)=>!['s11','s13','s14'].includes(s.id))){
 const sid=s.id,raw=read(`${C}/inputs/${sid}-studio.json`);
 const xml=new DOMParser().parseFromString(raw.lyrics.draftTtml,'application/xml');
 for(const e of Array.from(xml.getElementsByTagName('*')))if(!['p','span'].includes(e.localName))e.removeAttributeNS('urn:lazulite:studio:draft','id');
 const remap=new Map(Array.from(xml.getElementsByTagName('*')).filter(e=>e.getAttributeNS('http://www.w3.org/XML/1998/namespace','id')&&e.getAttributeNS('urn:lazulite:studio:draft','id')).map(e=>[e.getAttributeNS('http://www.w3.org/XML/1998/namespace','id'),e.getAttributeNS('urn:lazulite:studio:draft','id')]));
 for(const e of Array.from(xml.getElementsByTagName('*')))for(const a of Array.from(e.attributes))if(remap.get(a.value))a.value=remap.get(a.value)!;
 for(const e of Array.from(xml.getElementsByTagName('*')))if(e.localName==='p'&&e.getAttributeNS('urn:lazulite:studio:draft','id'))e.setAttributeNS('http://www.w3.org/XML/1998/namespace','xml:id',e.getAttributeNS('urn:lazulite:studio:draft','id')!);
 const manual=parseLyricTtml(new XMLSerializer().serializeToString(xml),{draft:true});manual.lines=manual.lines.filter(l=>!l.backgroundOf);manual.translationTracks=[];manual.romanizationTracks=[];
 let auto=createLyricDocument();const reading=read(`${C}/inputs/${sid}-reading.json`);
 auto.lines=reading.lines.map((l:any)=>({...createLine('',l.id),words:segmentText(l.text,DEFAULT_SEGMENT_OPTIONS).map((x:string,i:number)=>createWord(x,`${l.id}-auto-${i}`))}));
 const rows=proposeJapaneseRuby(auto,auto.lines.map(l=>l.id),reading.proposals,true);
 if(hasJapaneseRubyChanges(rows,auto))auto=(japaneseRubyCommand(auto,auto,rows) as any).document;
 for(const [condition,doc] of [['manual',manual],['auto',auto]] as const){
 const project=createProjectDocument(doc);project.lineOrder=doc.lines.map(l=>l.id);
 write(`${C}/inputs/${sid}-studio-${condition}-project.json`,project);
 write(`${C}/inputs/${sid}-studio-${condition}.json`,{lyrics:{draftTtml:serializeLyricTtml(doc,{draft:true})},lineOrder:project.lineOrder,editing:project.editing});
 }
 console.log('PREPARED',sid);
}else for(const f of [...new Set(readdirSync(`${O}/studio`).map(f=>f.replace(/\.gz$/,'')))].filter(f=>f.endsWith('.json')&&!f.endsWith('-adopt.json'))){
 const data=read(`${O}/studio/${f}`);if(data.status!=='ok')continue;
 const project=read(`${C}/inputs/${data.song}-studio-${data.condition}-project.json`);
 const scope=new Set(data.projection.scope.map((x:any)=>x.object_id));
 for(const l of project.lyrics.lines)l.words=l.words.filter((w:any)=>w.rubyUnits.length||scope.has(w.id)||w.text.trim());
 const result:any={alignment:{schema:'lazulite-japanese-result-v1',units:data.result.units},mapping:data.projection.mapping,scope:data.projection.scope,object_timings:data.object_timings,acoustics:{analysisId:null,segments:data.analysis.segments.map((s:any)=>({id:s.id,beginMs:Math.round(s.core_start*1000),endMs:Math.round(s.core_end*1000)}))}};
 const merged=mergeAlignment(project,result,Math.round(data.duration*1000),true,null);
 write(`${O}/studio/${f.replace('.json','-adopt.json')}`,{song:data.song,condition:data.condition,model:data.model,separator:data.separator,document:merged.project.lyrics});
 console.log('ADOPT',f);
}

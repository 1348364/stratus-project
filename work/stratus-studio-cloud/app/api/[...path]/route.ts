import { env } from 'cloudflare:workers';
import seed from '../../../lib/seed.json';
export const dynamic='force-dynamic';
const chat='Coding Stratus (2)';
const keys=['spec','changes'];
const token='cloud-owner-session';
const json=(value:any,status=200)=>Response.json(value,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
async function hash(text:string){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text)))].map(x=>x.toString(16).padStart(2,'0')).join('');}
async function init(db:any){if((await db.prepare('SELECT count(*) AS total FROM documents').first()).total===2)return;for(const id of keys){const text=(seed.documents as any)[id].text;await db.prepare('INSERT OR IGNORE INTO documents (id,text,revision,modified) VALUES (?,?,?,?)').bind(id,text,await hash(text),new Date().toISOString()).run();}}
async function docs(db:any){const {results}=await db.prepare('SELECT * FROM documents').all();return Object.fromEntries(results.map((r:any)=>[r.id,{...r,filename:(seed.documents as any)[r.id].filename,path:seed.project+'/work/Custom instructions/'+(seed.documents as any)[r.id].filename}]));}
async function meta(db:any,key:string){const row=await db.prepare('SELECT value FROM metadata WHERE key=?').bind(key).first();return row?JSON.parse(row.value):null;}
async function putMeta(db:any,key:string,value:any){await db.prepare('INSERT INTO metadata (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').bind(key,JSON.stringify(value)).run();}
async function save(db:any,id:string,body:any){if(!keys.includes(id)||typeof body.text!=='string'||typeof body.revision!=='string')return json({error:'Text and revision are required.'},400);if(new TextEncoder().encode(body.text).length>2000000)return json({error:'Document is too large.'},413);const current=(await docs(db))[id];if(current.revision!==body.revision)return json({error:'This file changed elsewhere. Compare both versions.',document:current},409);const revision=await hash(body.text);if(revision===current.revision)return json({document:current,unchanged:true});const modified=new Date().toISOString();const backup=crypto.randomUUID()+'.md';const batch=await db.batch([db.prepare('INSERT INTO history (id,document,text,revision,modified) SELECT ?,id,text,revision,? FROM documents WHERE id=? AND revision=?').bind(backup,modified,id,current.revision),db.prepare('UPDATE documents SET text=?,revision=?,modified=? WHERE id=? AND revision=?').bind(body.text,revision,modified,id,current.revision)]);if(!batch[1].meta.changes)return json({error:'The file changed while saving.',document:(await docs(db))[id]},409);return json({document:(await docs(db))[id],backup});}
async function handle(request:Request){
 const runtime=env as any,db=runtime.DB,url=new URL(request.url),path=url.pathname;
 const bridge=!!runtime.BRIDGE_KEY&&request.headers.get('X-Stratus-Bridge')===runtime.BRIDGE_KEY;
 const user=request.headers.get('oai-authenticated-user-id');
 if(!user&&!bridge)return json({error:'Sign in to your private Stratus Studio.'},401);
 if(path.startsWith('/api/bridge')&&!bridge)return json({error:'Mac connection authentication required.'},403);
 if(request.method!=='GET'){
  const origin=request.headers.get('Origin');
  if(origin&&origin!==url.origin)return json({error:'Cross-origin request rejected.'},403);
  if(!bridge&&request.headers.get('X-Studio-Token')!==token)return json({error:'Reload Studio before saving.'},403);
  if(Number(request.headers.get('Content-Length')||0)>2100000)return json({error:'Request too large.'},413);
 }
 await init(db);
 const all=await docs(db);
 if(request.method==='GET'){
  if(path==='/api/workspace'){const connection=await meta(db,'bridge');const release=all.spec.text.match(/Stratus-(\d+\.\d+\.\d+)\.zip/);return json({name:'Stratus Studio',project:seed.project,cloud:true,bridge:connection,release:release?.[1]||'Unspecified',token,documents:all});}
  if(path==='/api/activity')return json({filename:'CHANGE-LOG.md',text:(await meta(db,'activity'))?.text||seed.activity});
  if(path==='/api/chat'){const {results}=await db.prepare('SELECT id,operation,status,detail,queueId,created FROM jobs ORDER BY created DESC LIMIT 10').all();return json({name:chat,available:true,requests:results});}
  if(path==='/api/bridge/state'){const {results}=await db.prepare("SELECT * FROM jobs WHERE status IN ('waiting','dispatching') ORDER BY created LIMIT 1").all();return json({documents:all,jobs:results.map((r:any)=>({...r,revisions:JSON.parse(r.revisions)}))});}
  const history=path.match(/^\/api\/history\/(spec|changes)(?:\/([\w.-]+))?$/);
  if(history){if(history[2]){const row=await db.prepare('SELECT text,id AS name FROM history WHERE document=? AND id=?').bind(history[1],history[2]).first();return row?json(row):json({error:'Revision not found.'},404);}const {results}=await db.prepare('SELECT id AS name,length(text) AS bytes,modified FROM history WHERE document=? ORDER BY modified DESC LIMIT 100').bind(history[1]).all();return json({entries:results});}
 }
 const body=await request.json();
 const documentPath=path.match(/^\/api\/(?:documents|bridge\/documents)\/(spec|changes)$/);
 if(request.method==='PUT'&&documentPath)return save(db,documentPath[1],body);
 if(request.method==='POST'&&path==='/api/chat'){
  if(!['stage','run','spec','stage_run','related','run_both'].includes(body.operation)||typeof body.instructions!=='string'||body.instructions.length>12000||typeof body.id!=='string'||! /^[a-f0-9-]{36}$/.test(body.id))return json({error:'Invalid chat request.'},400);
  if(['spec','related'].includes(body.operation)&&!body.instructions.trim())return json({error:'Describe your specification edit or related shader work.'},400);
  const existing=await db.prepare('SELECT * FROM jobs WHERE id=?').bind(body.id).first();if(existing)return json(existing);
  if(keys.some(id=>body.revisions?.[id]!==all[id].revision))return json({error:'Documents changed. Review the latest saved files.'},409);
  const created=new Date().toISOString();const detail='Saved in the cloud queue. Coding Stratus (2) will receive this when your Mac is online and synced.';
  const instructions=body.instructions;
  // Immutable snapshots preserve the exact files the user chose to send.
  await putMeta(db,'job:'+body.id,{spec:all.spec,changes:all.changes});
  const inserted=await db.prepare("INSERT OR IGNORE INTO jobs (id,operation,instructions,revisions,status,detail,created) SELECT ?,?,?,?,'waiting',?,? WHERE (SELECT revision FROM documents WHERE id='spec')=? AND (SELECT revision FROM documents WHERE id='changes')=?").bind(body.id,body.operation,instructions,JSON.stringify(body.revisions),detail,created,all.spec.revision,all.changes.revision).run();
  if(!inserted.meta.changes)return json({error:'Documents changed while staging. Review and send again.'},409);
  return json({id:body.id,status:'waiting',detail,created,operation:body.operation});
 }
 if(request.method==='POST'&&path==='/api/bridge/heartbeat'){await putMeta(db,'bridge',{seen:new Date().toISOString(),status:body.status||'online',detail:String(body.detail||'').slice(0,500)});if(typeof body.activity==='string')await putMeta(db,'activity',{text:body.activity});return json({ok:true});}
 if(request.method==='POST'&&path==='/api/bridge/job'){
  const job=await db.prepare('SELECT * FROM jobs WHERE id=?').bind(body.id).first();if(!job)return json({error:'Request not found.'},404);
  if(body.claim){const result=await db.prepare("UPDATE jobs SET status='dispatching' WHERE id=? AND status='waiting'").bind(body.id).run();return json({claimed:!!result.meta.changes||job.status==='dispatching',snapshot:await meta(db,'job:'+body.id)});}
  if(!['queued','failed','unknown','waiting'].includes(body.status))return json({error:'Invalid delivery state.'},400);
  await db.prepare('UPDATE jobs SET status=?,detail=?,queueId=? WHERE id=?').bind(body.status,String(body.detail||'').slice(0,1800),body.queueId||null,body.id).run();return json({ok:true});
 }
 return json({error:'Endpoint not found.'},404);
}
export async function GET(request:Request){try{return await handle(request);}catch{return json({error:'Cloud storage is unavailable. Your editor draft is preserved.'},500);}}
export const PUT=GET;export const POST=GET;

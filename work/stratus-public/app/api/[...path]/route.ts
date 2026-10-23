import {env} from 'cloudflare:workers';
import {serverMailEnabled} from '../../../lib/feedback-mail';
import {getChatGPTUser,chatGPTSignInPath} from '../../chatgpt-auth';
import {containsPrivateContent} from '../../../lib/public-content';
export const dynamic='force-dynamic';
const json=(v:any,s=200)=>Response.json(v,{status:s,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
const sha=async(s:string)=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(x=>x.toString(16).padStart(2,'0')).join('');
const version=(v:any)=>typeof v==='string'&&/^\d+\.\d+\.\d+$/.test(v);
const compare=(a:string,b:string)=>{const x=a.split('.').map(Number),y=b.split('.').map(Number);for(let i=0;i<3;i++){if(x[i]!==y[i])return x[i]-y[i];}return 0;};
async function handle(req:Request){
 const e=env as any,u=new URL(req.url),p=u.pathname;
 const service=!!e.UPDATE_KEY&&req.headers.get('X-Stratus-Update')===e.UPDATE_KEY;
 if(req.method==='GET'&&p==='/api/image-formats')return json({jpeg:true,png:true});
 if(req.method==='GET'&&p==='/api/studio'){
  const user=await getChatGPTUser();
  if(!user)return new Response(null,{status:302,headers:{Location:chatGPTSignInPath('/api/studio'),'Cache-Control':'private, no-store','Referrer-Policy':'no-referrer'}});
  if(!e.STUDIO_OWNER_EMAIL||user.email.toLowerCase()!==e.STUDIO_OWNER_EMAIL.toLowerCase()||!e.STUDIO_URL)return json({error:'Not found.'},404);
  return new Response(null,{status:302,headers:{Location:e.STUDIO_URL,'Cache-Control':'private, no-store','Referrer-Policy':'no-referrer'}});
 }
 if(p.startsWith('/api/manage/')&&!service)return json({error:'Not authorised.'},403);
 if(req.method!=='GET'){const origin=req.headers.get('Origin');if(origin&&origin!==u.origin)return json({error:'Invalid origin.'},403);if(Number(req.headers.get('Content-Length')||0)>12000000)return json({error:'Request too large.'},413);}
 if(req.method==='GET'&&(p==='/api/release'||p==='/api/updates')){const item=await e.BUCKET.get(p==='/api/release'?'release.json':'updates.json');if(!item)return json(p==='/api/release'?{release:null}:{releases:[]});const value=await item.json();if(containsPrivateContent(value,e))return json({error:'Release feed unavailable.'},503);return Response.json(value,{headers:{'Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'}});}
 if(req.method==='PUT'&&p==='/api/manage/updates'){
  const raw=await req.text();if(raw.length>250000)return json({error:'Update feed too large.'},413);
  let b;try{b=JSON.parse(raw);}catch{return json({error:'Invalid updates.'},400);}
  if(containsPrivateContent(b,e))return json({error:'Private content cannot be published.'},400);
  if(!Array.isArray(b.releases)||!b.releases.length||b.releases.length>100)return json({error:'Invalid updates.'},400);
  const releases=[],seen=new Set();for(const r of b.releases){
   if(!version(r.version)||seen.has(r.version)||typeof r.date!=='string'||r.date.length>100||!Array.isArray(r.items)||!r.items.length||r.items.length>12||r.items.some((s:any)=>typeof s!=='string'||!s.trim()||s.length>4000))return json({error:'Invalid release notes.'},400);
   seen.add(r.version);releases.push({version:r.version,date:r.date,items:r.items});
  }
  releases.sort((a,b)=>compare(b.version,a.version));
  const prior=await e.BUCKET.get('updates.json');if(prior){const old=await prior.json();if(old.releases?.length&&compare(releases[0].version,old.releases[0].version)<0)return json({error:'Update downgrade rejected.'},409);}
  const value={releases,updated:new Date().toISOString()};await e.BUCKET.put('updates.json',JSON.stringify(value),{httpMetadata:{contentType:'application/json'}});return json({ok:true});
 }
 if(req.method==='GET'&&p.startsWith('/api/images/')){const key=p.slice('/api/images/'.length);if(!/^\d+\.\d+\.\d+\/[a-z0-9-]+-[a-f0-9]{12}\.(?:png|jpg)$/.test(key))return json({error:'Not found.'},404);const o=await e.BUCKET.get('images/'+key);return o?new Response(o.body,{headers:{'Content-Type':key.endsWith('.jpg')?'image/jpeg':'image/png','Cache-Control':'public,max-age=31536000,immutable','X-Content-Type-Options':'nosniff'}}):json({error:'Not found.'},404);}
 if(req.method==='PUT'&&p.startsWith('/api/manage/images/')){const key=p.slice('/api/manage/images/'.length);if(!/^\d+\.\d+\.\d+\/[a-z0-9-]+-[a-f0-9]{12}\.(?:png|jpg)$/.test(key))return json({error:'Invalid image key.'},400);const data=await req.arrayBuffer(),bytes=new Uint8Array(data),jpg=key.endsWith('.jpg');const valid=jpg?bytes[0]===255&&bytes[1]===216&&bytes[2]===255:bytes.slice(0,8).join(',')==='137,80,78,71,13,10,26,10';if(data.byteLength>10000000||data.byteLength<8||!valid)return json({error:'Expected a matching PNG or JPEG under 10 MB.'},400);await e.BUCKET.put('images/'+key,data,{httpMetadata:{contentType:jpg?'image/jpeg':'image/png'}});return json({ok:true});}
 if(req.method==='PUT'&&p==='/api/manage/release'){
  const b=await req.json();if(containsPrivateContent(b,e))return json({error:'Private content cannot be published.'},400);if(!version(b.version)||!Array.isArray(b.scenes)||!b.scenes.length||b.scenes.length>10||typeof b.summary!=='string'||b.summary.length>3000)return json({error:'Invalid release.'},400);
  const previous=await e.BUCKET.get('release.json');if(previous){const old=await previous.json();if(compare(b.version,old.version)<0)return json({error:'Release downgrade rejected.'},409);}
  const scenes=[];for(const s of b.scenes){if(!/^[a-z0-9-]{1,40}$/.test(s.id)||typeof s.title!=='string'||s.title.length>120||typeof s.description!=='string'||s.description.length>1500||typeof s.image!=='string'||!s.image.startsWith('/api/images/'+b.version+'/')||typeof s.alt!=='string'||s.alt.length>500)return json({error:'Invalid scene.'},400);if(!(await e.BUCKET.head('images/'+s.image.slice('/api/images/'.length))))return json({error:'Upload images before publishing.'},409);scenes.push({id:s.id,title:s.title,description:s.description,image:s.image,alt:s.alt,tag:'STRATUS '+b.version});}
  const value={version:b.version,summary:b.summary,date:String(b.date||'').slice(0,30),scenes,updated:new Date().toISOString()};await e.BUCKET.put('release.json',JSON.stringify(value),{httpMetadata:{contentType:'application/json'}});return json({ok:true,release:value});
 }
 if(req.method==='POST'&&p==='/api/feedback'){
  const raw=await req.text();if(raw.length>9000)return json({error:'Feedback is too long.'},413);let b;try{b=JSON.parse(raw);}catch{return json({error:'Invalid form.'},400);}
  if(typeof b.id!=='string'||! /^[a-f0-9-]{36}$/.test(b.id)||!['shader','website','both'].includes(b.topic)||typeof b.message!=='string'||b.message.trim().length<10||b.message.length>4000||typeof b.reply!=='string'||b.reply.length>254||(b.reply&&! /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(b.reply))||b.website||!Number.isFinite(b.started)||Date.now()-b.started<2000)return json({error:'Check your feedback and try again.'},400);
  const db=e.DB;if(await db.prepare('SELECT id FROM feedback WHERE id=?').bind(b.id).first())return json({ok:true,id:b.id});
  const hour=new Date().toISOString().slice(0,13),day=hour.slice(0,10);const ip=await sha(e.UPDATE_KEY+day+(req.headers.get('cf-connecting-ip')||'unknown'));const key='ip:'+hour+':'+ip,global='all:'+day;
  for(const [k,max] of [[key,5],[global,100]]){const row=await db.prepare('INSERT INTO limits (key,count) VALUES (?,1) ON CONFLICT(key) DO UPDATE SET count=count+1 WHERE count<? RETURNING count').bind(k,max).first();if(!row)return json({error:'Too many submissions. Please try again later.'},429);}
  await db.prepare('INSERT OR IGNORE INTO feedback (id,topic,message,reply,created,status,ip) VALUES (?,?,?,?,?,?,?)').bind(b.id,b.topic,b.message.trim(),b.reply.trim(),new Date().toISOString(),serverMailEnabled(e)?'cloud-pending':'pending',ip).run();
  await db.prepare('DELETE FROM limits WHERE key<?').bind('all:'+new Date(Date.now()-7*86400000).toISOString().slice(0,10)).run();
  return json({ok:true,id:b.id});
 }
 if(req.method==='GET'&&p==='/api/manage/feedback'){const query=u.searchParams.get('include_sent')==='1'?"SELECT id,topic,message,reply,created,status,receipt FROM feedback ORDER BY created DESC LIMIT 500":"SELECT id,topic,message,reply,created,status,receipt FROM feedback WHERE status!='sent' ORDER BY created LIMIT 25";const {results}=await e.DB.prepare(query).all();return json({items:results,delivery:serverMailEnabled(e)?'server':'local'});}
 if(req.method==='POST'&&p==='/api/manage/feedback'){
  const b=await req.json();if(!['sending','sent','unknown'].includes(b.status)||typeof b.id!=='string'||(b.status==='sent'&&(typeof b.receipt!=='string'||!b.receipt.length)))return json({error:'Invalid receipt.'},400);
  if(b.status==='sending'){if(serverMailEnabled(e))return json({claimed:false,delivery:'server'});const r=await e.DB.prepare("UPDATE feedback SET status='sending' WHERE id=? AND status='pending'").bind(b.id).run();return json({claimed:!!r.meta.changes});}
  await e.DB.prepare("UPDATE feedback SET status=?,receipt=? WHERE id=? AND status IN ('sending','unknown')").bind(b.status,String(b.receipt||'').slice(0,250),b.id).run();return json({ok:true});
 }
 return json({error:'Not found.'},404);
}
export async function GET(req:Request){try{return await handle(req);}catch{return json({error:'Service unavailable. Please try again later.'},503);}}
export const POST=GET;export const PUT=GET;

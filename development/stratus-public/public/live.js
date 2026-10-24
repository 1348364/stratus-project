'use strict';
let currentRelease=null,currentUpdates=null,showcaseVersion=null,latestVersion=null;
function feedStatus(){
 const status=latestVersion?`Latest release: Stratus ${latestVersion}${showcaseVersion?' · Showcase: '+showcaseVersion:''}`:showcaseVersion?`Live showcase · Stratus ${showcaseVersion}`:null;
 if(status){document.querySelector('#latest-release-note').textContent=status;document.querySelector('#feed-status').textContent=status;}
}
async function refreshUpdates(){
 try{
  const response=await fetch('/api/updates',{cache:'no-store'});if(!response.ok)return;
  const feed=await response.json();if(!Array.isArray(feed.releases)||!feed.releases.length||feed.updated===currentUpdates)return;
  currentUpdates=feed.updated;latestVersion=feed.releases[0].version;
  const list=document.querySelector('#live-update-list');list.replaceChildren();
  for(const [index,release] of feed.releases.entries()){
   const article=document.createElement('article');article.className='release';
   const meta=document.createElement('div');meta.className='release-meta';
   const number=document.createElement('span');number.className='release-version';number.textContent=release.version;
   const date=document.createElement('span');date.textContent=release.date;
   const label=document.createElement('span');label.className='release-label';label.textContent=index===0?'LATEST RELEASE':'RELEASE';meta.append(number,date,label);
   const content=document.createElement('div');content.className='release-content';
   const heading=document.createElement('h2');heading.textContent=`Stratus ${release.version}`;
   const bullets=document.createElement('ul');for(const note of release.items){const item=document.createElement('li');item.textContent=note;bullets.append(item);}
   content.append(heading,bullets);article.append(meta,content);list.append(article);
  }
  const published=new Set(feed.releases.map(r=>r.version));
  document.querySelectorAll('#release-list .release').forEach(el=>{el.hidden=published.has(el.querySelector('.release-version')?.textContent.trim());});
  document.querySelectorAll('[data-current-release]').forEach(el=>el.textContent=`STRATUS ${latestVersion} / IRIS`);feedStatus();
 }catch{/* Retain the last visible release notes if offline. */}
}

async function refreshRelease(){
 try{const response=await fetch('/api/release',{cache:'no-store'});if(!response.ok)return;const release=await response.json();if(!release.version||!Array.isArray(release.scenes)||!release.scenes.length)return;
 if(currentRelease===release.updated)return;currentRelease=release.updated;showcaseVersion=release.version;
 scenes=release.scenes.map(scene=>({...scene,version:release.version}));renderScenes();
 const hero=scenes[0];document.querySelector('.hero-image').src=hero.image;document.querySelector('.hero-image').alt=hero.alt;
 document.querySelectorAll('[data-release-number]').forEach(el=>el.textContent=release.version);
 document.querySelectorAll('[data-current-release]').forEach(el=>el.textContent=`STRATUS ${latestVersion||release.version} / IRIS`);
 document.querySelector('#gallery-release').textContent=`Real Minecraft captures from Stratus ${release.version}.`;
 document.querySelector('[data-view=showcases] .evidence-note').textContent=`These images were recorded for Stratus ${release.version}. Older reference scenes elsewhere on this site retain their original version labels. Appearance varies with world, settings and hardware.`;
 feedStatus();
 const box=document.querySelector('#live-release');box.className='live-release';box.replaceChildren();const title=document.createElement('h2');title.textContent=`Stratus ${release.version}`;const summary=document.createElement('p');summary.textContent=release.summary;const date=document.createElement('small');date.textContent=`Release captures · ${release.date}`;box.append(title,summary,date);
 }catch{/* Keep the labelled archived reference when offline. */}
}
refreshRelease();refreshUpdates();setInterval(()=>{if(!document.hidden){refreshRelease();refreshUpdates();}},60000);
const form=document.querySelector('#feedback-form'),feedbackStatus=document.querySelector('#feedback-result');let started=Date.now(),submissionId=null,submittedPayload=null;
form.addEventListener('input',()=>{submissionId=null;submittedPayload=null;});
form.addEventListener('submit',async event=>{event.preventDefault();if(!form.reportValidity())return;const button=form.querySelector('button[type=submit]');button.disabled=true;feedbackStatus.textContent='Sending…';
 const fields=new FormData(form);const payload={topic:fields.get('topic'),message:fields.get('message'),reply:fields.get('reply'),website:fields.get('website'),started};
 const signature=JSON.stringify(payload);if(signature!==submittedPayload){submissionId=crypto.randomUUID();submittedPayload=signature;}
 try{const response=await fetch('/api/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...payload,id:submissionId})});const result=await response.json();if(!response.ok||!result.ok)throw new Error(result.error||'Unable to send.');feedbackStatus.textContent='Thank you. Your feedback is saved for private email delivery.';form.reset();started=Date.now();submissionId=null;submittedPayload=null;}
 catch(error){feedbackStatus.textContent=error.message+' Your text is still here.';}finally{button.disabled=false;}
});

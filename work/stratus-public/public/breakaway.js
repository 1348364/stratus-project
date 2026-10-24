'use strict';
// Seeded document-space glass, rendered in one canvas with cached public-page reflections.
(()=>{
 const motion=window.StratusMotion,body=document.body,reduced=matchMedia('(prefers-reduced-motion: reduce)'),coarse=matchMedia('(pointer: coarse)'),transparency=matchMedia('(prefers-reduced-transparency: reduce)');if(!motion)return;
 const canvas=document.createElement('canvas');canvas.className='shard-reflections';canvas.setAttribute('aria-hidden','true');body.append(canvas);
 const ctx=canvas.getContext('2d',{alpha:true});if(!ctx)return;
 const clamp=n=>Math.max(0,Math.min(1,n)),noise=n=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);},smooth=n=>{n=clamp(n);return n*n*(3-2*n);};
 const idle=fn=>'requestIdleCallback'in window?requestIdleCallback(fn,{timeout:500}):setTimeout(fn,24);
 const textures=new Map(),patterns=new Map();let epoch=0,w=0,h=0,bandHeight=400,span=320,routeSeed=0,animatedY=scrollY,lastTick=0,gateAt=0,reset=true,latestY=0;
 const disabled=s=>s.hidden||s.paused||reduced.matches||transparency.matches||location.hash==='#feedback'||document.activeElement?.matches('input,textarea,select,:focus-visible')||document.querySelector('dialog[open]');
 function invalidate(){epoch++;textures.clear();patterns.clear();routeSeed=[...location.hash].reduce((s,c)=>s*31+c.charCodeAt(0),17)%100003;reset=true;motion.request();}
 function setup(s){w=s.w;h=s.h;bandHeight=Math.max(300,Math.round(h*.55));span=Math.max(260,Math.min(420,h*.42));invalidate();}
 function mesh(index){
  if(patterns.has(index))return patterns.get(index);const count=w<650?4:6,result=[];
  for(let i=0;i<count;i++){
   const seed=(index+1)*1271+i*83+routeSeed,width=75+noise(seed)*195,height=48+noise(seed+1)*92,n=noise(seed+3)<.43?3:noise(seed+3)<.8?4:5,points=[];
   for(let j=0;j<n;j++){const a=(j/n+(noise(seed+j+20)-.5)*.09)*Math.PI*2,r=.68+noise(seed+j+40)*.32;points.push([Math.cos(a)*width*.5*r,Math.sin(a)*height*.5*r]);}
   result.push({seed,points,width,height,x:(i+.12+noise(seed+4)*.76)/count*w,start:index*span+noise(seed+5)*span,travel:350+noise(seed+6)*300,turn:(noise(seed+7)-.5)*.8,drift:(noise(seed+8)-.5)*110});
  }
  patterns.set(index,result);if(patterns.size>6){const far=[...patterns.keys()].sort((a,b)=>Math.abs(b*span-latestY)-Math.abs(a*span-latestY));patterns.delete(far[0]);}return result;
 }
 function capture(index){
  if(index<0||textures.has(index))return;const version=epoch,record={index,y:index*bandHeight,ready:false,bitmap:null,readyAt:0,words:0,scale:1};textures.set(index,record);
  idle(()=>{
   if(version!==epoch||document.hidden||textures.get(index)!==record){if(textures.get(index)===record)textures.delete(index);return;}
   const scale=Math.min(1,(coarse.matches?680:960)/w),bitmap=document.createElement('canvas');bitmap.width=Math.ceil(w*scale);bitmap.height=Math.ceil(bandHeight*scale);const c=bitmap.getContext('2d');c.scale(scale,scale);c.fillStyle='#101817';c.fillRect(0,0,w,bandHeight);
   const root=document.querySelector('[data-view]:not([hidden])');if(!root||root.dataset.view==='feedback'){textures.delete(index);return;}
   // Reflection sources are the public view only. Form values, dialogs and private routes never enter a texture.
   const excluded='[hidden],.carousel-hidden,form,dialog,.voxel-stage,.layer-axis,.wordmark-depth i';
   const backgrounds=[root,...root.querySelectorAll('section,article,.hero,.reference-strip,.workflow-note,.world-layer,.atmosphere-wordmark,.table-scroll,img')],walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),styles=new Map();let phase=0,n=0,word=0,tokens=[],current=null;
   function slice(){
    if(version!==epoch||document.hidden||textures.get(index)!==record){if(textures.get(index)===record)textures.delete(index);return;}const started=performance.now();
    while(performance.now()-started<3){
     if(phase===0){
      if(n>=backgrounds.length){phase=1;continue;}const el=backgrounds[n++];if(el.closest(excluded))continue;const b=el.getBoundingClientRect(),y=b.top+scrollY-record.y;if(!b.width||y>bandHeight||y+b.height<0)continue;const st=getComputedStyle(el);if(st.visibility==='hidden'||st.display==='none')continue;
      if(el instanceof HTMLImageElement){if(!el.complete||!el.naturalWidth)continue;const ratio=Math.max(b.width/el.naturalWidth,b.height/el.naturalHeight),sw=b.width/ratio,sh=b.height/ratio;c.drawImage(el,(el.naturalWidth-sw)/2,(el.naturalHeight-sh)/2,sw,sh,b.left,y,b.width,b.height);}
      else if(st.backgroundColor!=='rgba(0, 0, 0, 0)'){c.beginPath();c.roundRect(b.left,y,b.width,b.height,Math.min(parseFloat(st.borderRadius)||0,b.width/2,b.height/2));c.fillStyle=st.backgroundColor;c.fill();if(parseFloat(st.borderTopWidth)){c.strokeStyle=st.borderTopColor;c.lineWidth=1;c.stroke();}}
     }else if(phase===1){
      const node=walker.nextNode();if(!node){phase=2;continue;}const parent=node.parentElement;if(!node.textContent.trim()||parent.closest(excluded+',script,style'))continue;const b=parent.getBoundingClientRect(),y=b.top+scrollY-record.y;if(b.width&&y<bandHeight&&y+b.height>0)tokens.push({node,parent});
     }else{
      if(record.words>=(coarse.matches?130:240)||(!current&&word>=tokens.length)){record.bitmap=bitmap;record.scale=scale;record.ready=true;record.readyAt=performance.now();canvas.dataset.reflectionWords=String(record.words);if(textures.size>4){const far=[...textures.values()].sort((a,b)=>Math.abs(b.y-latestY)-Math.abs(a.y-latestY));for(const old of far.slice(0,textures.size-4))textures.delete(old.index);}motion.request();return;}
      if(!current){const token=tokens[word++];let st=styles.get(token.parent);if(!st){st=getComputedStyle(token.parent);styles.set(token.parent,st);}if(st.display==='none'||st.visibility==='hidden')continue;current={...token,style:st,words:[...token.node.textContent.matchAll(/\S+/g)],at:0};}
      const item=current.words[current.at++];if(!item){current=null;continue;}const range=document.createRange();range.setStart(current.node,item.index);range.setEnd(current.node,item.index+item[0].length);const b=range.getBoundingClientRect(),y=b.top+scrollY-record.y;if(b.width&&y<bandHeight&&y+b.height>0){const st=current.style;c.font=`${st.fontStyle} ${st.fontWeight} ${st.fontSize} ${st.fontFamily}`;c.fillStyle=st.color;if('letterSpacing'in c)c.letterSpacing=st.letterSpacing==='normal'?'0px':st.letterSpacing;c.fillText(item[0],b.left,y+parseFloat(st.fontSize)*.82);record.words++;}
     }
    }
    idle(slice);
   }
   slice();
  });
 }
 function path(points){ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();}
 function read(s){
  if(w!==s.w||h!==s.h)setup(s);latestY=s.y;const off=disabled(s);if(!off){const first=Math.floor(s.y/bandHeight),last=Math.floor((s.y+s.h*.25)/bandHeight);for(let i=first;i<=last;i++)capture(i);if(textures.size>4){const far=[...textures.values()].sort((a,b)=>Math.abs(b.y-latestY)-Math.abs(a.y-latestY));for(const old of far.slice(0,textures.size-4))textures.delete(old.index);}}return off;
 }
 function write(off,s){
  const now=performance.now(),dt=lastTick?Math.min(40,now-lastTick):16;lastTick=now;const zone=s.h*.25,dpr=1;
  if(canvas.width!==Math.ceil(s.w*dpr)||canvas.height!==Math.ceil(zone*dpr)){canvas.width=Math.ceil(s.w*dpr);canvas.height=Math.ceil(zone*dpr);}ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,s.w,zone);canvas.hidden=off||s.y<4;
  if(canvas.hidden){animatedY=s.y;reset=true;return;}
  if(reset||Math.abs(animatedY-s.y)>s.h*1.4){animatedY=s.y;gateAt=now;reset=false;}
  animatedY+=(s.y-animatedY)*(1-Math.exp(-dt/85));const gain=smooth((animatedY-20)/160)*smooth((now-gateAt)/280);let settling=Math.abs(animatedY-s.y)>.2||now-gateAt<280,count=0,reflected=0;
  const first=Math.max(0,Math.floor((animatedY-690)/span)),last=Math.floor(animatedY/span),signature=[];
  for(let index=first;index<=last;index++)for(const p of mesh(index)){
   const t=(animatedY-p.start)/p.travel;if(t<=0||t>=1||count>=(coarse.matches?7:10))continue;
   const y=zone*.94-p.height*.35-t*t*(zone*.93+p.height*.35),x=p.x+Math.sin(t*Math.PI)*p.drift,opacity=gain*smooth(t/.2)*smooth((1-t)/.48)*.92;if(y+p.height*.65<0||opacity<.008)continue;
   count++;signature.push(p.seed);ctx.save();ctx.translate(x,y);ctx.rotate(p.turn+t*p.turn*.8);ctx.scale(1-t*.08,1-t*.14);path(p.points);ctx.clip();ctx.globalAlpha=opacity;
   const sourceY=s.y+zone*(.36+noise(p.seed+31)*.48),record=textures.get(Math.floor(sourceY/bandHeight)),zoom=1.02+noise(p.seed+32)*.62;
   if(record?.ready){const strength=clamp((now-record.readyAt)/230);if(strength<1)settling=true;ctx.save();ctx.globalAlpha=opacity*.88*strength;ctx.scale(-zoom,zoom*.94);const anchorY=sourceY-record.y,rw=p.width*1.3/zoom,rh=p.height*1.5/zoom,left=Math.max(0,x-rw*.5),top=Math.max(0,anchorY-rh*.5),right=Math.min(w,x+rw*.5),bottom=Math.min(bandHeight,anchorY+rh*.5);if(right>left&&bottom>top)ctx.drawImage(record.bitmap,left*record.scale,top*record.scale,(right-left)*record.scale,(bottom-top)*record.scale,left-x,top-anchorY,right-left,bottom-top);ctx.restore();reflected++;}
   ctx.fillStyle='rgba(183,230,207,.13)';ctx.fill();const sheen=ctx.createLinearGradient(-p.width*.5,-p.height*.5,p.width*.5,p.height*.5);sheen.addColorStop(0,'rgba(218,255,237,.40)');sheen.addColorStop(.35,'rgba(183,230,207,.10)');sheen.addColorStop(.7,'rgba(16,70,48,.18)');sheen.addColorStop(1,'rgba(199,248,220,.28)');ctx.fillStyle=sheen;ctx.fill();
   path(p.points);ctx.strokeStyle='rgba(8,41,29,.50)';ctx.lineWidth=3;ctx.stroke();ctx.strokeStyle='rgba(215,255,232,.80)';ctx.lineWidth=1.25;ctx.stroke();ctx.restore();
  }
  ctx.globalAlpha=1;ctx.globalCompositeOperation='destination-in';const fade=ctx.createLinearGradient(0,zone*.5,0,zone*.98);fade.addColorStop(0,'#000');fade.addColorStop(1,'transparent');ctx.fillStyle=fade;ctx.fillRect(0,0,w,zone);ctx.globalCompositeOperation='source-over';
  Object.assign(canvas.dataset,{shards:String(count),reflected:String(reflected),cached:String([...textures.values()].filter(r=>r.ready).length),pattern:signature.join('.'),zoneHeight:zone.toFixed(1),settling:String(settling)});if(settling)motion.request();
 }
 motion.register('glass-shatter',read,write);
 window.addEventListener('hashchange',invalidate);reduced.addEventListener('change',motion.request);document.addEventListener('focusin',motion.request);document.addEventListener('focusout',motion.request);
 document.addEventListener('load',e=>{if(e.target instanceof HTMLImageElement)invalidate();},true);document.fonts?.ready.then(invalidate);document.addEventListener('stratus:scenes-updated',invalidate);
 new MutationObserver(rows=>{if(rows.some(r=>r.addedNodes.length||r.removedNodes.length))invalidate();}).observe(document.querySelector('main'),{childList:true,subtree:true});
 new MutationObserver(motion.request).observe(body,{attributes:true,attributeFilter:['class']});motion.request();
})();

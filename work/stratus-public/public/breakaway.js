'use strict';
// Liquid-glass fragments stay in the top viewport quarter; scrolling reverses the fracture.
(()=>{
 const motion=window.StratusMotion,body=document.body,main=document.querySelector('main'),footer=document.querySelector('.public-footer'),reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const canvas=document.createElement('canvas');canvas.className='glass-canvas';canvas.setAttribute('aria-hidden','true');body.append(canvas);
 const ctx=canvas.getContext('2d',{alpha:true});if(!ctx)return;
 const bands=new Map();let epoch=0,width=0,bandHeight=420,dirty=true,geometry=[],content=[],lastFront=0;
 const clamp=x=>Math.max(0,Math.min(1,x)),noise=n=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);};
 const idle=fn=>'requestIdleCallback'in window?requestIdleCallback(fn,{timeout:700}):setTimeout(fn,40);
 const disabled=()=>reduced.matches||body.classList.contains('effects-paused')||document.hidden||document.activeElement?.matches('input,textarea,select,:focus-visible')||document.querySelector('dialog[open]');
 function invalidate(){epoch++;bands.clear();dirty=true;motion.request();}
 function measure(state){width=state.w;bandHeight=Math.max(320,Math.round(state.h*.65));geometry=[main,footer].filter(Boolean).map(el=>{const b=el.getBoundingClientRect();return {el,y:b.top+state.y,h:b.height};});content=[document.querySelector('[data-view]:not([hidden])'),footer].filter(Boolean);dirty=false;}
 function path(points){ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();}
 function mesh(index){
  const columns=Math.max(5,Math.round(width/150)),rows=3+Math.floor(noise(index+9)*3),points=[],shards=[];
  function divisions(count,length,seed){const weights=Array.from({length:count},(_,i)=>.3+noise(seed+i*17)*1.8),sum=weights.reduce((a,b)=>a+b,0),out=[0];for(const w of weights)out.push(out.at(-1)+w/sum*length);return out;}
  const xs=divisions(columns,width,index*89+3),ys=divisions(rows,bandHeight,index*47+8);
  for(let j=0;j<=rows;j++){points[j]=[];for(let i=0;i<=columns;i++){const key=(index*7+j)*83+i,dx=i&&i<columns?Math.min(xs[i]-xs[i-1],xs[i+1]-xs[i])*.35:0,dy=j&&j<rows?Math.min(ys[j]-ys[j-1],ys[j+1]-ys[j])*.35:0;points[j][i]=[xs[i]+(noise(key)-.5)*dx,ys[j]+(noise(key+71)-.5)*dy];}}
  function add(p,seed){const xx=p.map(v=>v[0]),yy=p.map(v=>v[1]),min=Math.min(...yy),left=Math.min(...xx);shards.push({p,seed,x:xx.reduce((a,b)=>a+b,0)/p.length,y:yy.reduce((a,b)=>a+b,0)/p.length,min,left,w:Math.max(...xx)-left,h:Math.max(...yy)-min});}
  for(let j=0;j<rows;j++)for(let i=0;i<columns;i++){const a=points[j][i],b=points[j][i+1],c=points[j+1][i],d=points[j+1][i+1],seed=index*107+j*columns+i;
   if(noise(seed+5)>.62){const t=.22+noise(seed+83)*.55,u=.22+noise(seed+93)*.55,m=[a[0]*(1-t)*(1-u)+b[0]*t*(1-u)+c[0]*(1-t)*u+d[0]*t*u,a[1]*(1-t)*(1-u)+b[1]*t*(1-u)+c[1]*(1-t)*u+d[1]*t*u];add([a,b,m],seed);add([b,d,m],seed+13);add([d,c,m],seed+29);add([c,a,m],seed+41);}
   else if(noise(seed)>.5){add([a,b,c],seed);add([b,d,c],seed+41);}else{add([a,b,d],seed);add([a,d,c],seed+41);}
  }return shards;
 }
 function warm(index){
  if(index<0||bands.has(index)||disabled())return;const version=epoch,record={index,y:index*bandHeight,ready:false,bitmap:null,shards:mesh(index)};bands.set(index,record);
  idle(()=>{
   if(version!==epoch||disabled()){if(bands.get(index)===record)bands.delete(index);return;}
   const scale=Math.min(1,1100/width),bitmap=document.createElement('canvas');bitmap.width=Math.ceil(width*scale);bitmap.height=Math.ceil(bandHeight*scale);const c=bitmap.getContext('2d');c.scale(scale,scale);c.fillStyle='#101817';c.fillRect(0,0,width,bandHeight);
   const origin=record.y,scroll=scrollY,tokens=[];
   // Only public presentation enters textures. Never rasterise form values or feedback results.
   for(const root of content){
    for(const el of [root,...root.querySelectorAll('section,article,.hero,.workspace-card,.reference-strip,.world-layer,.atmosphere-wordmark,img')]){
     if(el.closest('[hidden],.carousel-hidden,form'))continue;const b=el.getBoundingClientRect(),y=b.top+scroll-origin;if(b.width<1||y>bandHeight||y+b.height<0)continue;const style=getComputedStyle(el);if(style.display==='none'||style.visibility==='hidden')continue;
     if(el instanceof HTMLImageElement){if(!el.complete||!el.naturalWidth)continue;const ratio=Math.max(b.width/el.naturalWidth,b.height/el.naturalHeight),sw=b.width/ratio,sh=b.height/ratio;c.drawImage(el,(el.naturalWidth-sw)/2,(el.naturalHeight-sh)/2,sw,sh,b.left,y,b.width,b.height);}else if(style.backgroundColor!=='rgba(0, 0, 0, 0)'){c.fillStyle=style.backgroundColor;c.fillRect(b.left,y,b.width,b.height);}
    }
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let node;while((node=walker.nextNode())){const parent=node.parentElement;if(!node.textContent.trim()||parent.closest('[hidden],.carousel-hidden,script,style,form,.voxel-stage,.wordmark-depth i,.layer-axis'))continue;const b=parent.getBoundingClientRect(),y=b.top+scroll-origin;if(b.width&&y<bandHeight&&y+b.height>0)tokens.push({node,parent});}
   }
   let n=0,words=0;const limit=width<650?350:650;
   function textSlice(){if(version!==epoch||disabled()){if(bands.get(index)===record)bands.delete(index);return;}const start=performance.now(),nowScroll=scrollY;
    for(;n<tokens.length&&words<limit;n++){const {node,parent}=tokens[n],style=getComputedStyle(parent);if(style.visibility==='hidden'||style.display==='none')continue;c.font=`${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;c.fillStyle=style.color;if('letterSpacing'in c)c.letterSpacing=style.letterSpacing==='normal'?'0px':style.letterSpacing;
     const range=document.createRange();for(const match of node.textContent.matchAll(/\S+/g)){range.setStart(node,match.index);range.setEnd(node,match.index+match[0].length);const b=range.getBoundingClientRect(),y=b.top+nowScroll-origin;if(b.width&&y<bandHeight&&y+b.height>0){c.fillText(match[0],b.left,y+parseFloat(style.fontSize)*.82);words++;}}
     if(performance.now()-start>4){n++;idle(textSlice);return;}
    }
    record.bitmap=bitmap;record.scale=scale;record.ready=true;
    if(bands.size>4){const far=[...bands.values()].sort((a,b)=>Math.abs(b.y-lastFront)-Math.abs(a.y-lastFront));for(const old of far.slice(0,bands.size-4))bands.delete(old.index);}motion.request();
   }textSlice();
  });
 }
 function read(state){
  if(dirty||width!==state.w)measure(state);if(disabled())return {front:0,ready:[]};
  // A fixed viewport zone, with no end-of-page acceleration or sweep towards the footer.
  const front=state.y+Math.min(state.h*.16,state.y*.65);lastFront=front;
  const first=Math.max(0,Math.floor((front-state.h*.75)/bandHeight)),last=Math.floor((front+bandHeight*.5)/bandHeight);for(let i=first;i<=last;i++)warm(i);
  const ready=[...bands.values()].filter(b=>b.ready&&b.y<front+bandHeight&&b.y+bandHeight>front-state.h*.75),current=bands.get(Math.floor(front/bandHeight));return {front:current?.ready?front:0,ready};
 }
 function write({front,ready},state){
  const zone=Math.ceil(state.h*.25);if(canvas.width!==state.w||canvas.height!==zone){canvas.width=state.w;canvas.height=zone;}ctx.clearRect(0,0,canvas.width,canvas.height);
  for(const {el,y,h} of geometry){const cut=Math.min(h,Math.max(0,front-y));el.classList.toggle('glass-surface',cut>0);motion.style(el,'--glass-cut',`${cut.toFixed(1)}px`);}
  let count=0,minArea=Infinity,maxArea=0;const duration=Math.max(120,state.h*.26),budget=state.w<650?90:150;
  if(front>0)for(const band of ready)for(const shard of band.shards){
   const p=clamp((front-band.y-shard.min)/(duration*(.8+noise(shard.seed+7)*.4)));if(p<=0||p>=1||count>=budget)continue;const turn=noise(shard.seed+19)*2-1,fall=p*p,dx=turn*fall*state.w*.12,dy=-fall*duration*.25,x=shard.x+dx,y=band.y+shard.y-state.y+dy;if(y+shard.h<0||y-shard.h>zone)continue;
   count++;const area=shard.w*shard.h;minArea=Math.min(minArea,area);maxArea=Math.max(maxArea,area);
   ctx.save();ctx.globalAlpha=(1-p*p)*.82;ctx.translate(x,y);ctx.rotate(turn*fall*1.15);ctx.scale(1-fall*.1,Math.max(.25,Math.cos(p*(.6+noise(shard.seed)*1.2))));const local=shard.p.map(([px,py])=>[px-shard.x,py-shard.y]);path(local);ctx.clip();
   // Slight magnification and changing refraction make each piece behave like a thick glass lens.
   const bend=Math.sin(p*Math.PI+noise(shard.seed)*2)*5,zoom=1.025+Math.sin(p*Math.PI)*.025;
   ctx.drawImage(band.bitmap,0,0,band.bitmap.width,band.bitmap.height,-shard.x*zoom+bend,-shard.y*zoom-bend*.6,width*zoom,bandHeight*zoom);
   const left=shard.left-shard.x,top=shard.min-shard.y,sheen=ctx.createLinearGradient(left,top,left+shard.w,top+shard.h);
   sheen.addColorStop(0,'rgba(240,255,255,.38)');sheen.addColorStop(.25,'rgba(173,225,239,.08)');sheen.addColorStop(.52,'rgba(245,255,255,.02)');sheen.addColorStop(.78,'rgba(30,72,93,.18)');sheen.addColorStop(1,'rgba(220,247,255,.25)');ctx.fillStyle=sheen;ctx.fill();
   path(local);ctx.strokeStyle='rgba(223,252,255,.65)';ctx.lineWidth=1.3;ctx.stroke();
   // A curved specular streak travels through the shard as the scroll position changes.
   const shine=top+shard.h*(.18+p*.45);ctx.beginPath();ctx.moveTo(left,shine+shard.h*.15);ctx.quadraticCurveTo(left+shard.w*.45,shine-shard.h*.3,left+shard.w,shine);ctx.strokeStyle=`rgba(255,255,255,${Math.sin(p*Math.PI)*.36})`;ctx.lineWidth=1.4;ctx.stroke();ctx.restore();
  }
  canvas.hidden=count===0;canvas.dataset.shards=String(count);canvas.dataset.front=front.toFixed(0);canvas.dataset.cached=String(bands.size);canvas.dataset.zoneHeight=String(zone);canvas.dataset.sizeRatio=count?(maxArea/minArea).toFixed(1):'0';
 }
 motion.register('glass-shatter',read,write);
 window.addEventListener('hashchange',invalidate);window.addEventListener('resize',invalidate,{passive:true});reduced.addEventListener('change',motion.request);document.addEventListener('focusin',motion.request);document.addEventListener('focusout',motion.request);
 document.addEventListener('load',e=>{if(e.target instanceof HTMLImageElement)invalidate();},true);document.addEventListener('stratus:scenes-updated',invalidate);
 new ResizeObserver(()=>{dirty=true;motion.request();}).observe(main);
 new MutationObserver(rows=>{if(rows.some(r=>r.addedNodes.length||r.removedNodes.length))invalidate();}).observe(main,{childList:true,subtree:true});
 new MutationObserver(motion.request).observe(body,{attributes:true,attributeFilter:['class']});document.fonts?.ready.then(invalidate);motion.request();
})();

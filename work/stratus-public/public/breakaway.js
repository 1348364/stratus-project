'use strict';
// Uniform faceted stones, drawn on one bounded canvas. The accessible DOM never moves.
(() => {
 const motion=window.StratusMotion,body=document.body,reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const canvas=document.createElement('canvas');canvas.className='rock-canvas';canvas.setAttribute('aria-hidden','true');body.append(canvas);
 const context=canvas.getContext('2d',{alpha:true});if(!context)return;
 const records=new Map(),near=new Set(),active=new Set();let dirty=true,size=82,lastMetrics=0,totalMs=0,draws=0,worst=0,captureQueue=false;
 const clamp=x=>Math.max(0,Math.min(1,x));
 const idle=fn=>'requestIdleCallback'in window?requestIdleCallback(fn,{timeout:1200}):setTimeout(fn,40);
 const off=()=>reduced.matches||body.classList.contains('effects-paused')||document.hidden;
 const observer=new IntersectionObserver(entries=>{for(const e of entries){const r=records.get(e.target);if(!r)continue;if(e.isIntersecting){near.add(r);warm(r);}else near.delete(r);}motion.request();},{rootMargin:'350px 0px'});
 function register(){document.querySelectorAll('.immersive-hero,.home-view>.home-heading,.workspace-cards,.reference-strip,.gallery-section,.water-story,.public-faq,.workflow-note,.section-intro,.showcase-shot,.release,.spec-section,.platform-strip,.preset-guide,.spec-footnote,.upcoming-item,.roadmap-process,.roadmap-note').forEach(el=>{
   if(records.has(el)||el.parentElement.closest('[data-rock-group]'))return;
   el.dataset.rockGroup='';const r={el,bounds:null,cache:null,generation:0,last:0,used:0};records.set(el,r);observer.observe(el);
  });dirty=true;motion.request();}
 function measure(){for(const r of records.values()){
  if(!r.el.isConnected){observer.unobserve(r.el);records.delete(r.el);near.delete(r);continue;}
  if(r.el.closest('[data-view][hidden]')){r.bounds=null;continue;}
  const b=r.el.getBoundingClientRect(),old=r.bounds;r.bounds={x:b.left,y:b.top+scrollY,w:b.width,h:b.height};
  if(old&&(Math.abs(old.w-b.width)>1||Math.abs(old.h-b.height)>1)){r.cache=null;r.generation++;}
 }dirty=false;}
 function stonePath(ctx,x,y,s){ctx.beginPath();ctx.moveTo(x+s*.18,y);ctx.lineTo(x+s*.77,y);ctx.lineTo(x+s,y+s*.21);ctx.lineTo(x+s,y+s*.77);ctx.lineTo(x+s*.8,y+s);ctx.lineTo(x+s*.2,y+s);ctx.lineTo(x,y+s*.79);ctx.lineTo(x,y+s*.2);ctx.closePath();}
 function drawImage(ctx,img,b,origin){if(!img.complete||!img.naturalWidth)return;const x=b.left-origin.left,y=b.top-origin.top,w=b.width,h=b.height;if(w<1||h<1)return;
  const scale=Math.max(w/img.naturalWidth,h/img.naturalHeight),sw=w/scale,sh=h/scale;
  ctx.drawImage(img,(img.naturalWidth-sw)/2,(img.naturalHeight-sh)/2,sw,sh,x,y,w,h);
 }
 function warm(r){if(off()||r.cache||r.pending||!r.bounds||r.bounds.w<1)return;
  if([...r.el.querySelectorAll('img')].some(img=>!img.closest('.carousel-hidden')&&!img.complete))return;
  r.pending=true;const generation=r.generation;idle(()=>{
   if(off()||generation!==r.generation||!r.el.isConnected){r.pending=false;motion.request();return;}
   const b=r.el.getBoundingClientRect();if(b.width<1){r.pending=false;return;}
   const scale=Math.min(1,1100/b.width),height=Math.min(b.height,innerHeight+120),bitmap=document.createElement('canvas');bitmap.width=Math.ceil(b.width*scale);bitmap.height=Math.ceil(height*scale);
   const c=bitmap.getContext('2d');c.scale(scale,scale);c.fillStyle=getComputedStyle(r.el).backgroundColor;
   if(c.fillStyle==='rgba(0, 0, 0, 0)'||c.fillStyle==='transparent')c.fillStyle='#101817';c.fillRect(0,0,b.width,height);
   for(const img of r.el.querySelectorAll('img')){if(img.closest('.carousel-hidden'))continue;const box=img.getBoundingClientRect();if(box.bottom>b.top&&box.top<b.top+height)drawImage(c,img,box,b);}
   if(r.el.matches('.immersive-hero')){const shade=c.createLinearGradient(0,0,0,height);shade.addColorStop(0,'#0b171b22');shade.addColorStop(1,'#0b1417ed');c.fillStyle=shade;c.fillRect(0,0,b.width,height);}
   const walker=document.createTreeWalker(r.el,NodeFilter.SHOW_TEXT),tokens=[];let node;
   while((node=walker.nextNode())){const parent=node.parentElement;if(!node.textContent.trim()||parent.closest('[aria-hidden=true],script,style,[hidden],.carousel-hidden,.voxel-stage,.hero-bottom'))continue;
    tokens.push({node,parent});}
   let n=0,word=0;const limit=matchMedia('(pointer:coarse)').matches?220:420;
   function textSlice(){if(generation!==r.generation||off()){r.pending=false;motion.request();return;}const start=performance.now();
    for(;n<tokens.length&&word<limit;n++){
     const {node,parent}=tokens[n],style=getComputedStyle(parent);if(style.visibility==='hidden'||style.display==='none')continue;
     c.font=`${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;c.fillStyle=style.color;if('letterSpacing'in c)c.letterSpacing=style.letterSpacing==='normal'?'0px':style.letterSpacing;
     const range=document.createRange(),matches=[...node.textContent.matchAll(/\S+/g)];
     for(const match of matches){range.setStart(node,match.index);range.setEnd(node,match.index+match[0].length);const box=range.getBoundingClientRect();if(box.width&&box.top>=b.top-2&&box.top<b.top+height){c.fillText(match[0],box.left-b.left,box.top-b.top+parseFloat(style.fontSize)*.82);word++;}}
     if(performance.now()-start>4){n++;idle(textSlice);return;}
    }
    r.cache={bitmap,scale,height};r.pending=false;r.used=performance.now();
    const cached=[...records.values()].filter(v=>v.cache).sort((a,b)=>a.used-b.used);while(cached.length>4){const old=cached.shift();if(!active.has(old))old.cache=null;}
    motion.request();
   }textSlice();
  });}
 function read(state){if(dirty)measure();size=Math.max(64,Math.round(Math.sqrt(state.w*state.h/(state.w<650?95:150))));
  const list=[];if(off())return list;
  for(const r of near){const b=r.bounds;if(!b||!r.el.isConnected)continue;const top=b.y-state.y;
   const focused=r.el.contains(document.activeElement)&&document.activeElement.matches(':focus-visible');
   const p=focused?0:clamp((-70-top)/Math.max(300,Math.min(b.h,state.h)));
   if(!r.cache){warm(r);continue;}if(p>.035&&top+b.h> -100&&top<state.h){r.used=performance.now();list.push({r,p,top});}
  }return list.sort((a,b)=>(b.r.bounds.h+b.top)-(a.r.bounds.h+a.top)).slice(0,2);
 }
 function write(list,state){const start=performance.now();const width=Math.ceil(state.w),height=Math.ceil(state.h);
  if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
  context.clearRect(0,0,width,height);
  const current=new Set(list.map(x=>x.r));for(const r of active)if(!current.has(r)){r.el.classList.remove('rock-active');r.el.style.removeProperty('--rock-blend');}active.clear();
  let count=0;const budget=state.w<650?130:240;
  for(const {r,p,top} of list){const b=r.bounds,cache=r.cache,blend=clamp((p-.035)/.07),scatter=clamp((p-.04)*1.5);active.add(r);r.el.classList.add('rock-active');motion.style(r.el,'--rock-blend',blend.toFixed(3));
   for(let y=0;y<cache.height&&count<budget;y+=size)for(let x=0;x<b.w&&count<budget;x+=size){
    const i=Math.round(x/size)+Math.round(y/size)*31,s=Math.sin(i*12.9898),dx=(x+size/2-b.w/2)*scatter*.5+s*size*scatter*1.2,dy=(y+size/2-cache.height/2)*scatter*.3-scatter*95;
    const px=b.x+x+dx,py=top+y+dy;if(py>height+size||py+size< -size||px>width+size||px+size< -size)continue;
    count++;context.save();context.globalAlpha=blend*(1-scatter*.65);context.translate(px+size/2,py+size/2);context.rotate(s*scatter*.6);context.scale(1-scatter*.15,1-scatter*.15);
    const half=-size/2;stonePath(context,half+2,half+4,size-2);context.fillStyle='#071710';context.fill();context.save();stonePath(context,half,half,size-2);context.clip();
    const sw=Math.min(size,b.w-x),sh=Math.min(size,cache.height-y);context.drawImage(cache.bitmap,x*cache.scale,y*cache.scale,sw*cache.scale,sh*cache.scale,half,half,sw,sh);context.fillStyle=`rgba(76,97,84,${scatter*.2})`;context.fillRect(half,half,size,size);context.restore();
    stonePath(context,half,half,size-2);context.strokeStyle='#cbe6d337';context.lineWidth=.75;context.stroke();
    context.beginPath();context.moveTo(half+size*.8,half+size*.04);context.lineTo(half+size*.95,half+size*.23);context.lineTo(half+size*.95,half+size*.76);context.lineTo(half+size*.8,half+size*.91);context.closePath();context.fillStyle='#07171055';context.fill();context.restore();
   }
  }
  canvas.hidden=count===0;const ms=performance.now()-start;if(count){totalMs+=ms;draws++;worst=Math.max(worst,ms);}
  if(performance.now()-lastMetrics>500){canvas.dataset.fragments=String(count);canvas.dataset.drawMs=ms.toFixed(2);canvas.dataset.averageMs=(draws?totalMs/draws:0).toFixed(2);canvas.dataset.worstMs=worst.toFixed(2);canvas.dataset.cached=String([...records.values()].filter(r=>r.cache).length);lastMetrics=performance.now();}
 }
 motion.register('rocks',read,write);
 const invalidate=()=>{dirty=true;for(const r of records.values()){r.cache=null;r.generation++;}motion.request();};
 window.addEventListener('resize',invalidate,{passive:true});window.addEventListener('hashchange',invalidate);document.addEventListener('focusin',motion.request);document.addEventListener('focusout',motion.request);reduced.addEventListener('change',motion.request);
 new ResizeObserver(()=>{dirty=true;motion.request();}).observe(document.querySelector('main'));
 document.addEventListener('load',e=>{if(e.target instanceof HTMLImageElement){const group=e.target.closest('[data-rock-group]'),r=records.get(group);if(r){r.cache=null;r.generation++;warm(r);}}},true);
 new MutationObserver(rows=>{if(rows.some(row=>row.addedNodes.length||row.removedNodes.length))register();}).observe(document.querySelector('main'),{childList:true,subtree:true});
 new MutationObserver(motion.request).observe(body,{attributes:true,attributeFilter:['class']});register();
 document.fonts?.ready.then(invalidate);
})();

'use strict';
// A scroll-driven fracture front releases one row of matte stones at a time.
(() => {
 const motion=window.StratusMotion,body=document.body,reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const canvas=document.createElement('canvas');canvas.className='rock-canvas';canvas.setAttribute('aria-hidden','true');body.append(canvas);
 const context=canvas.getContext('2d',{alpha:true});if(!context)return;
 const records=new Map(),near=new Set(),active=new Set();let dirty=true,size=82,lastMetrics=0,totalMs=0,draws=0,worst=0;
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
 const outlines=[[[.12,.11],[.49,.02],[.84,.17],[.98,.48],[.8,.88],[.45,.97],[.08,.72],[.02,.4]],[[.22,.02],[.65,.09],[.96,.34],[.85,.7],[.58,.98],[.18,.88],[.03,.55],[.08,.25]],[[.08,.24],[.4,.04],[.78,.08],[.99,.5],[.72,.94],[.37,.86],[.04,.66],[.02,.42]]];
 function stonePath(ctx,x,y,s,seed,amount=1){const points=outlines[seed%outlines.length],square=[[0,0],[.5,0],[1,0],[1,.5],[1,1],[.5,1],[0,1],[0,.5]];ctx.beginPath();points.forEach(([px,py],j)=>{const a=square[j],xx=x+(a[0]+(px-a[0])*amount)*s,yy=y+(a[1]+(py-a[1])*amount)*s;j?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy);});ctx.closePath();}
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
   const front=focused?0:Math.max(0,r.el.matches('.immersive-hero')?-top*1.6:state.y-Math.max(0,b.y-state.h*.28));
   if(!r.cache){warm(r);continue;}if(front>0&&top+b.h> -size*3&&top<state.h){r.used=performance.now();list.push({r,front,top});}
  }return list.sort((a,b)=>(b.r.bounds.h+b.top)-(a.r.bounds.h+a.top)).slice(0,2);
 }
 function write(list,state){const start=performance.now();const width=Math.ceil(state.w),height=Math.ceil(state.h);
  if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
  context.clearRect(0,0,width,height);
  const current=new Set(list.map(x=>x.r));for(const r of active)if(!current.has(r)){r.el.classList.remove('rock-active');r.el.style.removeProperty('--rock-cut');}active.clear();
  let count=0,rows=0;const budget=state.w<650?100:180;
  for(const {r,front,top} of list){const b=r.bounds,cache=r.cache;active.add(r);r.el.classList.add('rock-active');
   // Clip only rows that have reached the fracture front; everything below remains live DOM.
   const cut=Math.min(cache.height,Math.ceil(front/size)*size);motion.style(r.el,'--rock-cut',`${cut.toFixed(1)}px`);
   for(let y=Math.max(0,Math.floor((front-size*1.7)/size)*size);y<Math.min(front,cache.height)&&count<budget;y+=size){
    const p=clamp((front-y)/(size*1.7));if(p>=1)continue;rows++;
    for(let x=0;x<b.w&&count<budget;x+=size){
    const i=Math.round(x/size)+Math.round(y/size)*31,s=Math.sin(i*12.9898),scatter=p*p,dx=(x+size/2-b.w/2)*scatter*.24+s*size*scatter*.6,dy=scatter*size*1.7;
    const px=b.x+x+dx,py=top+y+dy;if(py>height+size||py+size< -size||px>width+size||px+size< -size)continue;
    count++;context.save();context.globalAlpha=1-Math.pow(p,3);context.translate(px+size/2,py+size/2);context.rotate(s*scatter*.85);context.scale(1-scatter*.25,1-scatter*.25);
    const half=-size/2,shape=clamp(p*4);stonePath(context,half,half,size,i,shape);context.clip();
    const sw=Math.min(size,b.w-x),sh=Math.min(size,cache.height-y);context.drawImage(cache.bitmap,x*cache.scale,y*cache.scale,sw*cache.scale,sh*cache.scale,half,half,sw,sh);
    // Broad, uneven mineral planes. No outline, rim or glazed inset.
    context.fillStyle=`rgba(80,76,64,${shape*.38})`;context.fillRect(half,half,size,size);
    const ridgeX=half+size*(.36+(i%4)*.07),ridgeY=half+size*(.3+(i%3)*.09);
    context.beginPath();context.moveTo(half,half);context.lineTo(half+size,half);context.lineTo(ridgeX,ridgeY);context.lineTo(half,half+size*.67);context.closePath();context.fillStyle=`rgba(188,183,159,${shape*.18})`;context.fill();
    context.beginPath();context.moveTo(ridgeX,ridgeY);context.lineTo(half+size,half+size*.26);context.lineTo(half+size,half+size);context.lineTo(half+size*.32,half+size);context.closePath();context.fillStyle=`rgba(10,15,12,${shape*.42})`;context.fill();context.restore();
    }
   }
  }
  canvas.hidden=count===0;const ms=performance.now()-start;if(count){totalMs+=ms;draws++;worst=Math.max(worst,ms);}
  canvas.dataset.fragments=String(count);canvas.dataset.activeRows=String(rows);
  if(performance.now()-lastMetrics>500){canvas.dataset.drawMs=ms.toFixed(2);canvas.dataset.averageMs=(draws?totalMs/draws:0).toFixed(2);canvas.dataset.worstMs=worst.toFixed(2);canvas.dataset.cached=String([...records.values()].filter(r=>r.cache).length);lastMetrics=performance.now();}
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

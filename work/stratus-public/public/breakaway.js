'use strict';
// One page-wide fracture front. Scroll position controls all shards in both directions.
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
  const columns=Math.max(6,Math.round(width/115)),rows=4,cw=width/columns,ch=bandHeight/rows,points=[],shards=[];
  for(let j=0;j<=rows;j++){points[j]=[];for(let i=0;i<=columns;i++){const key=(index*rows+j)*83+i;points[j][i]=[i*cw+(i&&i<columns?(noise(key)-.5)*cw*.7:0),j*ch+(j&&j<rows?(noise(key+71)-.5)*ch*.7:0)];}}
  function add(p,seed){const xs=p.map(v=>v[0]),ys=p.map(v=>v[1]);shards.push({p,seed,x:(xs[0]+xs[1]+xs[2])/3,y:(ys[0]+ys[1]+ys[2])/3,min:Math.min(...ys)});}
  for(let j=0;j<rows;j++)for(let i=0;i<columns;i++){const a=points[j][i],b=points[j][i+1],c=points[j+1][i],d=points[j+1][i+1],seed=index*107+j*columns+i;if(noise(seed)>.5){add([a,b,c],seed);add([b,d,c],seed+41);}else{add([a,b,d],seed);add([a,d,c],seed+41);}}return shards;
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
  // Shared document coordinates carry the fracture through long sections and the footer.
  const maxScroll=Math.max(1,state.height-state.h),end=clamp((state.y/maxScroll-.86)/.14),front=state.y+Math.min(state.h*.36,state.y*.65)+end*state.h*.7;lastFront=front;
  const first=Math.max(0,Math.floor((front-state.h*.75)/bandHeight)),last=Math.floor((front+bandHeight*.5)/bandHeight);for(let i=first;i<=last;i++)warm(i);
  const ready=[...bands.values()].filter(b=>b.ready&&b.y<front+bandHeight&&b.y+bandHeight>front-state.h*.75),current=bands.get(Math.floor(front/bandHeight));return {front:current?.ready?front:0,ready};
 }
 function write({front,ready},state){
  if(canvas.width!==state.w||canvas.height!==state.h){canvas.width=state.w;canvas.height=state.h;}ctx.clearRect(0,0,canvas.width,canvas.height);
  for(const {el,y,h} of geometry){const cut=Math.min(h,Math.max(0,front-y));el.classList.toggle('glass-surface',cut>0);motion.style(el,'--glass-cut',`${cut.toFixed(1)}px`);}
  let count=0;const duration=Math.max(210,state.h*.47),budget=state.w<650?105:180;
  if(front>0)for(const band of ready)for(const shard of band.shards){
   const p=clamp((front-band.y-shard.min)/duration);if(p<=0||p>=1||count>=budget)continue;const turn=noise(shard.seed+19)*2-1,fall=p*p,dx=turn*fall*state.w*.18,dy=fall*duration*.7,x=shard.x+dx,y=band.y+shard.y-state.y+dy;if(y< -180||y>state.h+180)continue;
   count++;ctx.save();ctx.globalAlpha=(1-p*p)*.94;ctx.translate(x,y);ctx.rotate(turn*fall*1.3);ctx.scale(1-fall*.12,Math.max(.18,Math.cos(p*(.8+noise(shard.seed)*1.5))));const local=shard.p.map(([px,py])=>[px-shard.x,py-shard.y]);path(local);ctx.clip();
   ctx.drawImage(band.bitmap,0,0,band.bitmap.width,band.bitmap.height,-shard.x,-shard.y,width,bandHeight);
   ctx.fillStyle=`rgba(190,228,238,${.035+Math.sin(p*Math.PI)*.1})`;ctx.fill();path(local);ctx.strokeStyle=`rgba(220,249,255,${.25+Math.sin(p*Math.PI)*.5})`;ctx.lineWidth=.7;ctx.stroke();ctx.beginPath();ctx.moveTo(local[0][0],local[0][1]);ctx.lineTo(local[1][0],local[1][1]);ctx.strokeStyle='#f2ffffb0';ctx.lineWidth=1;ctx.stroke();ctx.restore();
  }
  canvas.hidden=count===0;canvas.dataset.shards=String(count);canvas.dataset.front=front.toFixed(0);canvas.dataset.cached=String(bands.size);
 }
 motion.register('glass-shatter',read,write);
 window.addEventListener('hashchange',invalidate);window.addEventListener('resize',invalidate,{passive:true});reduced.addEventListener('change',motion.request);document.addEventListener('focusin',motion.request);document.addEventListener('focusout',motion.request);
 document.addEventListener('load',e=>{if(e.target instanceof HTMLImageElement)invalidate();},true);document.addEventListener('stratus:scenes-updated',invalidate);
 new ResizeObserver(()=>{dirty=true;motion.request();}).observe(main);
 new MutationObserver(rows=>{if(rows.some(r=>r.addedNodes.length||r.removedNodes.length))invalidate();}).observe(main,{childList:true,subtree:true});
 new MutationObserver(motion.request).observe(body,{attributes:true,attributeFilter:['class']});document.fonts?.ready.then(invalidate);motion.request();
})();

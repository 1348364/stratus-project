'use strict';
// Two narrow viewport canvases keep the centre clear while glass drifts outwards.
(()=>{
 const motion=window.StratusMotion,body=document.body,reduced=matchMedia('(prefers-reduced-motion: reduce)'),coarse=matchMedia('(pointer: coarse)'),transparency=matchMedia('(prefers-reduced-transparency: reduce)');if(!motion)return;
 const edgeFraction=.10,edgeFadeFraction=.72,verticalFadeFraction=.10,renderResolution=()=>Math.min(3,Math.max(2,devicePixelRatio||1)),surfaces=['left','right'].map(side=>{const canvas=document.createElement('canvas');canvas.className=`shard-reflections shard-edge-${side}`;canvas.setAttribute('aria-hidden','true');body.append(canvas);return {side,canvas,ctx:canvas.getContext('2d',{alpha:true})};});if(surfaces.some(s=>!s.ctx))return;
 const canvas=surfaces[0].canvas,clamp=n=>Math.max(0,Math.min(1,n)),noise=n=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);},smooth=n=>{n=clamp(n);return n*n*(3-2*n);};
 const idle=fn=>'requestIdleCallback'in window?requestIdleCallback(fn,{timeout:500}):setTimeout(fn,24);
 const textures=new Map(),particles=new Map();let epoch=0,w=0,h=0,bandHeight=400,routeSeed=0,lastTick=0,lastDraw=0,gateAt=performance.now(),latestY=0,elapsed=0,timer=0,diagnosticAt=0,resolution=renderResolution();
 const disabled=s=>s.hidden||s.paused||reduced.matches||transparency.matches||location.hash==='#feedback'||document.activeElement?.matches('input,textarea,select,:focus-visible')||document.querySelector('dialog[open]');
 function schedule(){if(!timer)timer=setTimeout(()=>{timer=0;motion.request();},coarse.matches?42:32);}
 function invalidate(){epoch++;textures.clear();particles.clear();routeSeed=[...location.hash].reduce((s,c)=>s*31+c.charCodeAt(0),17)%100003;gateAt=performance.now();motion.request();}
 function setup(s){w=s.w;h=s.h;bandHeight=Math.max(300,Math.round(h*.55));invalidate();}
 function capture(index){
  if(index<0||textures.has(index))return;const version=epoch,record={index,y:index*bandHeight,ready:false,bitmap:null,readyAt:0,words:0,scale:1};textures.set(index,record);
  idle(()=>{
   if(version!==epoch||document.hidden||textures.get(index)!==record){if(textures.get(index)===record)textures.delete(index);return;}
   const scale=Math.min(resolution,(coarse.matches?1440:2880)/w),bitmap=document.createElement('canvas');bitmap.width=Math.ceil(w*scale);bitmap.height=Math.ceil(bandHeight*scale);const c=bitmap.getContext('2d');c.scale(scale,scale);c.fillStyle='#101817';c.fillRect(0,0,w,bandHeight);
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

 function path(ctx,points){ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();}
 function read(s){
  const nextResolution=renderResolution();if(w!==s.w||h!==s.h||resolution!==nextResolution){resolution=nextResolution;setup(s);}latestY=s.y;const off=disabled(s);
  if(!off){const first=Math.floor(s.y/bandHeight),last=Math.floor((s.y+s.h)/bandHeight);for(let i=first;i<=last;i++)capture(i);if(textures.size>4){const far=[...textures.values()].sort((a,b)=>Math.abs(b.y-latestY)-Math.abs(a.y-latestY));for(const old of far.slice(0,textures.size-4))textures.delete(old.index);}}return off;
 }
 function write(off,s){
  const now=performance.now(),edge=s.w*edgeFraction,interval=coarse.matches?40:30;
  if(off){for(const {canvas,ctx}of surfaces){canvas.hidden=true;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);}clearTimeout(timer);timer=0;lastTick=0;lastDraw=0;gateAt=now;return;}
  if(lastDraw&&now-lastDraw<interval){schedule();return;}
  const dt=lastTick?Math.min(60,now-lastTick):16;lastTick=now;lastDraw=now;elapsed+=dt;
  const gain=smooth((now-gateAt)/450),perSide=coarse.matches?13:26,report=now-diagnosticAt>250;if(report)diagnosticAt=now;let total=0,reflected=0;
  for(const {side,canvas,ctx}of surfaces){
   if(canvas.width!==Math.ceil(edge*resolution)||canvas.height!==Math.ceil(s.h*resolution)){canvas.width=Math.ceil(edge*resolution);canvas.height=Math.ceil(s.h*resolution);canvas.style.height=`${s.h}px`;ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality="high";}canvas.hidden=false;
   const right=side==='right',origin=right?s.w-edge:0;ctx.setTransform(resolution,0,0,resolution,-origin*resolution,0);ctx.clearRect(origin,0,edge,s.h);let count=0;const signature=[];
   for(let i=0;i<perSide;i++){
    const id=routeSeed+(right?200003:31)+i*173,duration=6500+noise(id+1)*5500,phase=elapsed/duration+noise(id+2),cycle=Math.floor(phase),t=phase-cycle,seed=id+cycle*3011;
    const key=(right?perSide:0)+i;let particle=particles.get(key);
    if(!particle||particle.seed!==seed){const width=Math.min(edge*.96,26+noise(seed)*76),height=width*(.45+noise(seed+1)*.40),n=noise(seed+3)<.48?3:noise(seed+3)<.86?4:5,points=[];for(let j=0;j<n;j++){const a=(j/n+(noise(seed+j+20)-.5)*.09)*Math.PI*2,r=.68+noise(seed+j+40)*.32;points.push([Math.cos(a)*width*.5*r,Math.sin(a)*height*.5*r]);}particle={seed,width,height,points};particles.set(key,particle);}
    const {width,height,points}=particle;
    const distance=edge*(.96-smooth(t)*1.48),x=right?s.w-distance:distance,y=((i+.12+noise(id+4)*.76)/perSide)*s.h+Math.sin(t*Math.PI*2+noise(seed)*6)*height*.3,turn=(noise(seed+5)-.5)*.8+t*(right?1:-1)*.3,opacity=gain*smooth(t/.18)*smooth((1-t)/.32);
    if(opacity<.008)continue;count++;if(report)signature.push(`${seed}:${x.toFixed(1)}`);ctx.save();ctx.translate(x,y);ctx.rotate(turn);path(ctx,points);ctx.clip();ctx.globalAlpha=opacity;
    const sourceY=s.y+clamp(y/s.h)*s.h,record=textures.get(Math.floor(sourceY/bandHeight)),sourceX=s.w*(right?.64+noise(seed+9)*.22:.14+noise(seed+9)*.22),zoom=1.08+noise(seed+8)*.48;
    if(record?.ready){const strength=clamp((now-record.readyAt)/230),anchorY=sourceY-record.y,rw=width*1.5/zoom,rh=height*1.7/zoom,left=Math.max(0,sourceX-rw*.5),top=Math.max(0,anchorY-rh*.5),end=Math.min(w,sourceX+rw*.5),bottom=Math.min(bandHeight,anchorY+rh*.5);ctx.save();ctx.globalAlpha=opacity*.98*strength;ctx.scale(-zoom,zoom*.94);if(end>left&&bottom>top)ctx.drawImage(record.bitmap,left*record.scale,top*record.scale,(end-left)*record.scale,(bottom-top)*record.scale,left-sourceX,top-anchorY,end-left,bottom-top);ctx.restore();reflected++;}
    ctx.fillStyle='rgba(183,230,207,.18)';ctx.fill();const sheen=ctx.createLinearGradient(-width*.5,-height*.5,width*.5,height*.5);sheen.addColorStop(0,'rgba(232,255,244,.58)');sheen.addColorStop(.35,'rgba(183,230,207,.16)');sheen.addColorStop(.7,'rgba(8,48,32,.30)');sheen.addColorStop(1,'rgba(210,255,231,.42)');ctx.fillStyle=sheen;ctx.fill();
    path(ctx,points);ctx.strokeStyle='rgba(3,24,16,.76)';ctx.lineWidth=3;ctx.stroke();ctx.strokeStyle='rgba(228,255,240,.94)';ctx.lineWidth=1.25;ctx.stroke();ctx.restore();
   }
   ctx.setTransform(resolution,0,0,resolution,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='destination-in';const fade=ctx.createLinearGradient(0,0,edge,0);fade.addColorStop(0,right?'transparent':'#000');fade.addColorStop(right?edgeFadeFraction:1-edgeFadeFraction,'#000');fade.addColorStop(1,right?'#000':'transparent');ctx.fillStyle=fade;ctx.fillRect(0,0,edge,s.h);
   const vertical=ctx.createLinearGradient(0,0,0,s.h);vertical.addColorStop(0,'transparent');vertical.addColorStop(verticalFadeFraction,'#000');vertical.addColorStop(1-verticalFadeFraction,'#000');vertical.addColorStop(1,'transparent');ctx.fillStyle=vertical;ctx.fillRect(0,0,edge,s.h);ctx.globalCompositeOperation='source-over';
   total+=count;if(report)Object.assign(canvas.dataset,{side,shards:String(count),reflected:String(reflected),cached:String([...textures.values()].filter(r=>r.ready).length),pattern:signature.join('.'),zonePercent:'10',renderScale:String(resolution),fadePercent:String(edgeFadeFraction*100),outward:'true',frame:String(Math.round(elapsed)),viewportY:String(s.y)});
  }
  if(report)canvas.dataset.totalShards=String(total);schedule();
 }
 motion.register('glass-shatter',read,write);
 window.addEventListener('hashchange',invalidate);reduced.addEventListener('change',motion.request);transparency.addEventListener('change',motion.request);document.addEventListener('focusin',motion.request);document.addEventListener('focusout',motion.request);
 document.addEventListener('load',e=>{if(e.target instanceof HTMLImageElement)invalidate();},true);document.fonts?.ready.then(invalidate);document.addEventListener('stratus:scenes-updated',invalidate);
 new MutationObserver(rows=>{if(rows.some(r=>r.addedNodes.length||r.removedNodes.length))invalidate();}).observe(document.querySelector('main'),{childList:true,subtree:true});
 new MutationObserver(motion.request).observe(body,{attributes:true,attributeFilter:['class']});motion.request();
})();

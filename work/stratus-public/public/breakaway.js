'use strict';
// Browser glass: live backdrop surfaces, without screenshots or clipping the page.
(()=>{
 const motion=window.StratusMotion,body=document.body,reduced=matchMedia('(prefers-reduced-motion: reduce)'),coarse=matchMedia('(pointer: coarse)');
 if(!motion)return;
 const layer=document.createElement('div');layer.className='liquid-fragments';layer.setAttribute('aria-hidden','true');body.append(layer);
 const clamp=n=>Math.max(0,Math.min(1,n)),noise=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);};
 let pieces=[],lastWidth=0,lastHeight=0,animatedY=scrollY,lastTick=0,reset=true;
 function roundedPath(points,radius){
  const corners=points.map((p,i)=>{const prev=points[(i+points.length-1)%points.length],next=points[(i+1)%points.length],a=Math.hypot(prev[0]-p[0],prev[1]-p[1]),b=Math.hypot(next[0]-p[0],next[1]-p[1]),r=Math.min(radius,a*.12,b*.12);return {p,entry:[p[0]+(prev[0]-p[0])*r/a,p[1]+(prev[1]-p[1])*r/a],exit:[p[0]+(next[0]-p[0])*r/b,p[1]+(next[1]-p[1])*r/b]};});
  return `M${corners[0].entry.join(',')} `+corners.map(({p,entry,exit},i)=>`${i?'L'+entry.join(','):''}Q${p.join(',')} ${exit.join(',')}`).join(' ')+'Z';
 }
 function build(s){
  lastWidth=s.w;lastHeight=s.h;layer.replaceChildren();pieces=[];
  const count=s.w<650?9:15;
  for(let i=0;i<count;i++){
   const seed=i*19+11,w=(s.w<650?48:72)+noise(seed)*150,h=32+noise(seed+2)*Math.min(90,s.h*.12),el=document.createElement('i');
   const points=i%3===0?[[w*.08,h*.12],[w*.94,0],[w*.65,h*.96],[w*.02,h*.64]]:[[w*.04,h*.15],[w*.96,h*.02],[w*(.25+noise(seed+5)*.5),h*.97]];
   const d=roundedPath(points,5),edge=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs><linearGradient id="e" x2=".8" y2="1"><stop stop-color="white" stop-opacity=".55"/><stop offset=".36" stop-color="white" stop-opacity=".06"/><stop offset=".72" stop-color="white" stop-opacity=".02"/><stop offset="1" stop-color="white" stop-opacity=".25"/></linearGradient></defs><path d="${d}" fill="none" stroke="url(#e)" stroke-width="1.25"/></svg>`;
   el.className='liquid-fragment';el.style.width=`${w}px`;el.style.height=`${h}px`;el.style.clipPath=`path('${d}')`;el.style.setProperty('--glass-edge',`url("data:image/svg+xml,${encodeURIComponent(edge)}")`);layer.append(el);
   el.style.opacity='0';pieces.push({el,w,h,x:(i+.5)/count,seed,phase:noise(seed+8),range:260+noise(seed+3)*230,turn:(noise(seed+4)-.5)*34,opacity:0});
  }
  layer.dataset.pieces=String(count);
 }
 function read(s){
  const disabled=reduced.matches||s.paused||s.hidden||location.hash==='#feedback'||document.activeElement?.matches('input,textarea,select,:focus-visible')||document.querySelector('dialog[open]');
  return {disabled,resize:lastWidth!==s.w||lastHeight!==s.h};
 }
 function write({disabled,resize},s){
  if(resize){build(s);reset=true;}
  const now=performance.now(),dt=lastTick?Math.min(40,now-lastTick):16;lastTick=now;
  layer.hidden=disabled||s.y<4;
  if(layer.hidden){animatedY=s.y;reset=true;for(const p of pieces){p.opacity=0;motion.style(p.el,'opacity','0');}return;}
  // New routes and large jumps begin clear, rather than spawning a completed fracture.
  if(reset||Math.abs(s.y-animatedY)>s.h*1.3){animatedY=s.y;for(const p of pieces)p.opacity=0;reset=false;}
  animatedY+=(s.y-animatedY)*(1-Math.exp(-dt/110));
  let settling=Math.abs(s.y-animatedY)>.2;
  const zone=s.h*.25,gain=clamp((animatedY-25)/180),mobile=coarse.matches?.65:1;let visible=0;
  for(const p of pieces){
   // Reversible positions follow scroll distance, with staggered sizes and timings.
   const t=((animatedY/p.range+p.phase)%1+1)%1,y=zone*(.85-t*1.2)-p.h*.35,angle=p.turn*(t-.5),drift=Math.sin(t*Math.PI)*(noise(p.seed+6)-.5)*55,x=p.x*s.w-p.w*.5+drift;
   const fade=Math.sin(t*Math.PI)**2,target=gain*fade*.66*mobile;
   p.opacity+=(target-p.opacity)*(1-Math.exp(-dt/(190+noise(p.seed+9)*120)));
   if(Math.abs(target-p.opacity)>.002)settling=true;
   motion.style(p.el,'transform',`translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0) rotate(${angle.toFixed(2)}deg)`);motion.style(p.el,'opacity',p.opacity.toFixed(3));
   // Every piece becomes fully transparent before the quarter-height limit.
   const fadeEnd=Math.max(0,zone-24-y-p.w*Math.abs(Math.sin(angle*Math.PI/180))*.5),fadeStart=Math.max(0,fadeEnd-55);
   motion.style(p.el,'--fade-start',`${fadeStart.toFixed(1)}px`);motion.style(p.el,'--fade-end',`${fadeEnd.toFixed(1)}px`);motion.style(p.el,'--shine',`${(t*100).toFixed(1)}%`);if(p.opacity>.03&&y+p.h>0)visible++;
  }
  layer.dataset.visible=String(visible);layer.dataset.zoneHeight=zone.toFixed(1);layer.dataset.settling=String(settling);if(settling)motion.request();
 }
 motion.register('glass-shatter',read,write);
 window.addEventListener('hashchange',()=>{reset=true;motion.request();});reduced.addEventListener('change',motion.request);document.addEventListener('focusin',motion.request);document.addEventListener('focusout',motion.request);
 new MutationObserver(motion.request).observe(body,{attributes:true,attributeFilter:['class']});motion.request();
})();

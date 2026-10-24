'use strict';
// The navigation splits: its left piece travels to the logo, while the remainder closes at the right.
(()=>{
 const header=document.querySelector('.topbar'),motion=window.StratusMotion,reduced=matchMedia('(prefers-reduced-motion: reduce)');if(!header||!motion)return;
 const brand=header.querySelector('.brand'),nav=header.querySelector('nav'),links=[...nav.querySelectorAll('a')],label=brand.querySelector('span');if(!brand||!nav||!links.length)return;
 const cluster=document.createElement('div');cluster.className='brand-cluster';brand.before(cluster);cluster.append(brand);label.classList.add('brand-label');
 const toggle=document.createElement('button');toggle.type='button';toggle.className='nav-expand';toggle.setAttribute('aria-label','Expand navigation');toggle.setAttribute('aria-expanded','true');toggle.setAttribute('aria-controls','public-navigation');toggle.innerHTML='<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M6 4.5 12 9 6 13.5Z"/></svg>';cluster.append(toggle);nav.id='public-navigation';
 const track=document.createElement('div');track.className='nav-track';track.append(...links);nav.append(track);const backplate=document.createElement('div');backplate.className='nav-backplate';backplate.setAttribute('aria-hidden','true');nav.prepend(backplate);nav.classList.add('nav-split-frame');header.classList.add('navigation-ready');
 const traveller=document.createElement('div');traveller.className='nav-traveller';traveller.setAttribute('aria-hidden','true');traveller.innerHTML='<span class="nav-flight-label"></span><span class="nav-flight-arrow">'+toggle.innerHTML+'</span>';traveller.querySelector('.nav-flight-label').textContent=links[0].textContent;header.append(traveller);
 let manual=false,lastY=scrollY,mode='',flight=null,flightEffects=[];
 function stopFlight(){for(const effect of flightEffects)effect.cancel();flightEffects=[];flight=null;traveller.style.visibility='hidden';}
 function animateSplit(v){
  if(v.paused){stopFlight();return;}
  traveller.style.visibility='visible';
  if(flight){for(const effect of flightEffects){effect.playbackRate=v.compact?1:-1;effect.play();}return;}
  if(!v.compact){traveller.style.visibility='hidden';return;}
  // Sample the annotated curved route, keeping animation on a single decorative fragment.
  const start={x:v.inset+v.available-v.fullWidth+v.pieceWidth/2,y:v.openTop+28},end={x:v.inset+74,y:v.brandTop+28},depth=Math.min(250,v.available*.22),frames=[];
  const c1={x:start.x+Math.min(20,v.inset),y:start.y+depth},c2={x:end.x+Math.min(170,v.available*.3),y:Math.max(start.y,end.y)+depth};
  for(let i=0;i<=30;i++){const t=i/30,u=1-t,e=t*t*(3-2*t),w=v.pieceWidth+(44-v.pieceWidth)*e,h=56-12*e,x=u*u*u*start.x+3*u*u*t*c1.x+3*u*t*t*c2.x+t*t*t*end.x,y=u*u*u*start.y+3*u*u*t*c1.y+3*u*t*t*c2.y+t*t*t*end.y;frames.push({offset:t,transform:`translate3d(${x-w/2}px,${y-h/2}px,0)`,width:`${w}px`,height:`${h}px`,opacity:t<.88?1:(1-t)/.12});}
  const timing={duration:900,fill:'both',easing:'linear'};
  flight=traveller.animate(frames,timing);
  const labelFlight=traveller.querySelector('.nav-flight-label').animate([{opacity:1,offset:0},{opacity:0,offset:.23},{opacity:0,offset:1}],timing),arrowFlight=traveller.querySelector('.nav-flight-arrow').animate([{opacity:0,offset:0},{opacity:0,offset:.4},{opacity:1,offset:.75},{opacity:1,offset:1}],timing);
  const cut=backplate.animate([{clipPath:`inset(0 0 0 ${v.pieceWidth}px round 28px)`,offset:0},{clipPath:'inset(0 0 0 0px round 28px)',offset:.48},{clipPath:'inset(0 0 0 0px round 28px)',offset:1}],timing);
  flightEffects=[flight,labelFlight,arrowFlight,cut];
  flight.onfinish=()=>{if(flight.playbackRate<0)stopFlight();else traveller.style.visibility='hidden';};
 }

 function read(s){
  const changed=Math.abs(s.y-lastY)>1;lastY=s.y;if(changed)manual=false;
  const view=document.querySelector('[data-view]:not([hidden])'),anchor=view?.querySelector('.immersive-hero,.section-intro'),bottom=anchor?.getBoundingClientRect().bottom??1,past=bottom<=0;
  if(!past)manual=false;const compact=past&&!manual,active=nav.querySelector('[aria-current=page]')||links[0],inset=Math.max(12,s.w*.04),available=s.w-inset*2,fullWidth=Math.min(track.scrollWidth+12,available),narrow=available<185+fullWidth+24,closedWidth=active.offsetWidth+12,openTop=narrow?76:14,brandTop=narrow?10:14;
  return {compact,past,active,mode:compact?'compact':past?'peek':'open',inset,available,fullWidth,narrow,openTop,brandTop,pieceWidth:links[0].offsetWidth+12,y:compact?brandTop:openTop,width:compact?closedWidth:fullWidth,shift:compact?-active.offsetLeft:0,paused:s.paused||reduced.matches};
 }
 function write(v){
  const changed=mode!==v.mode,splitChanged=(mode==='compact')!==v.compact,hadMode=!!mode;
  if(changed){mode=v.mode;header.dataset.navMode=mode;header.classList.toggle('nav-compact',v.compact);header.classList.toggle('nav-peek',mode==='peek');const expanderFocused=document.activeElement===toggle;toggle.setAttribute('aria-expanded',String(!v.compact));toggle.setAttribute('aria-label','Expand navigation');toggle.tabIndex=v.compact?0:-1;toggle.setAttribute('aria-hidden',String(!v.compact));if(!v.compact&&expanderFocused)v.active.focus({preventScroll:true});toggle.inert=!v.compact;
   if(v.compact&&links.includes(document.activeElement)&&document.activeElement!==v.active)toggle.focus({preventScroll:true});
   if(v.compact)nav.scrollLeft=0;
   for(const link of links){const hide=v.compact&&link!==v.active;link.inert=hide;link.tabIndex=hide?-1:0;if(hide)link.setAttribute('aria-hidden','true');else link.removeAttribute('aria-hidden');}
  }
  motion.style(header,'--header-inset',`${v.inset}px`);motion.style(nav,'--nav-top',`${v.y}px`);
  motion.style(nav,'--nav-width',`${v.width}px`);motion.style(track,'--nav-track-shift',`${v.shift}px`);
  header.classList.toggle('nav-stacked',v.narrow);header.classList.toggle('nav-motion-off',v.paused);
  if(v.paused&&flight)stopFlight();else if(splitChanged&&hadMode)animateSplit(v);
 }
 motion.register('compact-navigation',read,write);
 toggle.addEventListener('click',()=>{manual=!manual;lastY=scrollY;motion.request();});
 header.addEventListener('keydown',e=>{if(e.key==='Escape'&&manual){manual=false;motion.request();}});
 nav.addEventListener('click',e=>{const link=e.target.closest('a');if(link){if(link.getAttribute('href')===location.hash){e.preventDefault();window.scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'});}manual=false;motion.request();}});
 brand.addEventListener('click',e=>{if(location.hash==='#overview'){e.preventDefault();window.scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'});}});
 window.addEventListener('hashchange',()=>{manual=false;lastY=scrollY;motion.request();});reduced.addEventListener('change',motion.request);document.fonts?.ready.then(motion.request);
 new MutationObserver(motion.request).observe(nav,{subtree:true,attributes:true,attributeFilter:['aria-current']});motion.request();
})();

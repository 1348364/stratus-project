'use strict';
// The original header returns at the hero; a temporary peek closes on the next scroll.
(()=>{
 const header=document.querySelector('.topbar'),motion=window.StratusMotion,reduced=matchMedia('(prefers-reduced-motion: reduce)');if(!header||!motion)return;
 const brand=header.querySelector('.brand'),nav=header.querySelector('nav'),links=[...nav.querySelectorAll('a')],label=brand.querySelector('span');if(!brand||!nav||!links.length)return;
 const cluster=document.createElement('div');cluster.className='brand-cluster';brand.before(cluster);cluster.append(brand);label.classList.add('brand-label');
 const toggle=document.createElement('button');toggle.type='button';toggle.className='nav-expand';toggle.setAttribute('aria-label','Expand navigation');toggle.setAttribute('aria-expanded','true');toggle.setAttribute('aria-controls','public-navigation');toggle.innerHTML='<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M6 4.5 12 9 6 13.5Z"/></svg>';cluster.append(toggle);nav.id='public-navigation';
 const track=document.createElement('div');track.className='nav-track';track.append(...links);nav.append(track);header.classList.add('navigation-ready');
 let manual=false,lastY=scrollY,mode='';
 function read(s){
  const changed=Math.abs(s.y-lastY)>1;lastY=s.y;if(changed)manual=false;
  const view=document.querySelector('[data-view]:not([hidden])'),anchor=view?.querySelector('.immersive-hero,.section-intro'),bottom=anchor?.getBoundingClientRect().bottom??1,past=bottom<=0;
  if(!past)manual=false;const compact=past&&!manual,active=nav.querySelector('[aria-current=page]')||links[0],narrow=s.w<=760,inset=Math.max(12,s.w*.04),fullWidth=Math.min(track.scrollWidth+12,s.w-inset*2),closedWidth=active.offsetWidth+12;
  return {compact,past,active,mode:compact?'compact':past?'peek':'open',inset,y:narrow?(compact?10:76):14,width:compact?closedWidth:fullWidth,shift:compact?-active.offsetLeft:0,paused:s.paused||reduced.matches};
 }
 function write(v){
  const changed=mode!==v.mode;
  if(changed){mode=v.mode;header.dataset.navMode=mode;header.classList.toggle('nav-compact',v.compact);header.classList.toggle('nav-peek',mode==='peek');const expanderFocused=document.activeElement===toggle;toggle.setAttribute('aria-expanded',String(!v.compact));toggle.setAttribute('aria-label','Expand navigation');toggle.tabIndex=v.compact?0:-1;toggle.setAttribute('aria-hidden',String(!v.compact));if(!v.compact&&expanderFocused)v.active.focus({preventScroll:true});toggle.inert=!v.compact;
   if(v.compact&&links.includes(document.activeElement)&&document.activeElement!==v.active)toggle.focus({preventScroll:true});
   if(v.compact)nav.scrollLeft=0;
   for(const link of links){const hide=v.compact&&link!==v.active;link.inert=hide;link.tabIndex=hide?-1:0;if(hide)link.setAttribute('aria-hidden','true');else link.removeAttribute('aria-hidden');}
  }
  motion.style(header,'--header-inset',`${v.inset}px`);motion.style(nav,'--nav-top',`${v.y}px`);
  motion.style(nav,'--nav-width',`${v.width}px`);motion.style(track,'--nav-track-shift',`${v.shift}px`);
  header.classList.toggle('nav-motion-off',v.paused);
 }
 motion.register('compact-navigation',read,write);
 toggle.addEventListener('click',()=>{manual=!manual;lastY=scrollY;motion.request();});
 header.addEventListener('keydown',e=>{if(e.key==='Escape'&&manual){manual=false;motion.request();}});
 nav.addEventListener('click',e=>{const link=e.target.closest('a');if(link){if(link.getAttribute('href')===location.hash){e.preventDefault();window.scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'});}manual=false;motion.request();}});
 brand.addEventListener('click',e=>{if(location.hash==='#overview'){e.preventDefault();window.scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'});}});
 window.addEventListener('hashchange',()=>{manual=false;lastY=scrollY;motion.request();});reduced.addEventListener('change',motion.request);document.fonts?.ready.then(motion.request);
 new MutationObserver(motion.request).observe(nav,{subtree:true,attributes:true,attributeFilter:['aria-current']});motion.request();
})();

'use strict';
// Standalone visual effects. No model calls, external assets or scroll interception.
(()=>{
 const root=document.documentElement,body=document.body,hero=document.querySelector('.immersive-hero'),button=document.querySelector('#motion-control');
 const preference=matchMedia('(prefers-reduced-motion: reduce)');let paused=preference.matches,frame=0,targetX=0,targetY=0;
 function routeStyle(){body.classList.toggle('internal-page',!!location.hash&&!['#overview','#main','#discover'].includes(location.hash));schedule();}
 function update(){frame=0;const active=!paused&&!preference.matches;body.classList.toggle('effects-paused',!active);button.textContent=`MOTION: ${active?'ON':'OFF'}`;button.setAttribute('aria-pressed',String(active));
  if(!hero)return;const rect=hero.getBoundingClientRect(),amount=Math.max(0,Math.min(1,-rect.top/Math.max(1,rect.height)));
  root.style.setProperty('--hero-travel',active?`${amount*70}px`:'0px');root.style.setProperty('--depth-blur',active?`${amount*4}px`:'0px');root.style.setProperty('--scroll-fade',String(1-amount*.65));
  root.style.setProperty('--camera-x',active?`${targetX}px`:'0px');root.style.setProperty('--camera-y',active?`${targetY}px`:'0px');
 }
 function schedule(){if(!frame)frame=requestAnimationFrame(update);}
 button.addEventListener('click',()=>{paused=!paused;schedule();});preference.addEventListener('change',()=>{paused=preference.matches;schedule();});
 hero?.addEventListener('pointermove',event=>{if(event.pointerType!=='mouse'||paused||preference.matches)return;const box=hero.getBoundingClientRect();targetX=(event.clientX/innerWidth-.5)*12;targetY=((event.clientY-box.top)/box.height-.5)*10;schedule();},{passive:true});
 hero?.addEventListener('pointerleave',()=>{targetX=0;targetY=0;schedule();});
 window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});window.addEventListener('hashchange',routeStyle);routeStyle();
})();

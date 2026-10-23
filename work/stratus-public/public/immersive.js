'use strict';
// Standalone visual effects. No model calls, external assets or scroll interception.
(()=>{
 const root=document.documentElement,body=document.body,hero=document.querySelector('.immersive-hero'),button=document.querySelector('#motion-control');
 const motion=window.StratusMotion,preference=matchMedia('(prefers-reduced-motion: reduce)');let paused=preference.matches,targetX=0,targetY=0;
 function routeStyle(){body.classList.toggle('internal-page',!!location.hash&&!['#overview','#main','#discover'].includes(location.hash));schedule();}
 function update(){const active=!paused&&!preference.matches;body.classList.toggle('effects-paused',!active);const label=`MOTION: ${active?'ON':'OFF'}`;if(button.textContent!==label)button.textContent=label;button.setAttribute('aria-pressed',String(active));
  motion.style(root,'--camera-x',active?`${targetX}px`:'0px');motion.style(root,'--camera-y',active?`${targetY}px`:'0px');
 }
 const schedule=motion.request;motion.register('hero',null,update);
 button.addEventListener('click',()=>{paused=!paused;schedule();});preference.addEventListener('change',()=>{paused=preference.matches;schedule();});
 hero?.addEventListener('pointermove',event=>{if(event.pointerType!=='mouse'||paused||preference.matches)return;targetX=(event.clientX/innerWidth-.5)*12;targetY=(event.clientY/innerHeight-.5)*10;schedule();},{passive:true});
 hero?.addEventListener('pointerleave',()=>{targetX=0;targetY=0;schedule();});
 window.addEventListener('hashchange',routeStyle);routeStyle();
})();

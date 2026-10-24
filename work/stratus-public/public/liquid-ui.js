'use strict';
// A single pointer light follows the active glass surface; no idle animation loop.
(()=>{
 const motion=window.StratusMotion,reduced=matchMedia('(prefers-reduced-motion: reduce)');if(!motion)return;
 const selector='.button,.topbar .brand-cluster,.topbar nav,.workspace-card,.spec-section,.release,.upcoming-item,.live-release,.faq-list details,.feedback-form,.carousel-controls button,.text-link';let pointer=null,previous=null;
 document.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||reduced.matches||document.body.classList.contains('effects-paused'))return;const el=e.target.closest(selector);pointer=el?{el,x:e.clientX,y:e.clientY}:null;motion.request();},{passive:true});
 document.addEventListener('pointerleave',()=>{pointer=null;motion.request();});
 motion.register('glass-light',()=>{if(!pointer||!pointer.el.isConnected||document.hidden||reduced.matches||document.body.classList.contains('effects-paused'))return null;const b=pointer.el.getBoundingClientRect();return b.width&&b.height?{el:pointer.el,x:(pointer.x-b.left)/b.width*100,y:(pointer.y-b.top)/b.height*100}:null;},data=>{
  if(previous&&previous!==data?.el){previous.style.removeProperty('--lg-x');previous.style.removeProperty('--lg-y');}previous=data?.el||null;
  if(data){motion.style(data.el,'--lg-x',`${data.x.toFixed(1)}%`);motion.style(data.el,'--lg-y',`${data.y.toFixed(1)}%`);}
 });
})();

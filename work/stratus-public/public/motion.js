'use strict';
// Scroll seeks paused compositor animations, so every reveal can replay and reverse.
(()=>{
 const motion=window.StratusMotion,body=document.body,root=document.documentElement,reduced=matchMedia('(prefers-reduced-motion: reduce)');if(!motion)return;
 const groups=[['.hero-content','rise'],['.gallery-section,.water-story-copy,.water-story-image,.preset-guide,.spec-footnote','wipe'],['.workspace-card,.spec-section,.release,.upcoming-item,.roadmap-process li,.faq-list details','rise'],['.home-heading h2,.section-intro h1','heading'],['.reference-strip,.platform-strip,.workflow-note,.roadmap-note','line'],['.showcase-shot','wipe'],['.eyebrow,.chapter-label','detail']];
 const records=new Map(),active=new Set();let observer,dirty=true,lastWidth=0,lastHeight=0,lastPaused=null,scrolled=false;
 const clamp=n=>Math.max(0,Math.min(1,n)),disabled=()=>reduced.matches||body.classList.contains('effects-paused');
 function make(el,type){
  const from=type==='line'?'translateY(10px) scale(.985)':type==='heading'?'translateY(22px)':type==='detail'?'translateY(10px)':type==='wipe'?'translateY(26px) scale(.99)':'translateY(34px)';
  const animation=el.animate([{opacity:0,transform:from},{opacity:1,transform:'translate(0,0) scale(1)'}],{duration:1000,fill:'both',easing:'cubic-bezier(.2,.65,.25,1)'});animation.pause();animation.currentTime=disabled()?1000:0;
  el.dataset.reveal=type;el.classList.add('scroll-reveal','is-revealed');const record={el,animation,top:0,height:0,p:-1};records.set(el,record);observer?.observe(el);active.add(record);
 }
 function register(){
  for(const [el,r] of records)if(!el.isConnected){r.animation.cancel();observer?.unobserve(el);active.delete(r);records.delete(el);}
  for(const [selector,type] of groups)for(const el of document.querySelectorAll(selector)){if(records.has(el)||el.parentElement.closest('[data-reveal]'))continue;make(el,type);}
  dirty=true;motion.request();
 }
 if('IntersectionObserver'in window)observer=new IntersectionObserver(entries=>{for(const e of entries){const r=records.get(e.target);if(!r)continue;if(e.isIntersecting)active.add(r);else{active.delete(r);if(!disabled()&&!r.el.contains(document.activeElement)){r.animation.currentTime=0;r.p=0;r.el.dataset.revealProgress='0';}}}motion.request();},{rootMargin:'25% 0px 25% 0px'});
 function measure(s){for(const r of records.values()){if(r.el.closest('[data-view][hidden]'))continue;const b=r.el.getBoundingClientRect();const matrix=getComputedStyle(r.el).transform,offset=matrix==='none'?0:new DOMMatrixReadOnly(matrix).m42;r.top=b.top+s.y-offset;r.height=r.el.offsetHeight;}lastWidth=s.w;lastHeight=s.h;dirty=false;}
 motion.register('reversible-reveals',s=>{
  const paused=disabled();if(paused!==lastPaused){lastPaused=paused;for(const r of records.values()){r.animation.currentTime=1000;r.p=1;r.el.dataset.revealProgress='1';}dirty=true;}
  if(dirty||lastWidth!==s.w||lastHeight!==s.h)measure(s);
  const values=[];for(const r of active){if(r.el.closest('[data-view][hidden]'))continue;const top=r.top-s.y,bottom=top+r.height,pinned=r.el.contains(document.activeElement)||r.el.closest('form')?.contains(document.activeElement);const enter=clamp((s.h*.98-top)/(s.h*.24)),leave=clamp((bottom-s.h*.12)/(s.h*.18));values.push([r,paused||pinned?1:Math.min(enter,leave)]);}return {values,progress:clamp(s.y/Math.max(1,s.height-s.h)),hasScrolled:s.y>24};
 },({values,progress,hasScrolled})=>{motion.style(root,'--read-progress',progress);if(scrolled!==hasScrolled){scrolled=hasScrolled;body.classList.toggle('has-scrolled',scrolled);}for(const [r,p] of values)if(Math.abs(r.p-p)>.001){r.p=p;r.animation.currentTime=p*1000;r.el.dataset.revealProgress=p.toFixed(3);}});
 body.classList.add('motion-enabled','scroll-scrub');register();
 window.addEventListener('hashchange',()=>{dirty=true;motion.request();});window.addEventListener('resize',()=>{dirty=true;motion.request();},{passive:true});reduced.addEventListener('change',motion.request);
 document.addEventListener('focusin',motion.request);document.addEventListener('focusout',motion.request);document.addEventListener('load',()=>{dirty=true;motion.request();},true);document.fonts?.ready.then(()=>{dirty=true;motion.request();});
 new ResizeObserver(()=>{dirty=true;motion.request();}).observe(document.querySelector('main'));
 new MutationObserver(rows=>{if(rows.some(r=>r.addedNodes.length||r.removedNodes.length))register();}).observe(document.querySelector('main'),{childList:true,subtree:true});
 new MutationObserver(()=>{const p=disabled();if(p!==lastPaused)motion.request();}).observe(body,{attributes:true,attributeFilter:['class']});
})();

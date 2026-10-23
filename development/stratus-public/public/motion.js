'use strict';
// Presentation only. Dynamic feed elements join the same finite reveal system.
(() => {
 const preference=matchMedia('(prefers-reduced-motion: reduce)'),root=document.documentElement,body=document.body;
 const groups=[['.home-heading h2,.section-intro h1,.water-story-copy h2','heading'],['.eyebrow,.chapter-label','tracking'],['.workspace-card,.upcoming-item,.roadmap-process li','rise'],['.reference-strip,.platform-strip,.workflow-note,.roadmap-note','line'],['.gallery-section,.showcase-shot,.water-story-image','wipe'],['.release','slide'],['.spec-section,.preset-guide,.spec-footnote','soft'],['.spec-section dl>div,.preset-guide tbody tr,.faq-list details,.feedback-form>label,.feedback-form>input,.feedback-form>textarea,.feedback-form>select','detail']];
 let observer,frame=0;
 const disabled=()=>preference.matches||body.classList.contains('effects-paused');
 function update(){frame=0;const height=innerHeight,range=Math.max(1,root.scrollHeight-height);root.style.setProperty('--read-progress',Math.min(1,Math.max(0,scrollY/range)));body.classList.toggle('has-scrolled',scrollY>24);}
 function schedule(){if(!frame)frame=requestAnimationFrame(update);}
 function register(){for(const [selector,type] of groups){document.querySelectorAll(selector).forEach((el,index)=>{if(el.dataset.reveal)return;el.dataset.reveal=type;el.classList.add('scroll-reveal');el.style.setProperty('--reveal-delay',`${index%3*65}ms`);if(disabled()||!observer)el.classList.add('is-revealed');else observer.observe(el);});}schedule();}
 function setup(){observer?.disconnect();body.classList.toggle('motion-enabled',!preference.matches&&'IntersectionObserver'in window);observer='IntersectionObserver'in window?new IntersectionObserver(entries=>{for(const entry of entries){if(!entry.isIntersecting||entry.target.closest('[data-view][hidden]'))continue;entry.target.classList.add('is-revealed');observer.unobserve(entry.target);}},{threshold:.05,rootMargin:'0px 0px -15px 0px'}):null;
  for(const el of document.querySelectorAll('[data-reveal]')){if(disabled())el.classList.add('is-revealed');else if(!el.classList.contains('is-revealed'))observer?.observe(el);}register();}
 window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});window.addEventListener('hashchange',()=>requestAnimationFrame(register));preference.addEventListener('change',setup);
 document.addEventListener('focusin',e=>{let el=e.target;while(el&&el!==body){if(el.dataset?.reveal)el.classList.add('is-revealed');el=el.parentElement;}});
 new MutationObserver(records=>{if(records.some(r=>r.type==='childList'&&r.addedNodes.length))register();}).observe(document.querySelector('main'),{childList:true,subtree:true});
 new MutationObserver(()=>{if(disabled())document.querySelectorAll('[data-reveal]').forEach(el=>el.classList.add('is-revealed'));}).observe(body,{attributes:true,attributeFilter:['class']});setup();
})();

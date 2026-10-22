'use strict';
// Presentation only: native scrolling, no network requests or persistent state.
(() => {
 const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
 const root = document.documentElement;
 const revealSelectors = '.home-heading,.workspace-card,.reference-strip,.gallery .scene,.section-intro,.showcase-shot,.release,.spec-section,.platform-strip,.spec-footnote,.upcoming-item,.water-story-image,.water-story-copy,.public-faq .home-heading,.faq-list details,.release-focus>div,.preset-guide,.roadmap-process>h2,.roadmap-process li,.workflow-note,.roadmap-note';
 const reveals = [...document.querySelectorAll(revealSelectors)];
 const layers = [...document.querySelectorAll('.hero,.water-story-image,.showcase-image')];
 let observer, frame = 0, resizeObserver;
 function visible(element) { return !element.closest('[data-view][hidden]'); }
 function update() {
  frame = 0;
  const height = window.innerHeight;
  const range = Math.max(1, document.documentElement.scrollHeight - height);
  root.style.setProperty('--read-progress', String(Math.min(1, Math.max(0, window.scrollY / range))));
  document.body.classList.toggle('has-scrolled', window.scrollY > 24);
  if (preference.matches) return;
  for (const layer of layers) {
   if (!visible(layer)) continue;
   const box = layer.getBoundingClientRect();
   if (box.bottom < 0 || box.top > height) continue;
   const travel = (height / 2 - (box.top + box.height / 2)) / height;
   const maximum = window.innerWidth < 600 ? 12 : 25;
   layer.style.setProperty('--scene-shift', `${Math.max(-maximum, Math.min(maximum, travel * maximum))}px`);
  }
 }
 function schedule() { if (!frame) frame = requestAnimationFrame(update); }
 function setup() {
  observer?.disconnect();
  document.body.classList.toggle('motion-enabled', !preference.matches && 'IntersectionObserver' in window);
  if (preference.matches || !('IntersectionObserver' in window)) {
   reveals.forEach(element => element.classList.add('is-revealed'));
   layers.forEach(element => element.style.removeProperty('--scene-shift'));
   schedule(); return;
  }
  observer = new IntersectionObserver(entries => {
   for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    entry.target.classList.add('is-revealed');
    observer.unobserve(entry.target);
   }
  }, {threshold:0.06, rootMargin:'0px 0px -20px 0px'});
  reveals.forEach((element,index) => {
   element.classList.add('scroll-reveal');
   // Small offsets make grouped cards and gallery scenes arrive in sequence.
   const siblings = element.parentElement?.children;
   const stagger = siblings ? [...siblings].indexOf(element) % 3 : index % 3;
   element.style.setProperty('--reveal-delay', `${stagger * 65}ms`);
   if (!element.classList.contains('is-revealed')) observer.observe(element);
  });
  schedule();
 }
 function routeMotion() {
  // Pages already read remain revealed. First visits animate on entry.
  requestAnimationFrame(() => {
   for (const element of reveals) if (visible(element) && !element.classList.contains('is-revealed')) observer?.observe(element);
   schedule();
  });
 }
 window.addEventListener('scroll',schedule,{passive:true});
 window.addEventListener('resize',schedule,{passive:true});
 window.addEventListener('hashchange',routeMotion);
 window.addEventListener('load',schedule,{once:true});
 preference.addEventListener('change',setup);
 if ('ResizeObserver' in window) {resizeObserver=new ResizeObserver(schedule);resizeObserver.observe(document.body);}
 document.addEventListener('focusin',event=>event.target.closest?.('.scroll-reveal')?.classList.add('is-revealed'));
 setup();
})();

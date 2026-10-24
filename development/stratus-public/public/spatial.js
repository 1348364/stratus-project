'use strict';
// Procedural CSS geometry and presentation only; no external services or AI calls.
(() => {
 const body=document.body, hero=document.querySelector('.immersive-hero');
 if(!hero)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const stage=document.createElement('div');stage.className='voxel-stage';stage.dataset.effect='1';stage.setAttribute('aria-hidden','true');
 const blocks=[[0,0,0],[1,0,0],[2,0,0],[0,0,1],[1,0,1],[2,0,1],[0,0,2],[1,0,2],[2,0,2],[0,1,0],[2,1,0],[0,1,2],[1,1,2],[2,1,2],[0,2,0],[2,2,2],[1,3,1]];
 stage.innerHTML=`<div class="voxel-aura"></div><div class="voxel-orbit orbit-a"></div><div class="voxel-orbit orbit-b"></div><div class="voxel-world">${blocks.map(([x,y,z],i)=>`<div class="voxel ${y>0?'voxel-glass':''}" style="--x:${x};--y:${y};--z:${z};--order:${i}"><i class="voxel-top"></i><i class="voxel-front"></i><i class="voxel-side"></i></div>`).join('')}</div><span class="voxel-caption">S T R A T U S / FIELD STUDY 001<br><b>LIGHT · WATER · ATMOSPHERE</b></span>`;
 hero.append(stage);
 const journey=document.createElement('section');journey.className='spatial-journey';journey.dataset.effect='2';journey.setAttribute('aria-labelledby','spatial-title');
 journey.innerHTML=`<div class="spatial-sticky"><div class="spatial-heading"><p class="eyebrow">A WORLD, LAYER BY LAYER</p><h2 id="spatial-title">Nothing exists<br>in <em>isolation.</em></h2><p>Scroll through the elements that give Stratus its atmosphere.</p></div><div class="layer-stage" aria-hidden="true"><div class="layer-world"><div class="world-layer layer-sky"><span>03 / ATMOSPHERE</span></div><div class="world-layer layer-light"><span>02 / LIGHT</span><i></i></div><div class="world-layer layer-water"><span>01 / WATER</span></div><div class="layer-axis"></div></div></div><span class="spatial-counter" aria-hidden="true">01 — 03 <i></i> SCROLL TO UNFOLD</span></div><div class="spatial-steps"><article><span>01 / WATER</span><h3>Depth you can feel.</h3><p>Reflections meet refraction. The world above connects with the riverbed below.</p></article><article><span>02 / LIGHT</span><h3>A familiar sun.<br>A different mood.</h3><p>Square light, warm horizons and the character of the original world.</p></article><article><span>03 / ATMOSPHERE</span><h3>The space<br>between everything.</h3><p>Clouds, high wisps and mist bring distance and weather into the picture.</p></article></div>`;
 journey.querySelector('.spatial-sticky').append(journey.querySelector('.spatial-steps'));
 const wordmark=document.querySelector('.atmosphere-wordmark');
 if(wordmark){wordmark.dataset.effect='5';wordmark.removeAttribute('aria-hidden');wordmark.setAttribute('role','img');wordmark.setAttribute('aria-label','STRATUS');wordmark.innerHTML=`<span class="wordmark-depth" aria-hidden="true">${Array.from({length:8},(_,i)=>`<i style="--layer:${8-i};--layer-color:${['#153d2a','#1b4832','#23563c','#2f6749','#427a59','#5a906c','#74a783','#93bea0'][i]}">STRATUS</i>`).join('')}<b>STRATUS</b></span><span class="wordmark-arrow" aria-hidden="true">↘</span>`;wordmark.after(journey);}
 // Effect 4: every release image lives in an accessible depth carousel.
 const gallery=document.querySelector('#home-gallery');
 let selected=0;
 const controls=document.createElement('div');controls.className='carousel-controls';
 controls.innerHTML='<button type="button" class="carousel-prev" aria-label="Previous showcase">←</button><p class="carousel-status" aria-live="polite" aria-atomic="true"></p><button type="button" class="carousel-next" aria-label="Next showcase">→</button>';
 gallery?.after(controls);
 function carousel(){document.querySelectorAll('.workspace-card,.showcase-image').forEach(el=>el.dataset.effect='3');if(!gallery)return;gallery.classList.add('spatial-carousel');gallery.dataset.effect='4';gallery.setAttribute('role','region');gallery.setAttribute('aria-label','Release showcase carousel');
  const cards=[...gallery.querySelectorAll('.scene')];if(!cards.length)return;selected=(selected+cards.length)%cards.length;
  cards.forEach((card,i)=>{let offset=i-selected;if(offset>cards.length/2)offset-=cards.length;if(offset< -cards.length/2)offset+=cards.length;card.style.setProperty('--position',offset);card.style.setProperty('--distance',Math.abs(offset));card.style.zIndex=String(10-Math.abs(offset));card.classList.toggle('carousel-current',i===selected);card.classList.toggle('carousel-hidden',Math.abs(offset)>1);card.tabIndex=i===selected?0:-1;card.setAttribute('aria-hidden',String(Math.abs(offset)>1));});
  const title=cards[selected].querySelector('b')?.textContent||'Showcase';controls.querySelector('.carousel-status').textContent=`${String(selected+1).padStart(2,'0')} / ${String(cards.length).padStart(2,'0')} — ${title}`;
  cards.forEach((card,i)=>card.setAttribute('aria-label',`${i===selected?'Open':'Select'} ${card.querySelector('b')?.textContent||'showcase'}`));
  controls.querySelectorAll('button').forEach(b=>b.disabled=cards.length<2);
 }
 function advance(delta){selected+=delta;carousel();}
 controls.querySelector('.carousel-prev').addEventListener('click',()=>advance(-1));controls.querySelector('.carousel-next').addEventListener('click',()=>advance(1));
 gallery?.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();advance(e.key==='ArrowRight'?1:-1);gallery.querySelector('.carousel-current')?.focus({preventScroll:true});}});
 gallery?.addEventListener('click',e=>{const card=e.target.closest('.scene');if(card&&!card.classList.contains('carousel-current')){e.preventDefault();e.stopPropagation();selected=[...gallery.children].indexOf(card);carousel();}},true);
 document.addEventListener('stratus:scenes-updated',carousel);if(gallery)new MutationObserver(carousel).observe(gallery,{childList:true});carousel();
 const motion=window.StratusMotion;let px=0,py=0,active=false,pointer=null;
 const enabled=()=>!reduced.matches&&!body.classList.contains('effects-paused');
 const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
 function read(state){if(state.hidden||hero.closest('[data-view][hidden]'))return null;const r=journey.getBoundingClientRect(),box=wordmark?.getBoundingClientRect();let tilt=null;
  if(pointer&&pointer.card.isConnected&&enabled()){const b=pointer.card.getBoundingClientRect();tilt={card:pointer.card,x:(pointer.x-b.left)/b.width,y:(pointer.y-b.top)/b.height};}pointer=null;
  return {progress:clamp(-r.top/Math.max(1,r.height-state.h)),travel:box?clamp((state.h-box.top)/(state.h+box.height)):.5,tilt};
 }
 function paint(data){if(!data)return;const {progress,travel,tilt}=data;active=enabled();body.classList.toggle('spatial-paused',!active);
  motion.style(journey,'--unfold',active?progress:0.5);
  motion.style(journey,'--journey-turn',`${active?(progress-.5)*24:0}deg`);
  motion.style(stage,'--orbit-x',`${active?px*13:0}deg`);motion.style(stage,'--orbit-y',`${active?py*-9:0}deg`);
  if(wordmark)motion.style(wordmark,'--word-turn',`${active?(travel-.5)*20:0}deg`);
  if(tilt){motion.style(tilt.card,'--tilt-x',`${(tilt.x-.5)*7}deg`);motion.style(tilt.card,'--tilt-y',`${(tilt.y-.5)*-7}deg`);motion.style(tilt.card,'--shine-x',`${tilt.x*100}%`);}
  const part=Math.min(2,Math.floor(progress*3));journey.querySelectorAll('.spatial-steps article').forEach((el,i)=>el.classList.toggle('step-active',part===i));
 }
 const schedule=motion.request;motion.register('spatial',read,paint);
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>stage.classList.toggle('sculpture-dormant',!entries[0].isIntersecting)).observe(hero);
 hero.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse')return;px=e.clientX/innerWidth-.5;py=e.clientY/innerHeight-.5;schedule();},{passive:true});
 hero.addEventListener('pointerleave',()=>{px=py=0;schedule();});
 const heroImage=hero.querySelector('.hero-image');
 function syncImage(){const image=heroImage?.getAttribute('src');if(image){journey.style.setProperty('--world-image',`url(${JSON.stringify(image)})`);stage.style.setProperty('--world-image',`url(${JSON.stringify(image)})`);}}
 if(heroImage)new MutationObserver(syncImage).observe(heroImage,{attributes:true,attributeFilter:['src']});syncImage();
 // Event delegation also handles galleries replaced by the automatic release feed.
 document.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||!enabled())return;const card=e.target.closest('.showcase-image,.workspace-card');if(!card)return;pointer={card,x:e.clientX,y:e.clientY};schedule();},{passive:true});
 document.addEventListener('pointerout',e=>{const card=e.target.closest('.scene,.showcase-image,.workspace-card');if(card&&!card.contains(e.relatedTarget)){card.style.removeProperty('--tilt-x');card.style.removeProperty('--tilt-y');}},{passive:true});
 const intro=document.querySelector('.hero h1');
 if(intro)intro.classList.add('spatial-title');
 function route(){schedule();if(!enabled())return;const view=[...document.querySelectorAll('[data-view]')].find(el=>!el.hidden);if(view&&view.dataset.view!=='overview')view.animate([{opacity:0},{opacity:1}],{duration:400,easing:'ease-out'});}
 new MutationObserver(schedule).observe(body,{attributes:true,attributeFilter:['class']});
 window.addEventListener('hashchange',route);document.addEventListener('visibilitychange',()=>{body.classList.toggle('spatial-background',document.hidden);schedule();});reduced.addEventListener('change',schedule);schedule();
})();

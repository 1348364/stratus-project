'use strict';
// Procedural CSS geometry and presentation only; no external services or AI calls.
(() => {
 const body=document.body, hero=document.querySelector('.immersive-hero');
 if(!hero)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const stage=document.createElement('div');stage.className='voxel-stage';stage.setAttribute('aria-hidden','true');
 const blocks=[[0,0,0],[1,0,0],[2,0,0],[0,0,1],[1,0,1],[2,0,1],[0,0,2],[1,0,2],[2,0,2],[0,1,0],[2,1,0],[0,1,2],[1,1,2],[2,1,2],[0,2,0],[2,2,2],[1,3,1]];
 stage.innerHTML=`<div class="voxel-aura"></div><div class="voxel-orbit orbit-a"></div><div class="voxel-orbit orbit-b"></div><div class="voxel-world">${blocks.map(([x,y,z],i)=>`<div class="voxel ${y>0?'voxel-glass':''}" style="--x:${x};--y:${y};--z:${z};--order:${i}"><i class="voxel-top"></i><i class="voxel-front"></i><i class="voxel-side"></i></div>`).join('')}</div><span class="voxel-caption">S T R A T U S / FIELD STUDY 001<br><b>LIGHT · WATER · ATMOSPHERE</b></span>`;
 hero.append(stage);
 const journey=document.createElement('section');journey.className='spatial-journey';journey.setAttribute('aria-labelledby','spatial-title');
 journey.innerHTML=`<div class="spatial-sticky"><div class="spatial-heading"><p class="eyebrow">A WORLD, LAYER BY LAYER</p><h2 id="spatial-title">Nothing exists<br>in <em>isolation.</em></h2><p>Scroll through the elements that give Stratus its atmosphere.</p></div><div class="layer-stage" aria-hidden="true"><div class="layer-world"><div class="world-layer layer-sky"><span>03 / ATMOSPHERE</span></div><div class="world-layer layer-light"><span>02 / LIGHT</span><i></i></div><div class="world-layer layer-water"><span>01 / WATER</span></div><div class="layer-axis"></div></div></div><span class="spatial-counter" aria-hidden="true">01 — 03 <i></i> SCROLL TO UNFOLD</span></div><div class="spatial-steps"><article><span>01 / WATER</span><h3>Depth you can feel.</h3><p>Reflections meet refraction. The world above connects with the riverbed below.</p></article><article><span>02 / LIGHT</span><h3>A familiar sun.<br>A different mood.</h3><p>Square light, warm horizons and the character of the original world.</p></article><article><span>03 / ATMOSPHERE</span><h3>The space<br>between everything.</h3><p>Clouds, high wisps and mist bring distance and weather into the picture.</p></article></div>`;
 journey.querySelector('.spatial-sticky').append(journey.querySelector('.spatial-steps'));
 document.querySelector('.atmosphere-wordmark')?.after(journey);
 let frame=0,px=0,py=0,active=false;
 const enabled=()=>!reduced.matches&&!body.classList.contains('effects-paused');
 const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
 function paint(){frame=0;if(document.hidden)return;active=enabled();body.classList.toggle('spatial-paused',!active);
  const r=journey.getBoundingClientRect(),progress=clamp(-r.top/Math.max(1,r.height-innerHeight));
  journey.style.setProperty('--unfold',active?progress:0.5);
  journey.style.setProperty('--journey-turn',`${active?(progress-.5)*24:0}deg`);
  stage.style.setProperty('--orbit-x',`${active?px*13:0}deg`);stage.style.setProperty('--orbit-y',`${active?py*-9:0}deg`);
  const part=Math.min(2,Math.floor(progress*3));journey.querySelectorAll('.spatial-steps article').forEach((el,i)=>el.classList.toggle('step-active',part===i));
 }
 const schedule=()=>{if(!frame)frame=requestAnimationFrame(paint);};
 hero.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse')return;const r=hero.getBoundingClientRect();px=(e.clientX-r.left)/r.width-.5;py=(e.clientY-r.top)/r.height-.5;schedule();},{passive:true});
 hero.addEventListener('pointerleave',()=>{px=py=0;schedule();});
 const heroImage=hero.querySelector('.hero-image');
 function syncImage(){const image=heroImage?.getAttribute('src');if(image){journey.style.setProperty('--world-image',`url(${JSON.stringify(image)})`);stage.style.setProperty('--world-image',`url(${JSON.stringify(image)})`);}}
 if(heroImage)new MutationObserver(syncImage).observe(heroImage,{attributes:true,attributeFilter:['src']});syncImage();
 // Event delegation also handles galleries replaced by the automatic release feed.
 document.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||!enabled())return;const card=e.target.closest('.scene,.showcase-image,.workspace-card');if(!card)return;const r=card.getBoundingClientRect();card.style.setProperty('--tilt-x',`${((e.clientX-r.left)/r.width-.5)*7}deg`);card.style.setProperty('--tilt-y',`${((e.clientY-r.top)/r.height-.5)*-7}deg`);},{passive:true});
 document.addEventListener('pointerout',e=>{const card=e.target.closest('.scene,.showcase-image,.workspace-card');if(card&&!card.contains(e.relatedTarget)){card.style.removeProperty('--tilt-x');card.style.removeProperty('--tilt-y');}},{passive:true});
 const intro=document.querySelector('.hero h1');
 if(intro){intro.classList.add('spatial-title');if(!reduced.matches)intro.animate([{opacity:0,transform:'translateY(32px) rotateX(14deg)',filter:'blur(12px)'},{opacity:1,transform:'none',filter:'blur(0)'}],{duration:1450,easing:'cubic-bezier(.18,.7,.2,1)'});}
 function route(){schedule();if(!enabled())return;const view=[...document.querySelectorAll('[data-view]')].find(el=>!el.hidden);if(view&&view.dataset.view!=='overview')view.animate([{opacity:0,transform:'translateY(18px)'},{opacity:1,transform:'none'}],{duration:650,easing:'cubic-bezier(.2,.7,.2,1)'});}
 new MutationObserver(schedule).observe(body,{attributes:true,attributeFilter:['class']});
 window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});window.addEventListener('hashchange',route);document.addEventListener('visibilitychange',schedule);reduced.addEventListener('change',schedule);schedule();
})();

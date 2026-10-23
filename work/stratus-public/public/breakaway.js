'use strict';
// Reversible scroll state, not a timed departure animation. Native scrolling stays intact.
(() => {
 const body=document.body,preference=matchMedia('(prefers-reduced-motion: reduce)'),hero=document.querySelector('.immersive-hero');
 const groups=new Set();let frame=0;
 const clamp=n=>Math.max(0,Math.min(1,n));
 const disabled=()=>preference.matches||body.classList.contains('effects-paused');
 function mark(group){if(groups.has(group)||group.parentElement.closest('[data-break-group]'))return;group.dataset.breakGroup='';groups.add(group);
  let pieces=[...group.children].filter(el=>!el.matches('script,style'));
  if(group.matches('.public-faq'))pieces=[...group.querySelectorAll(':scope>.home-heading,:scope .faq-list>details')];
  if(group===hero)pieces=[...hero.querySelectorAll('.hero-content>*,.voxel-stage,.hero-manifesto')];
  pieces.forEach((piece,i)=>{piece.dataset.breakPiece='';piece.style.setProperty('--scatter-x',`${(i%2?-1:1)*(65+i%3*32)}px`);piece.style.setProperty('--scatter-y',`${-18-i%4*17}px`);piece.style.setProperty('--scatter-r',`${(i%2?1:-1)*(3+i%3*2)}deg`);});
 }
 function register(){document.querySelectorAll('.immersive-hero,.home-view>.home-heading,.workspace-cards,.reference-strip,.gallery-section,.water-story,.public-faq,.workflow-note,.section-intro,.showcase-shot,.release,.spec-section,.platform-strip,.preset-guide,.spec-footnote,.upcoming-item,.roadmap-process,.roadmap-note').forEach(mark);schedule();}
 const image=hero?.querySelector('.hero-image'),tiles=document.createElement('div');tiles.className='hero-fragments';tiles.setAttribute('aria-hidden','true');
 if(image){for(let i=0;i<12;i++){const tile=document.createElement('i'),x=i%4,y=Math.floor(i/4);tile.style.cssText=`--tile-x:${x};--tile-y:${y};--tile-dx:${(x-1.5)*105}px;--tile-dy:${(y-1)*95}px;--tile-r:${(i%2?1:-1)*(4+i%4*3)}deg`;tiles.append(tile);}hero.append(tiles);
  const sync=()=>{tiles.style.setProperty('--fragment-image',`url(${JSON.stringify(image.getAttribute('src'))})`);};new MutationObserver(sync).observe(image,{attributes:true,attributeFilter:['src']});sync();
 }
 function update(){frame=0;const off=disabled();for(const group of groups){if(!group.isConnected){groups.delete(group);continue;}if(group.closest('[data-view][hidden]'))continue;const r=group.getBoundingClientRect();if(r.top>innerHeight+200||r.bottom< -innerHeight)continue;
   const focused=group.contains(document.activeElement)&&document.activeElement.matches(':focus-visible');
   let amount=off||focused?0:group===hero?clamp((-r.top-r.height*.08)/(r.height*.75)):clamp((84-r.top)/Math.max(260,Math.min(r.height,innerHeight)));
   group.style.setProperty('--break',amount.toFixed(4));group.classList.toggle('is-breaking',amount>.001);
  }}
 function schedule(){if(!frame)frame=requestAnimationFrame(update);}
 window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});window.addEventListener('hashchange',schedule);document.addEventListener('focusin',schedule);document.addEventListener('focusout',schedule);preference.addEventListener('change',()=>{groups.forEach(g=>g.style.setProperty('--break','0'));schedule();});
 new MutationObserver(()=>{if(disabled())groups.forEach(g=>g.style.setProperty('--break','0'));schedule();}).observe(body,{attributes:true,attributeFilter:['class']});
 new MutationObserver(records=>{if(records.some(r=>r.addedNodes.length))register();}).observe(document.querySelector('main'),{childList:true,subtree:true});register();
})();

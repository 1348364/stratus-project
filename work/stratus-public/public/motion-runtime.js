'use strict';
// One event-driven frame, with all geometry reads before presentation writes.
(() => {
 const tasks=new Map(),profiling=new URLSearchParams(location.search).has('profile'),samples=[];let pending=0,ticks=0;
 function request(){if(!pending)pending=requestAnimationFrame(tick);}
 function tick(){pending=0;const started=profiling?performance.now():0,h=innerHeight,w=innerWidth;
  const state={y:scrollY,h,w,hidden:document.hidden,paused:document.body.classList.contains('effects-paused'),height:document.documentElement.scrollHeight};
  const values=[];for(const task of tasks.values())values.push([task,task.read?.(state)]);
  for(const [task,value] of values)task.write?.(value,state);
  if(profiling){samples.push(performance.now()-started);if(samples.length>120)samples.shift();ticks++;if(ticks%20===0){const sorted=[...samples].sort((a,b)=>a-b);Object.assign(document.documentElement.dataset,{motionTicks:String(ticks),frameP95:sorted[Math.floor((sorted.length-1)*.95)].toFixed(2),frameMean:(samples.reduce((a,b)=>a+b,0)/samples.length).toFixed(2)});}}
 }
 function style(el,key,value){if(el&&el.style.getPropertyValue(key)!==String(value))el.style.setProperty(key,String(value));}
 window.StratusMotion={register(name,read,write){tasks.set(name,{read,write});request();},request,style};
 for(const name of ['scroll','resize','hashchange'])window.addEventListener(name,request,{passive:true});
 document.addEventListener('visibilitychange',request);
})();

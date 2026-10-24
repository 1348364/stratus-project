'use strict';
// One event-driven frame, with all geometry reads before presentation writes.
(() => {
 const tasks=new Map();let pending=0;
 function request(){if(!pending)pending=requestAnimationFrame(tick);}
 function tick(){pending=0;const h=innerHeight,w=innerWidth;
  const state={y:scrollY,h,w,hidden:document.hidden,paused:document.body.classList.contains('effects-paused'),height:document.documentElement.scrollHeight};
  const values=[];for(const task of tasks.values())values.push([task,task.read?.(state)]);
  for(const [task,value] of values)task.write?.(value,state);
 }
 function style(el,key,value){if(el&&el.style.getPropertyValue(key)!==String(value))el.style.setProperty(key,String(value));}
 window.StratusMotion={register(name,read,write){tasks.set(name,{read,write});request();},request,style};
 for(const name of ['scroll','resize','hashchange'])window.addEventListener(name,request,{passive:true});
 document.addEventListener('visibilitychange',request);
})();

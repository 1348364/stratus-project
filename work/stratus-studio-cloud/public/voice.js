'use strict';
// Browser dictation only: audio is not uploaded to Studio or stored by this app.
(() => {
 const tools=document.querySelector('.toolbar-tools');if(!tools)return;
 const toggle=document.createElement('button');toggle.id='voice-toggle';toggle.type='button';toggle.textContent='Dictate';toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-controls','voice-panel');tools.prepend(toggle);
 const panel=document.createElement('section');panel.id='voice-panel';panel.className='voice-panel';panel.hidden=true;panel.setAttribute('aria-label','Voice to text');
 panel.innerHTML='<div class="voice-heading"><strong id="voice-title">Voice to text</strong><button type="button" id="voice-close" aria-label="Close dictation">×</button></div><p id="voice-help">English (Australia). Your browser may send audio to its speech service. Review the transcript before inserting; Studio does not store audio.</p><div class="voice-actions"><button type="button" id="voice-start">Start dictation</button><button type="button" id="voice-stop" disabled>Stop</button><span id="voice-status" role="status" aria-live="polite">Ready.</span></div><label class="sr-only" for="voice-text">Dictation transcript</label><textarea id="voice-text" rows="3" placeholder="Your words appear here. You can edit them after stopping." aria-describedby="voice-help"></textarea><p id="voice-interim" aria-label="Speech being recognised"></p><div class="voice-actions"><button type="button" id="voice-insert" disabled>Insert at cursor</button><button type="button" id="voice-clear">Clear transcript</button><small>Review first. Undo works after insertion.</small></div>';
 document.querySelector('#search-panel').before(panel);
 const el=id=>document.getElementById('voice-'+id),text=el('text'),start=el('start'),stop=el('stop'),insert=el('insert'),status=el('status');
 const Speech=window.SpeechRecognition||window.webkitSpeechRecognition;
 let recognition=null,active=false,started=false,error=false,watchdog=null,stopTimer=null,sessionTimer=null;
 const saved=storageGet('stratus-studio-dictation');if(typeof saved?.text==='string')text.value=saved.text;
 function remember(){if(text.value)storageSet('stratus-studio-dictation',{text:text.value});else storageRemove('stratus-studio-dictation');insert.disabled=active||!text.value.trim();}
 function message(value){status.textContent=value;}
 function finish(){clearTimeout(watchdog);clearTimeout(stopTimer);clearTimeout(sessionTimer);active=started=false;recognition=null;start.disabled=!Speech;stop.disabled=true;text.readOnly=false;el('clear').disabled=false;toggle.classList.remove('listening');el('interim').textContent='';remember();}
 function cancel(note){if(recognition){recognition.onresult=recognition.onend=recognition.onerror=null;try{recognition.abort();}catch{}}finish();if(note)message(note);}
 function end(){if(!recognition)return;start.disabled=true;stop.disabled=true;message('Finishing recognition…');try{recognition.stop();stopTimer=setTimeout(()=>cancel('Stopped. Review your transcript before inserting.'),3000);}catch{cancel('Stopped. Review your transcript before inserting.');}}
 toggle.onclick=()=>{if(panel.hidden){if(!state.current||!state.docs[state.current])return;panel.hidden=false;toggle.setAttribute('aria-expanded','true');el('title').textContent='Voice to text · '+state.docs[state.current].filename;if(!Speech)message('Dictation is unavailable in this browser. Open Studio in a browser with speech recognition, or use your keyboard’s dictation.');else message('Ready. Start dictation when you want the microphone on.');start.disabled=!Speech;remember();}else close();};
 function close(){cancel('Stopped. Transcript retained.');panel.hidden=true;toggle.setAttribute('aria-expanded','false');}
 el('close').onclick=()=>{close();toggle.focus();};
 start.onclick=()=>{
  if(active||!Speech||!state.docs[state.current])return;
  let rec;try{rec=new Speech();}catch{message('Speech recognition could not be initialised in this browser.');return;}const seen=new Set();recognition=rec;active=true;error=false;started=false;
  rec.lang='en-AU';rec.continuous=true;rec.interimResults=true;rec.maxAlternatives=1;
  start.disabled=true;stop.disabled=false;insert.disabled=true;text.readOnly=true;el('clear').disabled=true;toggle.classList.add('listening');message('Waiting for microphone permission…');
  rec.onstart=()=>{if(recognition!==rec)return;started=true;clearTimeout(watchdog);message('Listening… Speak naturally, then press Stop.');sessionTimer=setTimeout(end,180000);};
  rec.onresult=event=>{if(recognition!==rec)return;const interim=[];for(let i=event.resultIndex;i<event.results.length;i++){const result=event.results[i],words=result[0].transcript.trim();if(result.isFinal){if(!seen.has(i)){seen.add(i);if(words)text.value+=(text.value&&!/\s$/.test(text.value)?' ':'')+words;}}else interim.push(words);}el('interim').textContent=interim.join(' ');remember();};
  rec.onerror=event=>{if(recognition!==rec)return;error=true;const messages={'not-allowed':'Microphone access was denied. Allow it in your browser’s site settings, then try again.','service-not-allowed':'Speech recognition is blocked by this browser. Try another supported browser.','audio-capture':'No microphone is available. Connect one and try again.','no-speech':'No speech was detected. Press Start dictation to try again.','network':'The speech service could not connect. Check your connection and try again.','language-not-supported':'Australian English is unavailable in this browser’s speech service.','aborted':'Dictation stopped.'};message(messages[event.error]||'Recognition stopped. Your transcript is retained.');finish();};
  rec.onend=()=>{if(recognition!==rec)return;finish();if(!error)message('Stopped. Review your transcript, then insert it.');};
  watchdog=setTimeout(()=>{if(!started)cancel('Microphone did not start. Check browser permissions and try again.');},20000);
  try{rec.start();}catch{cancel('Dictation could not start in this browser. Your transcript is retained.');}
 };
 stop.onclick=end;text.addEventListener('input',remember);
 el('clear').onclick=()=>{if(!active){text.value='';remember();message('Transcript cleared.');}};
 insert.onclick=()=>{if(active||!text.value.trim()||!state.docs[state.current])return;const area=editorArea(),a=area.selectionStart,b=area.selectionEnd,words=text.value.trim();const prefix=a>0&&/\S/.test(area.value[a-1])&&!/^[.,!?;:)]/.test(words)?' ':'';const suffix=b<area.value.length&&/\S/.test(area.value[b])?' ':'';const value=prefix+words+suffix;
  edit(area.value.slice(0,a)+value+area.value.slice(b),{discrete:true});area.setSelectionRange(a+value.length,a+value.length);area.focus();text.value='';remember();message('Inserted. Use Save to keep the document in Studio.');
 };
 window.addEventListener('hashchange',close);window.addEventListener('pagehide',()=>cancel());
 document.addEventListener('visibilitychange',()=>{if(document.hidden&&active)cancel('Stopped because the page was hidden. Transcript retained.');});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden){close();toggle.focus();}});
 start.disabled=!Speech;remember();
})();

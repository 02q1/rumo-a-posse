/* ---------- Roteamento ---------- */
const MOBILE_TABS=['painel','questoes','revisao','jornada'];
function renderNavDue(){ const n=dueQs().length; document.querySelectorAll('[data-due]').forEach(el=>el.textContent=n?n:''); const ne=EDITAIS.filter(e=>today()>=e.ini&&today()<=e.fim).length; const ee=$('#navEd'); if(ee) ee.textContent=ne?ne:''; }
function render(){
  let r=(location.hash||'#painel').slice(1); if(!V[r]) r='painel';
  document.querySelectorAll('nav.side a[href^="#"]').forEach(a=>{ const h=a.getAttribute('href').slice(1); const on=h===r||(h==='mais'&&!MOBILE_TABS.includes(r)); a.classList.toggle('on',h==='mais'?on:h===r); if(h===r) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
  if(r!=='flashcards') FC=null;
  $('#view').innerHTML=V[r]();
  V[r].after&&V[r].after();
  renderNavDue(); setSync();
}
let lastRoute=location.hash;
window.addEventListener('hashchange',()=>{ if(location.hash!==lastRoute){ lastRoute=location.hash; render(); window.scrollTo({top:0}); } });
render();
if(!IS_ART&&'serviceWorker' in navigator&&location.protocol==='https:') navigator.serviceWorker.register('sw.js').catch(()=>{});

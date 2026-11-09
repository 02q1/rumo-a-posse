/* ======================================================================
   Recursos novos (v14): IA no site, favoritos e anotações, revisão por
   dificuldade, simulado personalizado, flashcards de erros, edital
   verticalizado, jornada, discursivas, agenda, perfil e menu "Mais".
   ====================================================================== */

/* ---------- IA: tutor e correção ---------- */
const AIKEY='rumo.apikey', AIMODEL='rumo.aimodel';
const lsGet=k=>{try{return localStorage.getItem(k)||''}catch(e){return ''}};
const lsSet=(k,v)=>{try{ if(v) localStorage.setItem(k,v); else localStorage.removeItem(k); }catch(e){}};
function aiReady(){ return IS_ART || !!lsGet(AIKEY); }
function aiSetupHTML(){ return `<div class="note">O tutor IA precisa de uma chave da API da Anthropic neste site: cole a sua em <a href="#perfil">Perfil</a> (ela fica só neste navegador). Na <a href="https://claude.ai/artifact/KMMxfikPC7cV323XHVfhQE" target="_blank" rel="noopener">versão do claude.ai</a> o tutor funciona sem chave.</div>`; }
let sampleP=null;
async function aiCall(prompt,{onText}={}){
  if(IS_ART){
    sampleP=sampleP||claude.use('sample'); const sample=await sampleP; if(!sample) throw {code:'nosample'};
    const r=await sample(prompt,{modelTier:'quick',onText:onText?({text})=>onText(text):undefined}); return r.text;
  }
  const key=lsGet(AIKEY); if(!key) throw {code:'nokey'};
  const model=lsGet(AIMODEL)||'claude-opus-5-5';
  let res, j;
  try{
    res=await fetch('https://api.anthropic.com/v1/messages',{method:'POST',headers:{'content-type':'application/json','x-api-key':key,'anthropic-version':'2026-10-21','anthropic-dangerous-direct-browser-access':'true'},
      body:JSON.stringify({model,max_tokens:16000,output_config:{effort:'low'},messages:[{role:'user',content:prompt}]})});
    j=await res.json().catch(()=>({}));
  }catch(e){ throw {code:'net'} }
  if(!res.ok) throw {code:res.status===401?'badkey':res.status===429?'rate_limited':'http',msg:j&&j.error&&j.error.message};
  if(j.stop_reason==='refusal') throw {code:'refusal'};
  return (j.content||[]).filter(b=>b.type==='text').map(b=>b.text).join('\n').trim();
}
function aiErr(e){
  const c=e&&e.code;
  return c==='rate_limited'?'Muitas perguntas seguidas. Tente de novo em alguns minutos.':c==='badkey'?'A chave da API foi recusada. Confira em Perfil.':c==='nokey'?'Cole sua chave da API em Perfil para usar o tutor neste site.':c==='refusal'?'O modelo não respondeu a este pedido. Tente reformular.':c==='net'?'Sem conexão com a API agora.':'Não consegui falar com o tutor agora'+(e&&e.msg?': '+e.msg:'.');
}

/* ---------- Busca, favoritos, anotações ---------- */
const norm=t=>String(t||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const HAY={};
function searchHit(q,t){ const hay=HAY[q.id]||(HAY[q.id]=norm([q.stem,q.cmd,(q.opts||[]).join(' '),q.tema,q.ass,q.disc,q.text?TXT[q.text]:''].join(' '))); return norm(t).split(/\s+/).filter(Boolean).every(w=>hay.includes(w)); }
function toolsHTML(q){
  const f=S.fav[q.id], n=S.notes[q.id];
  return `<div class="row qtools" style="gap:6px"><button class="btn sm" data-fav aria-pressed="${f?'true':'false'}">${f?'★ Favorita':'☆ Favoritar'}</button><button class="btn sm" data-note>${n?'Editar anotação':'Anotar'}</button></div><div class="ntslot">${n?`<div class="notebox">${esc(n)}</div>`:''}</div>`;
}
function wireTools(el,q){
  const fb=el.querySelector('[data-fav]'), nb=el.querySelector('[data-note]'), slot=el.querySelector('.ntslot');
  if(fb) fb.onclick=()=>{ if(S.fav[q.id]) delete S.fav[q.id]; else S.fav[q.id]=today(); persist(); const f=!!S.fav[q.id]; fb.textContent=f?'★ Favorita':'☆ Favoritar'; fb.setAttribute('aria-pressed',f); toast(f?'Questão salva nas favoritas':'Removida das favoritas'); };
  if(nb) nb.onclick=()=>{
    slot.innerHTML=`<textarea class="ta" rows="3" aria-label="Anotação da questão" placeholder="Sua anotação: a regra, a pegadinha, o artigo da lei…">${esc(S.notes[q.id]||'')}</textarea><div class="row" style="gap:6px;margin-top:6px"><button class="btn sm pri" data-nsave>Salvar anotação</button>${S.notes[q.id]?'<button class="btn sm" data-ndel>Apagar</button>':''}</div>`;
    const ta=slot.querySelector('textarea'); ta.focus();
    slot.querySelector('[data-nsave]').onclick=()=>{ const v=ta.value.trim(); if(v) S.notes[q.id]=v; else delete S.notes[q.id]; persist(); slot.innerHTML=v?`<div class="notebox">${esc(v)}</div>`:''; nb.textContent=v?'Editar anotação':'Anotar'; toast('Anotação salva'); };
    const d=slot.querySelector('[data-ndel]'); if(d) d.onclick=()=>{ delete S.notes[q.id]; persist(); slot.innerHTML=''; nb.textContent='Anotar'; };
  };
}

/* ---------- Revisão: difícil, bom, fácil ---------- */
function rateHTML(){ return `<div class="row rate" style="gap:6px"><span class="note">Como foi lembrar?</span><button class="btn sm" data-rate="h">Difícil: rever amanhã</button><button class="btn sm" data-rate="g">Bom</button><button class="btn sm" data-rate="e">Fácil: rever bem depois</button></div>`; }
function wireRate(fb,q){
  fb.querySelectorAll('[data-rate]').forEach(b=>b.onclick=()=>{
    const it=S.srs[q.id]; if(!it) return; const k=b.dataset.rate;
    if(k==='h'){ it.step=Math.max(0,it.step-1); it.due=addDays(today(),1); }
    else if(k==='e'){ it.step=Math.min(STEPS.length-1,it.step+1); it.due=addDays(today(),STEPS[it.step]*2); }
    persist(); const r=fb.querySelector('.rate'); if(r) r.innerHTML=`<span class="note">Próxima revisão em ${isoBR(it.due)}.</span>`;
  });
}

/* ---------- Simulado personalizado ---------- */
let CS={banca:'FCC',discs:[],n:20,pend:true};
const shuffle=a=>{ const b=a.slice(); for(let i=b.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [b[i],b[j]]=[b[j],b[i]]; } return b; };
const GERAIS=['Língua Portuguesa','Raciocínio Lógico e Matemática','Legislação do tribunal','Direitos Humanos e Inclusão','Tecnologia da Informação e Dados'];
const ESPEC=['Direito Constitucional','Direito Administrativo','AFO e Orçamento Público','Gestão de Pessoas'];
function customPool(){ return REAL.filter(q=>!q.anulada&&(!CS.banca||SRC[q.src].banca===CS.banca)&&(!CS.pend||!S.ans[q.id])); }
function customSimHTML(){
  const bancas=[...new Set(REAL.map(q=>SRC[q.src].banca))];
  const base=REAL.filter(q=>!q.anulada&&(!CS.banca||SRC[q.src].banca===CS.banca));
  const cnt={}; base.forEach(q=>cnt[q.disc]=(cnt[q.disc]||0)+1);
  const discs=Object.entries(cnt).sort((a,b)=>b[1]-a[1]);
  const pool=customPool().filter(q=>!CS.discs.length||CS.discs.includes(q.disc));
  return `<div class="panel" style="display:flex;flex-direction:column;gap:12px">
   <div class="row between"><h2>Simulado no formato TRT4 2026</h2><span class="chip hl">Seu alvo</span></div>
   <p class="note" style="margin:0">60 questões de múltipla escolha, como no edital: 30 de conhecimentos gerais (peso 1) e 30 específicas de Analista Administrativo (peso 2), 4 horas. Usa primeiro questões da FCC; se faltar, completa com outras bancas de A a E. A nota segue a regra do edital (mínimo 6 de 10).</p>
   <div class="row"><button class="btn pri" id="csTrt4">Começar simulado TRT4</button></div>
  </div>
  <div class="panel" style="display:flex;flex-direction:column;gap:12px">
   <h2>Monte o seu simulado</h2>
   <div class="grid g3">
    <label class="f">Banca<select id="csBanca"><option value="">Todas</option>${bancas.map(b=>`<option ${b===CS.banca?'selected':''}>${esc(b)}</option>`).join('')}</select></label>
    <label class="f">Número de questões<select id="csN">${[10,20,30,40,60].map(n=>`<option ${n===CS.n?'selected':''}>${n}</option>`).join('')}</select></label>
    <label class="f">Questões<select id="csPend"><option value="1" ${CS.pend?'selected':''}>Só as que nunca resolvi</option><option value="0" ${CS.pend?'':'selected'}>Todas</option></select></label>
   </div>
   <div><div class="note" style="margin-bottom:6px">Matérias (nenhuma marcada = todas)</div><div class="chips">${discs.map(([d,n])=>`<label class="chk"><input type="checkbox" data-csd="${esc(d)}" ${CS.discs.includes(d)?'checked':''}> ${esc(d)} <span class="note">${n}</span></label>`).join('')}</div></div>
   <div class="row between"><span class="note">${pool.length} questões disponíveis neste recorte · tempo: cerca de ${simMinutes(pool.slice(0,CS.n))} min</span><button class="btn pri" id="csGo" ${pool.length?'':'disabled'}>Começar (${Math.min(CS.n,pool.length)} questões)</button></div>
  </div>
  <h2 style="margin-top:8px">Provas completas</h2>`;
}
function simMinutes(qs){ return Math.max(5,Math.round(qs.reduce((t,q)=>t+(q.fmt==='CE'?2.2:3.4),0))); }
function startSim(ids,title,sub,extra){ const qs=ids.map(id=>QBY[id]); SIM=Object.assign({src:'custom',ids,resp:{},i:0,end:Date.now()+(extra&&extra.min||simMinutes(qs))*60000,done:false,title,sub,ce:qs.every(q=>q.fmt==='CE')},extra||{}); render(); window.scrollTo({top:0}); }
function wireCustomSim(){
  const b=$('#csBanca'); if(!b) return;
  b.onchange=e=>{CS.banca=e.target.value;CS.discs=[];render()};
  $('#csN').onchange=e=>{CS.n=+e.target.value;render()};
  $('#csPend').onchange=e=>{CS.pend=e.target.value==='1';render()};
  document.querySelectorAll('[data-csd]').forEach(c=>c.onchange=()=>{ const d=c.dataset.csd; CS.discs=c.checked?[...CS.discs,d]:CS.discs.filter(x=>x!==d); render(); });
  $('#csGo').onclick=()=>{ const pool=shuffle(customPool().filter(q=>!CS.discs.length||CS.discs.includes(q.disc))).slice(0,CS.n);
    startSim(pool.map(q=>q.id),'Simulado personalizado',`${pool.length} questões · ${CS.banca||'todas as bancas'}${CS.discs.length?' · '+CS.discs.join(', '):''}`); };
  $('#csTrt4').onclick=()=>{ const ids=trt4Ids(); startSim(ids,'Simulado no formato TRT4 2026','Analista Judiciário – Área Administrativa · FCC · 60 questões',{min:240,w:Object.fromEntries(ids.map((id,i)=>[id,i<30?1:2]))}); };
}
function trt4Ids(){
  const take=(disc,n,used)=>{ const mc=REAL.filter(q=>q.fmt==='MC'&&!q.anulada&&q.disc===disc&&!used.has(q.id));
    const order=[...shuffle(mc.filter(q=>SRC[q.src].banca==='FCC'&&!S.ans[q.id])),...shuffle(mc.filter(q=>SRC[q.src].banca==='FCC'&&S.ans[q.id])),...shuffle(mc.filter(q=>SRC[q.src].banca!=='FCC'))];
    const out=order.slice(0,n); out.forEach(q=>used.add(q.id)); return out; };
  const fill=(plan,total,used)=>{ let out=[]; plan.forEach(([d,n])=>out=out.concat(take(d,n,used))); let k=0; while(out.length<total&&k<20){ for(const [d] of plan){ if(out.length>=total) break; out=out.concat(take(d,1,used)); } k++; } return out.slice(0,total); };
  const used=new Set();
  const g=fill([['Língua Portuguesa',10],['Raciocínio Lógico e Matemática',7],['Legislação do tribunal',5],['Direitos Humanos e Inclusão',4],['Tecnologia da Informação e Dados',4]],30,used);
  const e=fill([['Direito Administrativo',11],['Direito Constitucional',8],['AFO e Orçamento Público',6],['Gestão de Pessoas',5]],30,used);
  return [...g,...e].map(q=>q.id);
}
function trt4NotaHTML(){
  if(!SIM||!SIM.w) return '';
  let pg=0,pe=0,ng=0,ne=0; SIM.ids.forEach(id=>{ const q=QBY[id], ok=SIM.resp[id]===q.ans; if(SIM.w[id]===1){ng++; if(ok)pg++} else {ne++; if(ok)pe++} });
  const nota=(pg+2*pe)/(ng+2*ne)*10;
  return `<div class="panel"><h3>Nota no critério do edital TRT4</h3><p style="margin:6px 0 0">Gerais: <b>${pg}/${ng}</b> (peso 1) · Específicas: <b>${pe}/${ne}</b> (peso 2) · Nota: <b style="font-family:var(--f-mono);font-size:20px;color:${nota>=6?'var(--ok)':'var(--bad)'}">${nota.toFixed(2).replace('.',',')}</b> de 10. ${nota>=6?'Acima do mínimo de 6: você estaria habilitado na objetiva.':'Abaixo do mínimo de 6 exigido pelo edital.'}</p><p class="note">Para ser chamado, além do mínimo, é preciso ficar bem colocado: no último TRT4 as notas de corte da Área Administrativa ficaram acima do mínimo. Use este número para medir a evolução.</p></div>`;
}

/* ---------- Flashcards: fixos + cartões dos seus erros ---------- */
let FCM='fixos';
function errDeck(){ return Object.entries(S.ans).filter(([id,a])=>!a.ok&&QBY[id]&&!QBY[id].anulada).map(([id])=>'q:'+id); }
function cardFront(k){ if(!k.startsWith('q:')) return esc(CARDS[k][0]); const q=QBY[k.slice(2)]; return `<span class="note">${esc(q.disc)}${q.ass?' · '+esc(q.ass):''}</span><br>${esc(q.stem.length>420?q.stem.slice(0,418)+'…':q.stem)}${q.fmt==='CE'?'<br><span class="note">Certo ou errado?</span>':'<br><span class="note">Qual é a resposta?</span>'}`; }
function cardBack(k){ if(!k.startsWith('q:')) return esc(CARDS[k][1]); const q=QBY[k.slice(2)]; const ans=q.fmt==='CE'?(q.ans==='C'?'Certo':'Errado'):q.ans+') '+q.opts['ABCDE'.indexOf(q.ans)]; return `<b>Gabarito: ${esc(ans)}</b>${q.com?'<br><span style="font-size:14px">'+esc(q.com)+'</span>':''}${S.notes[q.id]?'<div class="notebox" style="margin-top:8px;text-align:left">'+esc(S.notes[q.id])+'</div>':''}`; }
V.flashcards=()=>{
  const keys=FCM==='erros'?errDeck():CARDS.map((c,i)=>String(i));
  const due=keys.filter(k=>!S.cards[k]||S.cards[k].due<=today());
  if(!FC||FC.mode!==FCM) FC={queue:due,i:0,flip:false,mode:FCM};
  const k=FC.queue[FC.i];
  const learned=keys.filter(k=>S.cards[k]&&S.cards[k].step>=2).length;
  return `<div><h1>Flashcards</h1><p class="sub">Vire a carta, diga como foi lembrar e o sistema agenda a próxima revisão. Os cartões dos seus erros são criados sozinhos a partir das questões que você errou.</p></div>
  <div class="seg" role="group" aria-label="Baralho"><button data-fcm="fixos" class="${FCM==='fixos'?'on':''}">Fatos que mais caem (${CARDS.length})</button><button data-fcm="erros" class="${FCM==='erros'?'on':''}">Meus erros (${errDeck().length})</button></div>
  <div class="grid g3"><div class="panel stat"><span>Para hoje</span><b>${FC.queue.length-FC.i}</b></div><div class="panel stat"><span>Dominados</span><b>${learned}/${keys.length}</b></div><div class="panel stat"><span>Total</span><b>${keys.length}</b></div></div>
  ${k==null?`<div class="panel empty">${FCM==='erros'&&!keys.length?'Você ainda não errou nenhuma questão. Quando errar, ela vira cartão aqui.':'Nenhum cartão para hoje. Volte amanhã.'}</div>`:`
  <div class="panel card3d"><div>${cardFront(k)}</div>${FC.flip?`<div class="back">${cardBack(k)}</div>`:''}</div>
  <div class="row" style="justify-content:center">${FC.flip?`<button class="btn" data-fc="0">Não lembrei</button><button class="btn" data-fc="h">Difícil</button><button class="btn pri" data-fc="1">Bom</button><button class="btn" data-fc="e">Fácil</button>`:`<button class="btn pri" id="fcFlip">Mostrar resposta</button>`}</div>`}`;
};
V.flashcards.after=()=>{
  document.querySelectorAll('[data-fcm]').forEach(b=>b.onclick=()=>{FCM=b.dataset.fcm;FC=null;render()});
  const f=$('#fcFlip'); if(f) f.onclick=()=>{FC.flip=true;render()};
  document.querySelectorAll('[data-fc]').forEach(b=>b.onclick=()=>{ const k=FC.queue[FC.i], v=b.dataset.fc, ok=v!=='0';
    schedule(S.cards,k,ok); const it=S.cards[k];
    if(v==='h'){ it.step=Math.max(0,it.step-1); it.due=addDays(today(),1); } if(v==='e'){ it.step=Math.min(STEPS.length-1,it.step+1); it.due=addDays(today(),STEPS[it.step]*2); }
    if(!ok) FC.queue.push(k); FC.i++; FC.flip=false; activity(); gain(ok?5:2); persist(); render(); });
};

/* ---------- Edital verticalizado ---------- */
function vertStats(d,a){ const qs=REAL.filter(q=>q.disc===d&&(!a||q.ass===a)&&!q.anulada); let n=0,h=0; qs.forEach(q=>{const x=S.ans[q.id]; if(x){n++; if(x.ok)h++}}); return {tot:qs.length,n,h,pct:n?Math.round(100*h/n):0}; }
V.edital=()=>{
  let all=0, done=0, teoria=0;
  const body=VERT.blocos.map(bl=>`<div class="panel"><h2>${esc(bl.n)}</h2>${bl.m.map(m=>`<div class="vgrp"><h3>${esc(m.d)}</h3><div class="tw"><table class="vert"><thead><tr><th style="width:34px"><span class="sr">Teoria estudada</span></th><th>Assunto do edital</th><th class="num">Questões</th><th class="num">Acerto</th><th></th></tr></thead><tbody>${m.itens.map(([t,d,a])=>{ const key=VERT.titulo+'|'+t; const st=d?vertStats(d,a):{tot:0,n:0,pct:0}; all++; if(S.ed[key]) teoria++; if(st.n>=5&&st.pct>=70) done++;
    return `<tr><td><input type="checkbox" data-ed="${esc(key)}" ${S.ed[key]?'checked':''} aria-label="Teoria estudada: ${esc(t)}"></td><td>${esc(t)}</td><td class="num">${st.tot?st.n+'/'+st.tot:'–'}</td><td class="num">${st.n?`<span class="chip ${st.pct>=70?'ok':st.pct>=50?'warn':'bad'}">${st.pct}%</span>`:'–'}</td><td>${st.tot?`<a class="btn sm" href="#questoes" data-vd="${esc(d)}" data-va="${esc(a)}" style="text-decoration:none">Treinar</a>`:''}</td></tr>`}).join('')}</tbody></table></div></div>`).join('')}</div>`).join('');
  return `<div><h1>Edital verticalizado</h1><p class="sub">${esc(VERT.titulo)}. Cada linha é um assunto do Anexo II do edital. Marque a teoria quando estudar; as colunas de questões e acerto se preenchem sozinhas com o que você resolve aqui.</p></div>
  <div class="grid g3"><div class="panel stat"><span>Teoria estudada</span><b>${teoria}/${all}</b><div class="bar" style="margin-top:6px"><i style="width:${Math.round(100*teoria/all)}%"></i></div></div>
  <div class="panel stat"><span>Assuntos dominados</span><b>${done}/${all}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">5 ou mais questões com 70% de acerto</span></div>
  <div class="panel stat"><span>Prova</span><b>${daysTo(PROVA_TRT4)>0?daysTo(PROVA_TRT4)+' dias':'feita'}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">31/01/2027 · <a href="${VERT.url}" target="_blank" rel="noopener">edital completo (PDF)</a></span></div></div>
  ${body}<p class="note">Alguns assuntos ainda têm poucas questões no banco (Direitos Humanos, Informática, Regimento do TRT4). Nesses, estude pela lei e pelo regimento e use o tutor IA.</p>`;
};
V.edital.after=()=>{
  document.querySelectorAll('[data-ed]').forEach(c=>c.onchange=()=>{ if(c.checked) S.ed[c.dataset.ed]=today(); else delete S.ed[c.dataset.ed]; persist(); render(); });
  document.querySelectorAll('[data-vd]').forEach(b=>b.onclick=()=>qfSet({disc:b.dataset.vd,ass:b.dataset.va,origem:'real',status:'todas'}));
};

/* ---------- Jornada ---------- */
const PROVA_TRT4='2027-01-31', INSC_TRT4='2026-11-25';
const daysTo=iso=>Math.round((new Date(iso+'T12:00:00')-new Date(today()+'T12:00:00'))/864e5);
const FASES=[
 {ate:'2026-11-25',t:'Inscrição no TRT4',p:'Agora até 25/11/2026',txt:'Inscreva-se pela FCC. O edital aceita uma inscrição por turno: Técnico Judiciário, Área Administrativa (manhã, R$ 90, salário de R$ 9.776,71) e Analista Judiciário, Área Administrativa (tarde, R$ 110, R$ 16.040,88). Fazer as duas dobra as chances com o mesmo estudo. Boleto até 26/11.',acao:['Abrir a inscrição na FCC','https://www.concursosfcc.com.br/concursos/trt4r125/index.html']},
 {ate:'2027-01-31',t:'Reta curta para o TRT4',p:'Até 31/01/2027 · cerca de 12 semanas',txt:'As 30 específicas valem o dobro, então elas vêm primeiro: Direito Administrativo (Lei 8.112, Lei 14.133, improbidade, LAI e LGPD), Constitucional, Orçamento e Gestão de Pessoas. Depois Português, Raciocínio e o Regimento Interno do TRT4. Uma redação por semana e um simulado no formato TRT4 a cada 15 dias.',links:[['Edital verticalizado','#edital'],['Simulado TRT4','#simulado'],['Treinar redação','#discursivas']]},
 {ate:'2027-07-05',t:'Prova, gabarito e base completa',p:'Fev a jul/2027',txt:'Gabarito sai em 01/02/2027 e o resultado final está previsto para 05/07/2027. Enquanto isso, complete todos os assuntos do edital verticalizado e refaça as provas FCC de TRT. O cadastro de reserva vale 2 anos, prorrogáveis por mais 2: as nomeações podem vir até 2031.'},
 {ate:'2027-12-31',t:'Onda de TRTs pela FCC',p:'2º semestre de 2027',txt:'TRT23 (FCC já contratada), TRT3 e TRT5 devem publicar edital. Mesmo cargo, mesma banca e mesmo salário: o estudo do TRT4 serve inteiro, só muda o regimento. Meta: 75% nas específicas nos simulados.'},
 {ate:'2028-12-31',t:'Ampliar o leque',p:'2028',txt:'Nove TRTs têm a validade vencendo em 2027 e devem abrir novos concursos; TRF2, TRF6 e o CNU 3 (APO e EPPGG, que combinam com Engenharia de Produção e BI) também. Acrescente AFO aprofundada e Políticas Públicas ao ciclo.'},
 {ate:'2029-12-31',t:'Janela de 2029',p:'2029',txt:'MPU e TRF1 previstos. Quem estudou com constância desde 2026 chega aqui com dois anos de base, o tempo médio de aprovação em tribunais.'},
];
const STL={aberto:['ok','Inscrições abertas'],encerrado:['ghost','Inscrições encerradas'],banca:['hl','Banca contratada'],autorizado:['hl','Autorizado'],comissao:['warn','Comissão formada'],previsto:['ghost','Previsto'],estudo:['ghost','Em estudo']};
function readiness(){
  const g=GERAIS.map(d=>({d,...discStats(d)})), e=ESPEC.map(d=>({d,...discStats(d)}));
  const avg=a=>{ const x=a.filter(r=>r.n>=5); return x.length?x.reduce((t,r)=>t+r.pct,0)/x.length:null; };
  const pg=avg(g), pe=avg(e);
  const nota=pg!=null&&pe!=null?(pg/100*30+pe/100*60)/90*10:null;
  return {g,e,pg,pe,nota};
}
V.jornada=()=>{
  const cur=FASES.findIndex(f=>f.ate>=today()), R=readiness(), dp=daysTo(PROVA_TRT4), di=daysTo(INSC_TRT4);
  const per=x=>x.q<'2027-07'?'1º semestre de 2027':x.q<'2028-01'?'2º semestre de 2027':x.q<'2029-01'?'2028':'2029 em diante';
  const groups=[]; RADAR.slice().sort((a,b)=>a.q.localeCompare(b.q)).forEach(x=>{ const k=per(x); let g=groups.find(y=>y[0]===k); if(!g){g=[k,[]];groups.push(g)} g[1].push(x); });
  const y0=2005,y1=2031, pos=y=>((y-y0)/(y1-y0)*100).toFixed(2);
  const row=r=>`<tr><td>${esc(r.d)}</td><td class="num">${r.n?r.n:'–'}</td><td class="num">${r.n>=5?`<span class="chip ${r.pct>=70?'ok':r.pct>=50?'warn':'bad'}">${r.pct}%</span>`:r.n?r.pct+'%':'–'}</td></tr>`;
  return `<div><h1>Sua jornada até a posse</h1><p class="sub">Alvo: Analista Judiciário, Área Administrativa, em tribunal do trabalho, começando pelo TRT4. Abaixo, as fases do caminho, os concursos previstos para 2027 e 2028 e a frequência com que cada órgão abre edital.</p></div>
  <section class="panel hero">
   <div style="display:flex;flex-direction:column;gap:8px;min-width:0"><span class="chip ok" style="align-self:flex-start">Edital aberto · FCC</span><h2 style="font-size:22px">TRT4 2026: prova em 31/01/2027</h2>
    <p class="note" style="margin:0">Analista R$ 16.040,88 · Técnico R$ 9.776,71 · cadastro de reserva · Porto Alegre. ${di>=0?`<b>Inscrições até 25/11/2026 (${di===0?'hoje':'faltam '+di+' dias'})</b>.`:'Inscrições encerradas.'}</p>
    <div class="row"><a class="btn pri" href="https://www.concursosfcc.com.br/concursos/trt4r125/index.html" target="_blank" rel="noopener" style="text-decoration:none">${di>=0?'Fazer a inscrição':'Página do concurso'}</a><a class="btn" href="#edital" style="text-decoration:none">Edital verticalizado</a></div></div>
   <div class="lvlbox"><span class="stat"><span>Contagem regressiva</span><b>${dp>0?dp+' dias':'Prova feita'}</b></span>
    <span class="stat"><span>Nota estimada no critério do edital</span><b style="color:${R.nota==null?'inherit':R.nota>=6?'var(--ok)':'var(--bad)'}">${R.nota==null?'–':R.nota.toFixed(1).replace('.',',')}</b></span>
    <span class="note">${R.nota==null?'Resolva pelo menos 5 questões em cada matéria geral e específica para ver a estimativa.':'Média do seu acerto (gerais com peso 1, específicas com peso 2). O mínimo do edital é 6.'}</span></div>
  </section>
  <div class="panel"><h2>Fases</h2><ol class="fases">${FASES.map((f,i)=>`<li class="${i<cur?'past':i===cur?'now':''}"><div class="dot" aria-hidden="true"></div><div style="min-width:0"><div class="row between"><b>${esc(f.t)}</b><span class="note">${esc(f.p)}${i===cur?' · <b>você está aqui</b>':''}</span></div><p class="note" style="margin:4px 0 0">${esc(f.txt)}</p>${f.acao?`<a class="btn sm pri" href="${f.acao[1]}" target="_blank" rel="noopener" style="text-decoration:none;margin-top:8px;display:inline-block">${esc(f.acao[0])}</a>`:''}${f.links?`<div class="row" style="gap:6px;margin-top:8px">${f.links.map(([l,u])=>`<a class="btn sm" href="${u}" style="text-decoration:none">${esc(l)}</a>`).join('')}</div>`:''}</div></li>`).join('')}</ol></div>
  <div class="grid g2"><div class="panel"><h3>Prontidão: conhecimentos gerais (peso 1)</h3><div class="tw"><table><thead><tr><th>Matéria</th><th class="num">Resolvidas</th><th class="num">Acerto</th></tr></thead><tbody>${R.g.map(row).join('')}</tbody></table></div></div>
   <div class="panel"><h3>Prontidão: específicas de Analista Administrativo (peso 2)</h3><div class="tw"><table><thead><tr><th>Matéria</th><th class="num">Resolvidas</th><th class="num">Acerto</th></tr></thead><tbody>${R.e.map(row).join('')}</tbody></table></div><p class="note">Meta: 70% nas gerais e 75% nas específicas.</p></div></div>
  <div class="panel"><div class="row between"><h2>Concursos previstos: 2027 e 2028</h2><span class="note">conferido em ${RADAR_DATA}</span></div>
   ${groups.map(([g,xs])=>`<h3 style="margin:16px 0 6px">${g}</h3><div class="radar">${xs.map(x=>{const [k,l]=STL[x.st]||['ghost',x.st];return `<div class="rcard ${x.alvo?'alvo':''}"><div class="row between" style="gap:6px"><b>${esc(x.o)}</b><span class="chip ${k}">${l}</span></div><div class="note">${esc(x.c)} · ${esc(x.b)}</div><div style="font-size:13.5px">${esc(x.quando)}</div><div class="note">Remuneração: ${esc(x.sal)}${x.val?' · validade: '+esc(x.val):''}</div>${x.nota?`<div class="note">${esc(x.nota)}</div>`:''}<div class="row" style="gap:6px;margin-top:2px"><a class="note" href="${x.url}" target="_blank" rel="noopener">Fonte: ${esc(x.fonte)}</a>${x.tipo?`<a class="btn sm" href="#questoes" data-jt="${x.tipo}" style="text-decoration:none;margin-left:auto">Treinar</a>`:''}</div></div>`}).join('')}</div>`).join('')}
   <p class="note">Concursos “previstos” ou “em estudo” podem atrasar ou não acontecer. Só o edital publicado garante datas e vagas.</p></div>
  <div class="panel"><h2>Frequência de abertura</h2><p class="note">Anos em que cada órgão aplicou prova para analista. Com isso dá para estimar o intervalo médio e a próxima janela provável. São levantamentos em fontes públicas: use como tendência, não como data.</p>
   <div class="hist" role="table" aria-label="Histórico de concursos por órgão"><div class="hrow head" role="row"><span role="columnheader">Órgão</span><span role="columnheader" class="axis">${[2006,2010,2014,2018,2022,2026,2030].map(y=>`<i style="left:${pos(y)}%">${y}</i>`).join('')}</span><span role="columnheader" class="num">Intervalo</span><span role="columnheader">Próxima janela (estimativa)</span></div>
   ${HIST.map(h=>{ const a=h.anos, iv=a.length>1?(a[a.length-1]-a[0])/(a.length-1):null, nx=iv?Math.round(a[a.length-1]+iv):null, live=RADAR.find(r=>norm(r.o).split(' ')[0]===norm(h.o).split(' ')[0]&&r.st!=='encerrado');
     return `<div class="hrow" role="row"><span role="cell"><b>${esc(h.o)}</b><br><span class="note">${esc(h.b)}</span></span><span role="cell" class="axis" aria-label="${a.join(', ')}">${a.map(y=>`<i class="pt" style="left:${pos(y)}%" title="${y}">${y}</i>`).join('')}${nx&&nx<=y1?`<i class="pt est" style="left:${pos(Math.min(nx,y1))}%" title="estimativa ${nx}">${nx}?</i>`:''}</span><span role="cell" class="num">${iv?'~'+iv.toFixed(1).replace('.',',')+' anos':'–'}</span><span role="cell">${live?`<span class="chip ${STL[live.st][0]}">${STL[live.st][1]}</span> ${esc(live.quando.split(';')[0])}`:nx?'por volta de '+nx:'–'}</span></div>`;}).join('')}
   </div>
   <h3 style="margin-top:16px">O ritmo da FCC nos tribunais do trabalho</h3>
   <div class="tw"><table><thead><tr><th>Ano</th><th>Provas de Analista aplicadas pela FCC</th></tr></thead><tbody>${FCC_TRT.map(([y,xs])=>`<tr><td class="num">${y}</td><td>${xs.join(', ')}</td></tr>`).join('')}</tbody></table></div>
   <p class="note">Entre 2022 e 2025 a FCC aplicou pelo menos 13 provas de Analista em TRTs e no TRF4, cerca de 3 por ano. Para quem mira tribunal do trabalho, isso quer dizer um edital novo a cada 3 a 5 meses no país. Cada um exige o regimento do próprio tribunal; o resto do edital é quase igual.</p></div>`;
};
V.jornada.after=()=>{ document.querySelectorAll('[data-jt]').forEach(b=>b.onclick=()=>qfSet({tipo:b.dataset.jt})); };

/* ---------- Discursivas ---------- */
const RED_REAL={t:'A importância da relação entre “tempo de trabalho” e “tempo livre” na vida do indivíduo contemporâneo',b:'FCC',f:'Texto dissertativo-argumentativo, 20 a 30 linhas',real:'TRT4 2022, Analista Judiciário – Área Administrativa',apoio:'Texto de apoio: trecho de Ricardo Antunes, “Adeus ao trabalho?”, sobre redução da jornada, tempo livre e sentido do trabalho.',url:'https://arquivos.qconcursos.com/prova/arquivo_prova/88706/fcc-2022-trt-4-regiao-rs-analista-judiciario-area-administrativa-prova.pdf'};
const RED_TEMAS=[RED_REAL,...TEMAS_RED];
const RUBRICA='Critérios da FCC no edital do TRT4 (Capítulo 10): Conteúdo até 40 pontos (perspectiva sobre o tema, análise e senso crítico, consistência e coerência dos argumentos); Estrutura até 30 pontos (respeito ao gênero dissertativo-argumentativo, progressão textual, coesão entre frases e parágrafos); Expressão até 30 pontos (norma-padrão: sintaxe, concordância, regência, pontuação, pronomes, tempos verbais, grafia e acentuação). Nota zero se fugir ao tema ou ao gênero. Entre 20 e 30 linhas. Aprovação com 60 de 100.';
let RD={i:0,txt:''};
const linhas=t=>t.split('\n').reduce((n,l)=>n+Math.max(1,Math.ceil(l.length/70)),0);
V.discursivas=()=>{
  const T=RED_TEMAS[RD.i]; const w=RD.txt.trim()?RD.txt.trim().split(/\s+/).length:0, L=RD.txt.trim()?linhas(RD.txt.trim()):0;
  return `<div><h1>Discursivas</h1><p class="sub">A redação do TRT4 vale 10 pontos, precisa de nota 6 e é corrigida só para os mais bem colocados na objetiva (até o 80º de Analista Administrativo). Treine aqui no formato da FCC e peça uma correção comentada à IA.</p></div>
  <div class="panel" style="display:flex;flex-direction:column;gap:10px">
   <label class="f">Tema<select id="rdT">${RED_TEMAS.map((t,i)=>`<option value="${i}" ${i===RD.i?'selected':''}>${t.real?'Prova real · ':'Treino · '}${esc(t.t)}</option>`).join('')}</select></label>
   <div class="cmd" style="font-style:normal"><b>${esc(T.t)}</b><br><span class="note">${esc(T.f)}${T.real?' · caiu em '+esc(T.real)+' · <a href="'+T.url+'" target="_blank" rel="noopener">ver na prova</a>':' · tema de treino escrito por IA, não caiu em prova'}</span>${T.apoio?'<br><span class="note">'+esc(T.apoio)+'</span>':''}</div>
   <textarea id="rdTxt" class="ta red" rows="16" placeholder="Escreva sua redação aqui. Na prova, a folha tem 30 linhas; conte cerca de 70 caracteres por linha manuscrita.">${esc(RD.txt)}</textarea>
   <div class="row between"><span class="note" id="rdCnt">${w} palavras · cerca de ${L} linhas ${L&&(L<20||L>30)?'<b style="color:var(--bad)">(fora de 20 a 30)</b>':''}</span><div class="row" style="gap:6px"><button class="btn" id="rdSave">Guardar</button><button class="btn pri" id="rdAi">Corrigir com IA</button></div></div>
   <div id="rdOut"></div>
   <p class="note" style="margin:0">${esc(RUBRICA)} A correção por IA é um treino e não substitui a banca.</p>
  </div>
  ${(S.red||[]).length?`<div class="panel"><h3>Suas redações</h3><div class="tw"><table><thead><tr><th>Data</th><th>Tema</th><th class="num">Linhas</th><th>Nota da IA</th><th></th></tr></thead><tbody>${S.red.slice().reverse().map(r=>`<tr><td>${isoBR(r.d)}</td><td>${esc(r.tema)}</td><td class="num">${linhas(r.txt)}</td><td>${r.nota!=null?r.nota+'/100':'–'}</td><td><button class="btn sm" data-rdo="${esc(r.id)}">Abrir</button></td></tr>`).join('')}</tbody></table></div></div>`:''}`;
};
V.discursivas.after=()=>{
  const ta=$('#rdTxt'), cnt=$('#rdCnt');
  ta.oninput=()=>{ RD.txt=ta.value; const t=ta.value.trim(), w=t?t.split(/\s+/).length:0, L=t?linhas(t):0; cnt.innerHTML=`${w} palavras · cerca de ${L} linhas ${L&&(L<20||L>30)?'<b style="color:var(--bad)">(fora de 20 a 30)</b>':''}`; };
  $('#rdT').onchange=e=>{RD.i=+e.target.value;render()};
  const save=(nota,fb)=>{ const T=RED_TEMAS[RD.i]; S.red=S.red||[]; const id=RD.id||('r'+Date.now()); RD.id=id; const old=S.red.findIndex(r=>r.id===id); const rec={id,d:today(),tema:T.t,txt:RD.txt,nota:nota!=null?nota:(old>=0?S.red[old].nota:null),fb:fb||(old>=0?S.red[old].fb:'')}; if(old>=0) S.red[old]=rec; else S.red.push(rec); S.red=S.red.slice(-30); persist(); };
  $('#rdSave').onclick=()=>{ if(!RD.txt.trim()) return; save(); activity(); gain(10,'Redação guardada · +10 XP'); render(); };
  $('#rdAi').onclick=async()=>{
    const out=$('#rdOut'); if(!RD.txt.trim()){ out.innerHTML='<div class="note">Escreva o texto primeiro.</div>'; return; }
    if(!aiReady()){ out.innerHTML=aiSetupHTML(); return; }
    const T=RED_TEMAS[RD.i], b=$('#rdAi'); b.disabled=true; out.innerHTML='<div class="tutor">Corrigindo…</div>'; const box=out.firstChild;
    const prompt=`Você é corretor de redações de concursos da banca FCC. Corrija a redação abaixo de um candidato a Analista Judiciário do TRT4, em português, usando estes critérios do edital: ${RUBRICA}
Tema proposto: ${T.t}
Responda em texto simples, sem markdown, neste formato:
NOTA: <número de 0 a 100>
Conteúdo (x/40): duas ou três frases.
Estrutura (x/30): duas ou três frases.
Expressão (x/30): liste até 5 desvios da norma-padrão, citando o trecho e a correção.
Para subir a nota: três ações concretas.
Seja exigente como a banca e não invente erros. Se o texto fugir ao tema, diga e dê nota zero.

REDAÇÃO:
${RD.txt}`;
    try{ const t=await aiCall(prompt,{onText:x=>{box.textContent=x}}); box.textContent=t; const m=t.match(/NOTA:\s*(\d{1,3})/); const nota=m?Math.min(100,+m[1]):null; save(nota,t); activity(); gain(20,'Redação corrigida · +20 XP'); out.insertAdjacentHTML('beforeend','<div class="ai" style="margin-top:6px">Correção gerada por IA a partir dos critérios do edital. Não é a correção da FCC.</div>'); }
    catch(e){ box.textContent=aiErr(e); }
    b.disabled=false;
  };
  document.querySelectorAll('[data-rdo]').forEach(b=>b.onclick=()=>{ const r=S.red.find(x=>x.id===b.dataset.rdo); if(!r) return; RD={i:Math.max(0,RED_TEMAS.findIndex(t=>t.t===r.tema)),txt:r.txt,id:r.id}; render(); if(r.fb) $('#rdOut').innerHTML=`<div class="tutor">${esc(r.fb)}</div>`; window.scrollTo({top:0}); });
};

/* ---------- Agenda semanal (no Plano) ---------- */
const DIAS=['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'];
function agendaHTML(){
  const A=S.agenda||{dias:[1,1,1,1,1,1,0],min:[90,90,90,90,90,180,0]};
  const R=planRows().slice(); const blocks=[]; let k=0;
  const plan=DIAS.map((d,i)=>{ if(!A.dias[i]) return {d,items:[]}; const nb=Math.max(1,Math.floor((A.min[i]||0)/50)); const items=['Revisão do dia e flashcards (15 min)']; for(let j=0;j<nb;j++){ items.push(R[k%R.length].d); k++; } return {d,items,min:A.min[i]}; });
  const tot=A.dias.reduce((t,on,i)=>t+(on?(A.min[i]||0):0),0);
  return `<div class="panel"><div class="row between"><h3>Agenda da semana</h3><span class="note">${(tot/60).toFixed(1).replace('.',',')} h por semana</span></div>
   <p class="note">Marque os dias em que você estuda e quanto tempo tem. A agenda distribui os blocos de 50 minutos pela ordem de prioridade do seu ciclo (as matérias que mais precisam aparecem primeiro).</p>
   <div class="agcfg">${DIAS.map((d,i)=>`<label class="chk"><input type="checkbox" data-agd="${i}" ${A.dias[i]?'checked':''}> ${d}</label><select data-agm="${i}" aria-label="Minutos em ${d}" ${A.dias[i]?'':'disabled'}>${[30,60,90,120,180,240].map(m=>`<option value="${m}" ${m===A.min[i]?'selected':''}>${m>=60?(m/60).toString().replace('.',',')+' h':m+' min'}</option>`).join('')}</select>`).join('')}</div>
   <div class="agenda">${plan.map(p=>`<div class="agday ${p.items.length?'':'off'}"><b>${p.d}</b>${p.items.length?p.items.map(t=>`<span>${esc(t)}</span>`).join(''):'<span class="note">descanso</span>'}</div>`).join('')}</div>
   <div class="row" style="margin-top:10px">${IS_ART?'<span class="note">A exportação para o calendário (.ics) está disponível na versão site.</span>':`<a class="btn sm" href="data:text/calendar;charset=utf-8,${encodeURIComponent(icsAgenda(plan))}" download="agenda-rumo-a-posse.ics">Baixar para o calendário (.ics)</a>`}</div></div>`;
}
function icsAgenda(plan){
  const base=new Date(today()+'T12:00:00'); const dow=(base.getDay()+6)%7; const mon=addDays(today(),-dow);
  const pad=n=>String(n).padStart(2,'0');
  let s='BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Rumo a Posse//PT\r\n';
  plan.forEach((p,i)=>{ if(!p.items.length) return; const d=addDays(mon,i).replace(/-/g,''); const dur=p.min||60;
    s+=`BEGIN:VEVENT\r\nUID:rumo-${d}-${i}@rumo\r\nDTSTART:${d}T190000\r\nDURATION:PT${Math.floor(dur/60)}H${pad(dur%60)}M\r\nRRULE:FREQ=WEEKLY\r\nSUMMARY:Estudo: ${p.items.slice(1).join(', ').replace(/[,;]/g,m=>'\\'+m)}\r\nEND:VEVENT\r\n`; });
  return s+'END:VCALENDAR\r\n';
}
const _plano=V.plano, _planoAfter=V.plano.after;
V.plano=()=>_plano()+agendaHTML();
V.plano.after=()=>{ _planoAfter();
  const A=S.agenda=S.agenda||{dias:[1,1,1,1,1,1,0],min:[90,90,90,90,90,180,0]};
  document.querySelectorAll('[data-agd]').forEach(c=>c.onchange=()=>{ A.dias[+c.dataset.agd]=c.checked?1:0; if(c.checked&&!A.min[+c.dataset.agd]) A.min[+c.dataset.agd]=60; persist(); render(); });
  document.querySelectorAll('[data-agm]').forEach(s=>s.onchange=()=>{ A.min[+s.dataset.agm]=+s.value; S.plan.horas=Math.round(A.dias.reduce((t,on,i)=>t+(on?A.min[i]:0),0)/60); persist(); render(); });
};

/* ---------- Início: chamada da jornada ---------- */
const _painel=V.painel, _painelAfter=V.painel.after;
V.painel=()=>{
  const dp=daysTo(PROVA_TRT4), di=daysTo(INSC_TRT4);
  const top=`${!(S.perfil&&S.perfil.nome)?`<div class="panel row between" style="gap:10px"><div><b>Como você quer ser chamado?</b><div class="note">Seu nome aparece na saudação e fica salvo com o seu progresso.</div></div><form id="nmF" class="row" style="gap:6px"><input id="nmI" class="in" placeholder="Seu nome" aria-label="Seu nome" autocomplete="given-name"><button class="btn pri" type="submit">Salvar</button></form></div>`:''}
  ${dp>0?`<div class="panel jcall"><div style="min-width:0"><span class="chip ok">Seu alvo · edital aberto</span><h2 style="margin-top:6px">TRT4: prova em ${dp} dias</h2><p class="note" style="margin:4px 0 0">${di>=0?`Inscrições até 25/11 (${di===0?'último dia':'faltam '+di+' dias'}). Dá para fazer Técnico de manhã e Analista à tarde.`:'Inscrições encerradas. Foco total na reta final.'}</p></div><div class="row"><a class="btn pri" href="#jornada" style="text-decoration:none">Ver a jornada</a><a class="btn" href="#edital" style="text-decoration:none">Edital verticalizado</a></div></div>`:''}`;
  return top+_painel();
};
V.painel.after=()=>{ _painelAfter(); const f=$('#nmF'); if(f) f.onsubmit=e=>{ e.preventDefault(); const v=$('#nmI').value.trim().slice(0,40); if(!v) return; S.perfil=Object.assign({},S.perfil,{nome:v}); persist(); render(); }; };

/* ---------- Perfil ---------- */
function applyTheme(){ const t=lsGet('rumo.theme'); if(t) document.documentElement.dataset.theme=t; else delete document.documentElement.dataset.theme; }
applyTheme();
V.perfil=()=>{
  const key=lsGet(AIKEY), model=lsGet(AIMODEL)||'claude-opus-5-5', th=lsGet('rumo.theme');
  return `<div><h1>Perfil e conta</h1><p class="sub">Seu nome, a sincronização entre aparelhos, o backup e as preferências.</p></div>
  <div class="panel" style="display:flex;flex-direction:column;gap:12px"><h2>Você</h2>
   <div class="grid g3"><label class="f">Nome<input id="pfN" class="in" value="${esc(S.perfil&&S.perfil.nome||'')}" maxlength="40" autocomplete="given-name"></label>
   <label class="f">Meta de questões por dia<input id="pfG" class="in" type="number" min="5" max="200" value="${S.goal}"></label>
   <label class="f">Tema<select id="pfT"><option value="" ${!th?'selected':''}>Automático</option><option value="light" ${th==='light'?'selected':''}>Claro</option><option value="dark" ${th==='dark'?'selected':''}>Escuro</option></select></label></div></div>
  <div class="panel" style="display:flex;flex-direction:column;gap:10px"><div class="row between"><h2>Sincronização</h2><span class="chip ghost" data-sync>${esc(SYNC_TXT)}</span></div><div id="authSlot"></div></div>
  <div class="panel" style="display:flex;flex-direction:column;gap:10px"><h2>Backup</h2><div id="bkSlot"></div></div>
  <div class="panel" style="display:flex;flex-direction:column;gap:10px"><h2>Tutor IA</h2>
   ${IS_ART?'<p class="note" style="margin:0">Nesta versão do claude.ai, o tutor e a correção de redação funcionam sem configurar nada.</p>':`<p class="note" style="margin:0">No site, o tutor usa a sua própria chave da API da Anthropic (crie em <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">console.anthropic.com</a>). A chave fica só neste navegador, não vai para a sincronização, e cada explicação custa centavos na sua conta. Se preferir não usar chave, abra a <a href="https://claude.ai/artifact/KMMxfikPC7cV323XHVfhQE" target="_blank" rel="noopener">versão do claude.ai</a>.</p>
   <div class="grid g2"><label class="f">Chave da API<input id="pfK" class="in" type="password" autocomplete="off" placeholder="sk-ant-…" value="${key?'••••••••••••':''}"></label>
   <label class="f">Modelo<select id="pfM"><option value="claude-opus-5-5" ${model==='claude-opus-5-5'?'selected':''}>Claude Opus 5.5 (padrão)</option><option value="claude-haiku-5-5" ${model==='claude-haiku-5-5'?'selected':''}>Claude Haiku 5.5 (mais barato)</option></select></label></div>
   <div class="row" style="gap:6px"><button class="btn sm pri" id="pfKs">Salvar chave</button>${key?'<button class="btn sm" id="pfKd">Remover chave</button><button class="btn sm" id="pfKt">Testar</button>':''}<span class="note" id="pfKm"></span></div>`}</div>
  <div class="panel"><h2>Sobre esta versão</h2><p class="note">Rumo à Posse v14 · ${REAL.length} questões de provas reais + ${IAQ.length} inéditas (IA) · dados de concursos conferidos em ${EDITAIS_DATA}. ${IS_ART?'Versão do claude.ai.':'Site: <a href="https://02q1.github.io/rumo-a-posse/" target="_blank" rel="noopener">02q1.github.io/rumo-a-posse</a>. Funciona sem internet depois da primeira visita.'}</p></div>`;
};
V.perfil.after=()=>{
  authUI(); backupUI();
  $('#pfN').onchange=e=>{ S.perfil=Object.assign({},S.perfil,{nome:e.target.value.trim().slice(0,40)}); persist(); toast('Nome salvo'); };
  $('#pfG').onchange=e=>{ S.goal=Math.max(5,Math.min(200,+e.target.value||20)); persist(); toast('Meta salva'); };
  $('#pfT').onchange=e=>{ lsSet('rumo.theme',e.target.value); applyTheme(); };
  const ks=$('#pfKs'); if(ks){
    const m=t=>{$('#pfKm').textContent=t};
    ks.onclick=()=>{ const v=$('#pfK').value.trim(); if(!v||v.startsWith('•')){ m('Cole a chave no campo.'); return; } lsSet(AIKEY,v); m('Chave salva neste navegador.'); render(); };
    $('#pfM').onchange=e=>{ lsSet(AIMODEL,e.target.value); m('Modelo salvo.'); };
    const kd=$('#pfKd'); if(kd) kd.onclick=()=>{ lsSet(AIKEY,''); render(); };
    const kt=$('#pfKt'); if(kt) kt.onclick=async()=>{ m('Testando…'); try{ const t=await aiCall('Responda apenas: ok'); m('Funcionando: '+t.slice(0,40)); }catch(e){ m(aiErr(e)); } };
  }
};

/* ---------- Mais (menu do celular) ---------- */
const MENU=[['Estudo',[['questoes','Questões','Banco com filtros, busca e favoritas'],['simulado','Simulados','Formato TRT4, personalizado ou prova inteira'],['revisao','Revisão','Revisão espaçada e caderno de erros'],['flashcards','Flashcards','Fatos que mais caem e seus erros'],['discursivas','Discursivas','Redação no formato FCC com correção por IA'],['aulas','Aulas','Vídeos gratuitos por assunto']]],
 ['Planejamento',[['jornada','Jornada','Fases, concursos de 2027-2028 e frequência'],['edital','Edital verticalizado','TRT4 2026, assunto por assunto'],['plano','Plano e agenda','Ciclo semanal e agenda'],['estatisticas','Desempenho','Acerto por matéria, banca e prova']]],
 ['Concursos',[['editais','Editais abertos','Inscrições abertas agora'],['concursos','Carreiras','Cargos acima de R$ 8 mil'],['bancas','Bancas','Como cada banca cobra']]],
 ['Conta',[['perfil','Perfil e conta','Nome, sincronização, backup e tutor IA']]]];
V.mais=()=>`<div><h1>Mais</h1><p class="sub">Todas as seções da plataforma.</p></div>${MENU.map(([g,xs])=>`<div class="panel"><h3>${g}</h3><div class="tiles">${xs.map(([r,t,d])=>`<a class="tile" href="#${r}"><b>${t}</b><span class="note">${d}</span></a>`).join('')}</div></div>`).join('')}<p class="note" data-sync>${esc(SYNC_TXT)}</p>`;

/* ---------- Simulado: nota no critério do edital ---------- */
const _simResult=simResult;
simResult=function(){ return _simResult().replace('<div class="panel"><h3>Por matéria</h3>',trt4NotaHTML()+'<div class="panel"><h3>Por matéria</h3>'); };

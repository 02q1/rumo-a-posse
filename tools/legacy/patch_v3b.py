p='app/template.html'; s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:90],s.count(a)); s=s.replace(a,b)
R("badges:{}});","badges:{}, daily:{}, xpd:{}});")
# gain tracks xp per day + confetti on level up
R("function gain(x,msg){ const before=lvl(S.xp).i; S.xp+=x; const after=lvl(S.xp).i; if(after>before) toast('Subiu de nível: '+LEVELS[after]+'!'); else if(msg) toast(msg); checkBadges(); }",
"""function gain(x,msg){ const before=lvl(S.xp).i; S.xp+=x; const d=today(); S.xpd=S.xpd||{}; S.xpd[d]=(S.xpd[d]||0)+x; const after=lvl(S.xp).i; if(after>before){ toast('Nova parada na trilha: '+LEVELS[after]+'!'); confetti(120); } else if(msg) toast(msg); checkBadges(); }
function weekXP(off=0){ let t=0; const base=new Date(today()+'T12:00:00'); const dow=(base.getDay()+6)%7; const start=addDays(today(),-dow-7*off); for(let i=0;i<7;i++){ t+=(S.xpd||{})[addDays(start,i)]||0 } return t; }
/* Efeito de confete (respeita movimento reduzido) */
function confetti(n=60){
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const c=document.createElement('canvas'); c.className='fx'; document.body.appendChild(c);
  const W=c.width=innerWidth*devicePixelRatio, H=c.height=innerHeight*devicePixelRatio, ctx=c.getContext('2d');
  const cs=getComputedStyle(document.documentElement), cols=['--mark','--accent','--ok','--bad'].map(v=>cs.getPropertyValue(v).trim()||'#ffd43b');
  const P=Array.from({length:n},()=>({x:W/2+(Math.random()-.5)*W*.3,y:H*.55,vx:(Math.random()-.5)*W*.018,vy:-(Math.random()*H*.022+H*.01),r:(Math.random()*6+4)*devicePixelRatio,c:cols[Math.floor(Math.random()*cols.length)],a:Math.random()*6}));
  let t=0; (function f(){ ctx.clearRect(0,0,W,H); P.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=H*.0009;p.a+=.2;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.a);ctx.fillStyle=p.c;ctx.fillRect(-p.r/2,-p.r/4,p.r,p.r/2);ctx.restore()}); if(++t<90) requestAnimationFrame(f); else c.remove(); })();
}
/* Missões do dia */
function dayRec(){ const d=today(); S.daily=S.daily||{}; if(!S.daily[d]){ S.daily[d]={n:0,ok:0,max:0,rev:0,disc:{},banca:{},claimed:{}}; const ks=Object.keys(S.daily).sort(); while(ks.length>30) delete S.daily[ks.shift()]; } return S.daily[d]; }
let COMBO=0, LASTBONUS=0;
function hashStr(t){ let h=0; for(const ch of t) h=(h*31+ch.charCodeAt(0))|0; return Math.abs(h); }
function missions(){
  const D=dayRec(), h=hashStr(today()), bancas=['Cebraspe','FGV','Cesgranrio'], b=bancas[h%3];
  const foco=planRows()[0]?.d||'Língua Portuguesa';
  const pool=[
    {id:'combo',t:'Acerte 5 seguidas',sub:'Combo de 5 acertos sem errar',cur:D.max,goal:5},
    {id:'rev',t:'Revise 5 itens da fila',sub:'A revisão espaçada é o que fixa a matéria',cur:D.rev,goal:5},
    {id:'foco',t:'8 questões de '+foco,sub:'Matéria prioritária do seu plano',cur:D.disc[foco]||0,goal:8},
    {id:'banca',t:'6 questões da '+b,sub:'Treine o estilo da banca',cur:D.banca[b]||0,goal:6},
    {id:'acc',t:'Feche o dia com 70% de acerto',sub:'Mínimo de 10 questões',cur:D.n>=10?Math.round(100*D.ok/D.n):0,goal:70,pct:true},
  ];
  const a=pool[h%pool.length], c=pool[(h+2)%pool.length];
  return [{id:'meta',t:'Bata a meta: '+S.goal+' questões',sub:'Meta diária ajustável no início',cur:D.n,goal:S.goal},a,c].map(m=>({...m,done:m.cur>=m.goal,claimed:!!D.claimed[m.id]}));
}
function checkMissions(){ const D=dayRec(); missions().forEach(m=>{ if(m.done&&!D.claimed[m.id]){ D.claimed[m.id]=1; setTimeout(()=>{ gain(50); toast('Missão cumprida: '+m.t+' (+50 XP)'); confetti(70); },600); } }); }""")
R("""  S.ans[q.id]=a; schedule(S.srs,q.id,ok); activity(); gain(ok?10:3); persist();
  return ok;""","""  const D=dayRec(), wasDue=S.srs[q.id]&&S.srs[q.id].due<=today();
  D.n++; if(ok)D.ok++; if(wasDue)D.rev++; D.disc[q.disc]=(D.disc[q.disc]||0)+1; const bn=SRC[q.src].banca; D.banca[bn]=(D.banca[bn]||0)+1;
  COMBO=ok?COMBO+1:0; D.max=Math.max(D.max||0,COMBO); LASTBONUS=ok&&COMBO>1?Math.min(10,2*(COMBO-1)):0;
  S.ans[q.id]=a; schedule(S.srs,q.id,ok); activity(); gain((ok?10:3)+LASTBONUS); if(ok&&COMBO>0&&COMBO%5===0) confetti(50); checkMissions(); persist();
  return ok;""")
R("""${ok===null?'Item anulado pela banca':ok?'Acertou! +10 XP':'Errou. Foi para o seu caderno de erros (+3 XP pelo esforço)'}""",
"""${ok===null?'Item anulado pela banca':ok?'Acertou! +'+(10+LASTBONUS)+' XP'+(COMBO>1?'<span class="combo">Combo x'+COMBO+'</span>':''):'Errou. Foi para o seu caderno de erros (+3 XP pelo esforço)'}""")
R("['150','Banco inteiro',()=>Object.keys(S.ans).length>=150],","['500','500 questões',()=>Object.keys(S.ans).length>=500],\n  ['x10','Combo de 10',()=>Object.values(S.daily||{}).some(d=>d.max>=10)],\n  ['MIS','Todas as missões do dia',()=>Object.values(S.daily||{}).some(d=>Object.keys(d.claimed||{}).length>=3)],")
# ---------- painel ----------
a=s.index('V.painel=()=>{'); b=s.index('V.painel.after=')
old=s[a:b]
tail=old[old.index('  <div class="panel"><h2>Conquistas</h2>'):]
NEWP='''V.painel=()=>{
  const L=lvl(S.xp), st=streak(), td=S.days[today()]||0, due=dueQs().length;
  const answered=Object.keys(S.ans).length, overall=discStats(), M=missions(), nxt=planRows()[0];
  const wk=weekXP(0), lw=weekXP(1);
  return `
  <section class="hero">
    <div style="display:flex;flex-direction:column;gap:10px;min-width:0">
      <span class="chip hl" style="align-self:flex-start">Parada ${L.i+1} de ${LEVELS.length}: ${esc(L.name)}</span>
      <h1>Bom estudo, Elias. Rumo à <em>posse</em>.</h1>
      <p class="sub" style="margin:0">${S.xp} XP · faltam ${L.need-L.into} XP para ${esc(LEVELS[Math.min(L.i+1,LEVELS.length-1)])}. Cada acerto vale 10 XP, combos dão bônus e cada missão vale 50.</p>
      <div class="row"><a class="btn hl" href="#questoes" data-focus="${esc(nxt?nxt.d:'')}" style="text-decoration:none">Jogar a sessão de hoje</a>${due?`<a class="btn" href="#revisao" style="text-decoration:none">Revisar ${due}</a>`:''}</div>
    </div>
    ${trailSVG(L)}
  </section>
  <div class="grid g2">
    <div class="panel"><div class="row between"><h2>Missões de hoje</h2><span class="note">renovam à meia-noite</span></div>
      <div style="margin-top:6px">${M.map(m=>`<div class="mission ${m.done?'done':''}"><div class="ic">${m.done?'✓':m.id==='combo'?'x5':m.id==='rev'?'↻':m.id==='acc'?'%':m.cur}</div><div style="min-width:0"><b>${esc(m.t)}</b><div class="note">${esc(m.sub)}</div><div class="bar ${m.done?'hl':''}" style="margin-top:6px"><i style="width:${Math.min(100,100*m.cur/m.goal)}%"></i></div></div><span class="xpw">${m.done?'+50 XP ✓':Math.min(m.cur,m.goal)+(m.pct?'%':'')+' / '+m.goal+(m.pct?'%':'')}</span></div>`).join('')}</div></div>
    <div class="grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">
      <div class="panel row" style="gap:12px">${ring(td,S.goal,'Meta do dia')}<div class="stat"><span>Meta do dia</span><b>${td}/${S.goal}</b><div class="row" style="gap:6px"><button class="btn sm" data-goal="-5" aria-label="Diminuir meta">−5</button><button class="btn sm" data-goal="5" aria-label="Aumentar meta">+5</button></div></div></div>
      <div class="panel stat"><span>Sequência</span><b class="streak">${st} dia${st===1?'':'s'}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">Um pouco todo dia mantém a chama.</span></div>
      <div class="panel stat"><span>XP da semana</span><b>${wk}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">${lw?(wk>=lw?'Você já passou a semana passada ('+lw+')':'Faltam '+(lw-wk)+' para bater a semana passada'):'Sua primeira semana conta como recorde'}</span></div>
      <div class="panel stat"><span>Acerto geral</span><b>${overall.n?overall.pct+'%':'–'}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">${answered} resolvidas · ${S.sims.length} simulado${S.sims.length===1?'':'s'}</span></div>
    </div>
  </div>
  ${nxt?`<div class="panel row between"><div style="min-width:0"><h3>Próxima matéria do seu plano: ${esc(nxt.d)}</h3><p class="note" style="margin:4px 0 0">${esc(nxt.why)}</p></div><a class="btn pri" href="#questoes" data-focus="${esc(nxt.d)}" style="text-decoration:none">Treinar agora</a></div>`:''}
'''+tail
s=s[:a]+NEWP+s[b:]
R("document.querySelectorAll('[data-focus]').forEach(b=>b.onclick=()=>{QF={src:'',disc:b.dataset.focus,status:'pend',banca:''};qIdx=0});",
  "document.querySelectorAll('[data-focus]').forEach(b=>b.onclick=()=>{QF={src:'',disc:b.dataset.focus||'',status:'pend',banca:''};qIdx=0});")
# trail svg helper before V.painel
R("V.painel=()=>{","""function trailSVG(L){
  const n=LEVELS.length, W=420, H=200, pts=[];
  for(let k=0;k<n;k++){ const t=k/(n-1); pts.push([24+t*(W-48), 100+Math.sin(t*Math.PI*2.2)*62]); }
  const path=pts.map((p,k)=>(k?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' ');
  const frac=(L.i+L.into/L.need)/(n-1), seg=Math.floor(frac*(n-1)), ft=frac*(n-1)-seg, A=pts[seg], B=pts[Math.min(n-1,seg+1)];
  const me=[A[0]+(B[0]-A[0])*ft, A[1]+(B[1]-A[1])*ft];
  const done=pts.slice(0,seg+1).concat([me]).map((p,k)=>(k?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' ');
  return `<svg class="trail" viewBox="0 0 ${W} ${H}" role="img" aria-label="Trilha da posse: você está na parada ${L.i+1} de ${n}, ${esc(L.name)}"><path class="road" d="${path}"/><path class="done" d="${done}"/>${pts.map((p,k)=>`<circle class="st ${k<=L.i?'ok':''}" cx="${p[0]}" cy="${p[1]}" r="8"/>`).join('')}<circle class="me" cx="${me[0]}" cy="${me[1]}" r="12"/><text x="${pts[0][0]-8}" y="${pts[0][1]+30}">Início</text><text x="${pts[n-1][0]-30}" y="${pts[n-1][1]-18}">Posse</text></svg>`;
}
V.painel=()=>{""")
# ---------- plano adaptativo ----------
R("""V.plano=()=>{
  const A=ALVOS[S.plan.alvo]||ALVOS.tribunal, H=S.plan.horas;
  const study=H*0.75, rev=H*0.25, tot=A.w.reduce((s,x)=>s+x[1],0);
  const rows=A.w.map(([d,w])=>{ const h=study*w/tot; const st=discStats(d); return {d,h,blocks:Math.max(1,Math.round(h*60/50)),st}; });""",
"""function adapt(d,w){ const st=discStats(d); let f=1, why='Peso do edital; ainda sem dados suficientes, então vale o peso padrão.';
  if(st.n>=6){ if(st.pct<50){f=1.6;why='Seu acerto está em '+st.pct+'%: o plano aumentou o tempo desta matéria.'} else if(st.pct<70){f=1.25;why='Acerto de '+st.pct+'%, abaixo da meta de 70%: tempo um pouco maior.'} else if(st.pct>=85&&st.n>=15){f=.75;why='Acerto de '+st.pct+'%: a matéria está madura, o plano reduziu o tempo.'} else why='Acerto de '+st.pct+'%, dentro da meta: mantém o peso.'; }
  return {d,w,f,adj:w*f,st,why}; }
function planRows(){ const A=ALVOS[S.plan.alvo]||ALVOS.tribunal; return A.w.map(([d,w])=>adapt(d,w)).map(r=>({...r,need:r.adj*(r.st.n?(1-r.st.pct/100)+0.3:1.3)/(1+(dayRec().disc[r.d]||0)/8)})).sort((a,b)=>b.need-a.need); }
V.plano=()=>{
  const A=ALVOS[S.plan.alvo]||ALVOS.tribunal, H=S.plan.horas;
  const study=H*0.75, rev=H*0.25, R0=A.w.map(([d,w])=>adapt(d,w)), tot=R0.reduce((s,x)=>s+x.adj,0);
  const rows=R0.map(r=>{ const h=study*r.adj/tot; return {...r,h,blocks:Math.max(1,Math.round(h*60/50))}; });""")
R("""<thead><tr><th>Matéria</th><th class="num">Horas/semana</th><th class="num">Blocos de 50 min</th><th>Seu acerto</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.d)}</td><td class="num">${r.h.toFixed(1)}</td><td class="num">${r.blocks}</td><td>${r.st.n?r.st.pct+'% ('+r.st.n+')':'<span class="note">sem dados</span>'}</td></tr>`).join('')}""",
"""<thead><tr><th>Matéria</th><th class="num">Horas/semana</th><th class="num">Blocos de 50 min</th><th>Seu acerto</th><th>Ajuste automático</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.d)}</td><td class="num">${r.h.toFixed(1)}</td><td class="num">${r.blocks}</td><td>${r.st.n?r.st.pct+'% ('+r.st.n+')':'<span class="note">sem dados</span>'}</td><td>${r.f>1?'<span class="chip bad">+'+Math.round((r.f-1)*100)+'%</span>':r.f<1?'<span class="chip ok">'+Math.round((r.f-1)*100)+'%</span>':'<span class="chip ghost">padrão</span>'}</td></tr>`).join('')}""")
R("<li>A cada 4 semanas, faça um simulado completo e ajuste os pesos: aumente as matérias abaixo de 60%.</li></ol></div>`;",
"""<li>O plano é adaptativo: com 6 ou mais questões numa matéria, ele aumenta o tempo onde seu acerto está abaixo de 70% e reduz onde passa de 85%.</li>
   <li>A cada 4 semanas, faça um simulado completo para medir a evolução.</li></ol></div>`;""")
R("""<p class="sub">Ciclo de estudos semanal no método dos cursinhos de alto índice de aprovação: matérias com peso, blocos de 50 minutos e 25% do tempo para revisão e questões.</p></div>""",
"""<p class="sub">Ciclo de estudos semanal com pesos do edital, blocos de 50 minutos e 25% do tempo para revisão. Os pesos se ajustam sozinhos ao seu desempenho.</p></div>""")
# ---------- perfil estatístico das bancas ----------
R("""  <p style="margin:0"><b>Estratégia:</b> ${esc(x.dica)}</p></div>`).join('')}""","""  ${bancaStats(x.b.split(' ')[0])}
  <p style="margin:0"><b>Estratégia:</b> ${esc(x.dica)}</p></div>`).join('')}""")
R("V.bancas=()=>`","""function bancaStats(b){
  const qs=Q.filter(q=>SRC[q.src].banca===b); if(!qs.length) return '<p class="note" style="margin:0">Ainda sem provas desta banca no banco de questões.</p>';
  const valid=qs.filter(q=>!q.anulada), an=qs.length-valid.length, ce=valid.filter(q=>q.fmt==='CE'), mc=valid.filter(q=>q.fmt==='MC');
  const dc={}; qs.forEach(q=>dc[q.disc]=(dc[q.disc]||0)+1); const top=Object.entries(dc).sort((a,c)=>c[1]-a[1]).slice(0,7), mx=top[0][1];
  const words=Math.round(qs.reduce((t,q)=>t+(q.stem+' '+(q.opts||[]).join(' ')).split(/\\s+/).length,0)/qs.length);
  const provas=new Set(qs.map(q=>q.src)).size;
  let ans='';
  if(ce.length){ const c=ce.filter(q=>q.ans==='C').length; const pc=Math.round(100*c/ce.length); ans+=`<div><h3>Certo ou Errado</h3><div class="bar ok" style="margin-top:8px" role="img" aria-label="${pc}% certo"><i style="width:${pc}%"></i></div><p class="note" style="margin:6px 0 0">${pc}% dos itens são Certos e ${100-pc}% Errados (${ce.length} itens). Não chute sempre o mesmo lado: o equilíbrio é quase meio a meio.</p></div>`; }
  if(mc.length){ const L='ABCDE'.split('').map(l=>[l,mc.filter(q=>q.ans===l).length]); const m2=Math.max(...L.map(x=>x[1])); ans+=`<div><h3>Letra do gabarito</h3><div class="letters" style="margin-top:8px">${L.map(([l,n])=>`<div><span>${Math.round(100*n/mc.length)}%</span><i style="height:${Math.max(4,60*n/m2)}px"></i><b>${l}</b></div>`).join('')}</div><p class="note" style="margin:6px 0 0">Distribuição das respostas em ${mc.length} questões. Nenhuma letra domina, então "chutar sempre C" não funciona.</p></div>`; }
  return `<div class="panel" style="background:var(--bg);box-shadow:none;display:flex;flex-direction:column;gap:14px"><div class="row between"><h3>Raio-X nas questões deste banco</h3><span class="note">${qs.length} questões de ${provas} prova${provas>1?'s':''} · ${an} anulada${an===1?'':'s'} (${(100*an/qs.length).toFixed(1)}%) · enunciado médio de ${words} palavras</span></div>
   <div class="grid g2"><div><h3>Matérias que mais aparecem</h3><div class="bars" style="margin-top:8px">${top.map(([d,n])=>`<div class="l"><span title="${esc(d)}">${esc(d)}</span><div class="bar"><i style="width:${100*n/mx}%"></i></div><span>${Math.round(100*n/qs.length)}%</span></div>`).join('')}</div></div><div style="display:flex;flex-direction:column;gap:14px">${ans}</div></div>
   <p class="note" style="margin:0">Calculado só sobre as provas que estão aqui, não sobre toda a história da banca. As matérias das questões novas foram classificadas automaticamente.</p></div>`;
}
V.bancas=()=>`""")
R("<p class=\"sub\">Como cada banca pensa. Use isso para escolher a estratégia de prova.</p></div>","<p class=\"sub\">Como cada banca pensa, com um raio-X estatístico calculado sobre as provas reais deste banco.</p></div>")
open(p,'w').write(s); print('ok js')

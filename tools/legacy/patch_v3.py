import re
p='app/template.html'; s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:80],s.count(a)); s=s.replace(a,b)
# ---------- head + CSS ----------
i=s.index('<style>'); j=s.index('</style>')+len('</style>')
head_old=s[:i]
CSS=r'''<style>
/* Layout: trilha de jogo sobre cartão-resposta — navegação lateral (barra inferior no celular), coluna de trabalho com cartões arredondados; caneta azul + marca-texto amarelo */
:root{
  --bg:#eef1fb; --paper:#ffffff; --ink:#18214a; --muted:#59628a; --line:#d8ddf0;
  --accent:#3346e0; --accent-soft:#e3e7ff; --on-accent:#ffffff;
  --mark:#ffd43b; --mark-soft:#fff4c2; --on-mark:#18214a;
  --ok:#11905c; --ok-soft:#dcf4e9; --bad:#d9442f; --bad-soft:#fde5e1; --warn:#a96300; --warn-soft:#fff0d6; --gold:#b97f00;
  --sh:rgba(24,33,74,.13);
  --f-display:"Baloo 2", "Trebuchet MS", system-ui, sans-serif;
  --f-read:"Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --f-mono:"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
  --r:16px;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0e1230; --paper:#181d42; --ink:#edefff; --muted:#a4aad0; --line:#2c3366;
  --accent:#8e9cff; --accent-soft:#252c68; --on-accent:#0e1230; --mark:#ffd43b; --mark-soft:#3a3416; --on-mark:#18214a;
  --ok:#46d19a; --ok-soft:#123a2c; --bad:#ff7d6b; --bad-soft:#43201c; --warn:#f2b44c; --warn-soft:#3a2b10; --gold:#ffc93d; --sh:rgba(0,0,0,.45); color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0e1230; --paper:#181d42; --ink:#edefff; --muted:#a4aad0; --line:#2c3366;
  --accent:#8e9cff; --accent-soft:#252c68; --on-accent:#0e1230; --mark:#ffd43b; --mark-soft:#3a3416; --on-mark:#18214a;
  --ok:#46d19a; --ok-soft:#123a2c; --bad:#ff7d6b; --bad-soft:#43201c; --warn:#f2b44c; --warn-soft:#3a2b10; --gold:#ffc93d; --sh:rgba(0,0,0,.45); color-scheme:dark}
*{box-sizing:border-box}
html,body{height:100%}
body{background:var(--bg);color:var(--ink);font:15.5px/1.55 var(--f-read)}
a{color:var(--accent)}
button{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.app{display:grid;grid-template-columns:232px 1fr;min-height:100%}
nav.side{position:sticky;top:0;height:100vh;padding:20px 12px;background:var(--paper);display:flex;flex-direction:column;gap:3px;overflow:auto;box-shadow:1px 0 0 var(--line)}
.brand{font-family:var(--f-display);font-weight:800;font-size:23px;line-height:1.05;padding:0 8px 16px;display:flex;align-items:center;gap:10px}
.brand svg{flex:none}
.brand small{display:block;font-family:var(--f-read);font-weight:400;font-size:11px;color:var(--muted);letter-spacing:.02em}
nav.side a{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:12px;text-decoration:none;color:var(--ink);font-weight:700;font-family:var(--f-display);font-size:16px}
nav.side a svg{flex:none;width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
nav.side a:hover{background:var(--accent-soft)}
nav.side a.on{background:var(--accent);color:var(--on-accent)}
nav.side a .k{font-family:var(--f-mono);font-size:11px;margin-left:auto;background:var(--mark);color:var(--on-mark);border-radius:99px;padding:0 7px;font-weight:600}
nav.side a .k:empty{display:none}
.side .foot{margin-top:auto;font-size:12px;color:var(--muted);padding:10px}
main{min-width:0;padding-block:24px 104px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:1000px;margin:0 auto;display:flex;flex-direction:column;gap:18px}
h1,h2,h3{font-family:var(--f-display);text-wrap:balance;margin:0;line-height:1.15}
h1{font-size:32px;font-weight:800}
h1 em{font-style:normal;background:linear-gradient(transparent 58%,var(--mark) 58%,var(--mark) 92%,transparent 92%);padding:0 4px;color:var(--ink)}
h2{font-size:22px;font-weight:800}
h3{font-size:17px;font-weight:700}
.sub{color:var(--muted);margin:4px 0 0;max-width:70ch}
.panel{background:var(--paper);border-radius:var(--r);padding:18px;box-shadow:0 1px 0 var(--line),0 6px 18px -10px var(--sh)}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
.stat{display:flex;flex-direction:column;gap:2px}
.stat b{font-family:var(--f-display);font-size:30px;font-weight:800;font-variant-numeric:tabular-nums;line-height:1.1}
.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em;font-weight:700}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.between{justify-content:space-between}
.btn{border:2px solid var(--line);background:var(--paper);padding:8px 16px;border-radius:12px;font-weight:800;font-family:var(--f-display);font-size:16px;box-shadow:0 3px 0 var(--line);position:relative;top:0}
.btn:hover{border-color:var(--accent)}
.btn:active:not(:disabled){top:2px;box-shadow:0 1px 0 var(--line)}
.btn.pri{background:var(--accent);border-color:var(--accent);color:var(--on-accent);box-shadow:0 4px 0 color-mix(in srgb,var(--accent) 60%,var(--ink))}
.btn.pri:active:not(:disabled){box-shadow:0 1px 0 color-mix(in srgb,var(--accent) 60%,var(--ink))}
.btn.hl{background:var(--mark);border-color:var(--mark);color:var(--on-mark);box-shadow:0 4px 0 color-mix(in srgb,var(--mark) 55%,#7a5a00)}
.btn.sm{padding:4px 10px;font-size:14px;border-radius:10px}
.btn:disabled{opacity:.45;cursor:not-allowed}
select,input[type=number],input[type=range]{font:inherit;color:var(--ink);background:var(--paper);border:2px solid var(--line);border-radius:10px;padding:7px 9px}
input[type=range]{accent-color:var(--accent);padding:0}
label.f{display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-weight:700;min-width:0}
label.f select{text-transform:none;letter-spacing:0;font-size:14px;font-weight:400;max-width:100%}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:12px;padding:3px 10px;border-radius:999px;background:var(--accent-soft);color:var(--ink);font-weight:700;max-width:100%;white-space:normal}
.chip.ok{background:var(--ok-soft);color:var(--ok)} .chip.bad{background:var(--bad-soft);color:var(--bad)} .chip.warn{background:var(--warn-soft);color:var(--warn)}
.chip.ghost{background:transparent;border:1.5px solid var(--line);color:var(--muted)}
.chip.hl{background:var(--mark);color:var(--on-mark)}
.qmeta{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:12px;color:var(--muted)}
.qnum{font-family:var(--f-mono);font-weight:600;color:var(--ink)}
.support{font-size:15.5px;line-height:1.7;background:var(--bg);border-radius:12px;padding:14px 16px;max-height:340px;overflow:auto}
.support p{margin:0 0 .8em;text-indent:1.5em}
.support p.src{text-indent:0;text-align:right;font-size:13px;color:var(--muted);margin:0}
.cmd{font-style:italic;color:var(--muted)}
.stem{font-size:17px;line-height:1.65;white-space:pre-line;max-width:70ch}
.opts{display:flex;flex-direction:column;gap:9px}
.opt span:last-child{min-width:0}
.opt{display:flex;gap:12px;align-items:flex-start;text-align:left;border:2px solid var(--line);background:var(--paper);border-radius:14px;padding:11px 13px;font-size:16px;line-height:1.5;box-shadow:0 3px 0 var(--line);position:relative;top:0}
.opt:hover:not(:disabled){border-color:var(--accent)}
.opt:active:not(:disabled){top:2px;box-shadow:0 1px 0 var(--line)}
.bub{flex:none;display:inline-grid;place-items:center;width:30px;height:22px;border-radius:50%;border:2px solid var(--ink);font-family:var(--f-mono);font-weight:600;font-size:12px;margin-top:2px}
.opt.sel .bub{background:var(--ink);color:var(--paper)}
.opt.right{border-color:var(--ok);background:var(--ok-soft);box-shadow:0 3px 0 var(--ok)} .opt.right .bub{border-color:var(--ok);background:var(--ok);color:var(--paper)}
.opt.wrong{border-color:var(--bad);background:var(--bad-soft);box-shadow:0 3px 0 var(--bad)} .opt.wrong .bub{border-color:var(--bad);background:var(--bad);color:var(--paper)}
.ce{display:flex;gap:10px}
.ce .opt{flex:1;justify-content:center;font-family:var(--f-display);font-weight:800;font-size:18px}
.fb{border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.fb.ok{background:var(--ok-soft)} .fb.bad{background:var(--bad-soft)} .fb.null{background:var(--warn-soft)}
.fb .h{font-family:var(--f-display);font-weight:800;font-size:20px}
.fb.ok .h{color:var(--ok)} .fb.bad .h{color:var(--bad)} .fb.null .h{color:var(--warn)}
.combo{font-family:var(--f-display);font-weight:800;background:var(--mark);color:var(--on-mark);border-radius:999px;padding:1px 10px;font-size:14px;margin-left:6px}
.ai{font-size:12px;color:var(--muted)}
.links{display:flex;gap:8px;flex-wrap:wrap}
.links a{font-size:13px;text-decoration:none;border:1.5px solid var(--line);border-radius:999px;padding:4px 11px;background:var(--paper);color:var(--ink);font-weight:700}
.links a:hover{border-color:var(--accent)}
.tutor{border-left:4px solid var(--accent);padding:10px 14px;background:var(--paper);border-radius:0 12px 12px 0;white-space:pre-wrap;font-size:15px}
.bar{height:10px;border-radius:99px;background:var(--accent-soft);overflow:hidden}
.bar i{display:block;height:100%;background:var(--accent);border-radius:99px}
.bar.ok i{background:var(--ok)} .bar.bad i{background:var(--bad)} .bar.warn i{background:var(--warn)} .bar.hl i{background:var(--mark)}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-weight:700}
td.num,th.num{text-align:right;font-family:var(--f-mono);font-variant-numeric:tabular-nums}
.tw{overflow-x:auto}
.ring{width:96px;height:96px}
.lvl{font-family:var(--f-display);font-weight:800;font-size:22px}
.streak{color:var(--gold)}
.badges{display:flex;gap:8px;flex-wrap:wrap}
.badge{display:flex;flex-direction:column;align-items:center;gap:4px;width:92px;text-align:center;font-size:11px;color:var(--muted)}
.badge .m{width:50px;height:50px;border-radius:50%;display:grid;place-items:center;border:2px dashed var(--line);font-family:var(--f-display);font-weight:800;font-size:14px}
.badge.on .m{border:3px solid var(--gold);color:var(--on-mark);background:var(--mark)}
.badge.on{color:var(--ink)}
.card3d{min-height:220px;display:flex;flex-direction:column;justify-content:center;gap:14px;text-align:center;font-size:19px;line-height:1.5;padding:28px}
.card3d .back{font-size:16px;color:var(--ink);border-top:2px dashed var(--line);padding-top:14px}
.timer{font-family:var(--f-mono);font-size:22px;font-weight:600}
.sheet{display:grid;grid-template-columns:repeat(auto-fill,minmax(42px,1fr));gap:6px}
.sheet button{border:2px solid var(--line);background:var(--paper);border-radius:8px;padding:4px 0;font-family:var(--f-mono);font-size:12px}
.sheet button.done{background:var(--accent-soft);border-color:var(--accent)}
.sheet button.cur{outline:2px solid var(--ink)}
.sheet button.r{background:var(--ok-soft);border-color:var(--ok)} .sheet button.w{background:var(--bad-soft);border-color:var(--bad)}
.note{font-size:13px;color:var(--muted)}
.empty{padding:28px;text-align:center;color:var(--muted)}
.chart text{fill:var(--muted);font-family:var(--f-mono);font-size:10px}
.chart rect.b{fill:var(--accent)}
.chart line{stroke:var(--line)}
.toast{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(88px + env(safe-area-inset-bottom,0px));background:var(--ink);color:var(--paper);padding:10px 18px;border-radius:999px;font-weight:800;font-family:var(--f-display);z-index:50;font-size:16px;box-shadow:0 8px 24px -8px var(--sh)}
.sync{font-size:11px;font-family:var(--f-mono)}
.plan td.h{font-family:var(--f-mono)}
details summary{cursor:pointer;font-weight:700}
/* Trilha da Posse */
.hero{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:18px;align-items:center;background:var(--accent);color:var(--on-accent);border-radius:22px;padding:22px;box-shadow:0 8px 0 color-mix(in srgb,var(--accent) 60%,var(--ink))}
.hero h1{color:var(--on-accent)} .hero h1 em{color:var(--on-mark)}
.hero .sub{color:var(--on-accent);opacity:.85}
.trail{width:100%;height:auto;display:block}
.trail .road{fill:none;stroke:color-mix(in srgb,var(--on-accent) 30%,transparent);stroke-width:14;stroke-linecap:round}
.trail .done{fill:none;stroke:var(--mark);stroke-width:14;stroke-linecap:round}
.trail circle.st{fill:var(--accent);stroke:var(--on-accent);stroke-width:3}
.trail circle.st.ok{fill:var(--mark);stroke:var(--mark)}
.trail text{fill:var(--on-accent);font-family:var(--f-display);font-weight:700;font-size:13px}
.trail .me{fill:var(--mark);stroke:var(--ink);stroke-width:3}
.mission{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:10px 0;border-bottom:1px dashed var(--line)}
.mission:last-child{border-bottom:0}
.mission .ic{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:var(--accent-soft);font-family:var(--f-display);font-weight:800;color:var(--accent)}
.mission.done .ic{background:var(--mark);color:var(--on-mark)}
.mission b{font-family:var(--f-display);font-size:16px}
.xpw{font-family:var(--f-mono);font-size:12px;color:var(--muted);white-space:nowrap}
.bars{display:flex;flex-direction:column;gap:6px}
.bars .l{display:grid;grid-template-columns:minmax(0,11em) minmax(0,1fr) 3.2em;gap:8px;align-items:center;font-size:13px}
.bars .l span:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bars .l span:last-child{font-family:var(--f-mono);text-align:right}
.letters{display:flex;gap:6px;align-items:flex-end;height:90px}
.letters div{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;font-family:var(--f-mono);font-size:12px;height:100%;justify-content:flex-end}
.letters i{display:block;width:100%;background:var(--accent);border-radius:6px 6px 2px 2px}
canvas.fx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:60}
@media (max-width: 820px){
  .app{grid-template-columns:1fr}
  nav.side{position:fixed;inset:auto 0 0 0;top:auto;height:auto;flex-direction:row;overflow-x:auto;padding:6px max(8px,env(safe-area-inset-left,0px)) calc(6px + env(safe-area-inset-bottom,0px)) max(8px,env(safe-area-inset-right,0px));z-index:20;gap:2px;box-shadow:0 -1px 0 var(--line)}
  .brand,.side .foot{display:none}
  nav.side a{flex-direction:column;gap:2px;font-size:12px;padding:6px 9px;white-space:nowrap;position:relative}
  nav.side a .k{position:absolute;top:2px;right:2px;margin:0}
  .g3,.g4{grid-template-columns:repeat(2,minmax(0,1fr))}
  .hero{grid-template-columns:1fr}
}
@media (max-width: 520px){ .g2{grid-template-columns:1fr} h1{font-size:26px} .stem{font-size:16px} .bars .l{grid-template-columns:minmax(0,8em) minmax(0,1fr) 3em} }
@media (prefers-reduced-motion: no-preference){
  .opt,.btn{transition:border-color .15s, background .15s, top .05s}
  .fb{animation:pop .28s ease-out}
  .opt.wrong{animation:shake .32s ease-in-out}
  @keyframes pop{from{transform:scale(.96);opacity:.4}to{transform:none;opacity:1}}
  @keyframes shake{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
}
</style>'''
HEAD='''<title>Rumo à Posse</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;600&display=swap">
'''
s=HEAD+CSS+s[j:]
# ---------- nav ----------
ICON={'painel':'<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
'questoes':'<ellipse cx="6" cy="6" rx="3" ry="2"/><ellipse cx="6" cy="12" rx="3" ry="2"/><ellipse cx="6" cy="18" rx="3" ry="2"/><path d="M12 6h9M12 12h9M12 18h9"/>',
'simulado':'<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>',
'revisao':'<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
'flashcards':'<rect x="3" y="6" width="14" height="14" rx="2"/><path d="M7 3h12a2 2 0 0 1 2 2v12"/>',
'estatisticas':'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
'plano':'<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
'concursos':'<path d="M3 21h18M5 21V10M19 21V10M9 21v-7M15 21v-7M2 10l10-6 10 6z"/>',
'bancas':'<path d="M12 3v18M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
'aulas':'<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M10 9l5 3-5 3z"/>'}
LBL={'painel':'Início','questoes':'Questões','simulado':'Simulados','revisao':'Revisão','flashcards':'Flashcards','estatisticas':'Desempenho','plano':'Plano','concursos':'Concursos','bancas':'Bancas','aulas':'Aulas'}
nav_i=s.index('<nav class="side"'); nav_j=s.index('</nav>')+6
links=''.join(f'\n    <a href="#{k}"><svg viewBox="0 0 24 24" aria-hidden="true">{v}</svg>{LBL[k]}'+(' <span class="k" id="navDue"></span>' if k=='revisao' else '')+'</a>' for k,v in ICON.items())
NAV=f'''<nav class="side" id="nav" aria-label="Seções">
    <div class="brand"><svg width="38" height="30" viewBox="0 0 38 30" aria-hidden="true"><ellipse cx="19" cy="15" rx="17" ry="12" fill="var(--mark)" stroke="var(--ink)" stroke-width="2.5"/><path d="M11 15l6 5 10-11" fill="none" stroke="var(--ink)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Rumo à Posse<small>questões reais, estudo de graça</small></span></div>{links}
    <div class="foot"><div id="syncState" class="sync">salvando neste navegador</div><div style="margin-top:6px">Provas e gabaritos oficiais públicos. Comentários gerados por IA, marcados como tal.</div></div>
  </nav>'''
s=s[:nav_i]+NAV+s[nav_j:]
open(p,'w').write(s); print('ok css/nav')

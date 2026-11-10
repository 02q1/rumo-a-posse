# Gera o site independente (GitHub Pages) a partir do HTML do artifact:
# troca a sincronização do Claude pelo Supabase (login por e-mail) e toca as aulas do YouTube dentro da página.
import re, sys
S='/tmp/claude-0/-home-user/478c6bdf-f475-5683-bd52-c80df6bd2f12/scratchpad/'
OUT=sys.argv[1] if len(sys.argv)>1 else S+'out/site/index.html'
URL='https://yqiwcighfohcdovhihvp.supabase.co'; KEY='sb_publishable_qN-5otd_jUA2eJWr8efzkg_q6uCBI_t'
h=open(S+'out/banca-aberta.html').read()
def rep(old,new,cnt=1):
    global h
    assert h.count(old)==cnt,(old[:60],h.count(old)); h=h.replace(old,new)
# 1) sincronização: bloco do claude.use -> Supabase
i=h.index("(async()=>{\n  try{\n    if(!window.claude||!claude.use) return;"); j=h.index("})();",i)+5
SYNC=r"""
function backupUI(){
  const foot=document.getElementById('syncState'); if(!foot||document.getElementById('bkBox')) return;
  const el=document.createElement('div'); el.id='bkBox'; el.style.cssText='margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center';
  el.innerHTML='<details><summary class="note" style="cursor:pointer">Avançado: backup em arquivo</summary><div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-top:6px"><button class="btn sm" id="bkOut">Exportar backup</button><button class="btn sm" id="bkIn">Importar backup</button><input type="file" id="bkFile" accept="application/json,.json" hidden><span class="note" id="bkMsg">Extra: guarda ou restaura o progresso em um arquivo.</span></div></details>';
  foot.parentNode.insertBefore(el,foot.nextSibling);
  const msg=t=>{document.getElementById('bkMsg').textContent=t};
  document.getElementById('bkOut').onclick=()=>{ try{
    const blob=new Blob([JSON.stringify(S)],{type:'application/json'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
    a.download='rumo-a-posse-backup-'+new Date().toISOString().slice(0,10)+'.json'; document.body.appendChild(a); a.click(); a.remove(); msg('Backup exportado.');
  }catch(e){msg('Não consegui exportar.')} };
  document.getElementById('bkIn').onclick=()=>document.getElementById('bkFile').click();
  document.getElementById('bkFile').onchange=async ev=>{ const f=ev.target.files[0]; if(!f) return; try{
    const d=JSON.parse(await f.text()); if(!d||typeof d!=='object'||Array.isArray(d)) throw 0;
    S=Object.assign(BLANK(),d); persist(); render(); msg('Backup importado.');
  }catch(e){ msg('Arquivo inválido.') } ev.target.value=''; };
}
function setSync(t){ const el=document.getElementById('syncState'); if(el) el.textContent=t;
  let p=document.getElementById('syncPill'); if(!p){ p=document.createElement('div'); p.id='syncPill'; p.style.cssText='position:fixed;right:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));font:12px system-ui,sans-serif;padding:3px 9px;border-radius:12px;background:var(--paper);color:var(--ink);border:1px solid var(--line2);opacity:.85;z-index:50;pointer-events:none'; document.body.appendChild(p); }
  p.style.pointerEvents=UID?'none':'auto'; p.style.cursor=UID?'':'pointer'; p.onclick=UID?null:()=>{const d=document.querySelector('#authBox details'); if(d){d.open=true; d.scrollIntoView({behavior:'smooth',block:'center'}); const m=document.getElementById('sbMail'); if(m) m.focus();}}; if(!UID){ p.textContent='⚠ Sem sincronização · toque para entrar'; return; } p.textContent=(/Sincronizado/.test(t)?'☁ ':/Sincroniz/.test(t)?'⟳ ':'⚠ ')+t; }
__AUTH__
setSync(''); backupUI(); new MutationObserver(()=>{ if(!document.getElementById('bkBox')) backupUI(); authUI(); }).observe(document.body,{childList:true,subtree:true});"""

SYNC=SYNC.replace('__AUTH__',open('/tmp/auth.js').read().replace('__URL__',URL).replace('__KEY__',KEY))
h=h[:i]+SYNC+h[j:]
# 2) player embutido
rep('<a class="btn pri sm" href="${ytw(a.id)}" target="_blank" rel="noopener" style="text-decoration:none">Assistir</a>',
    '<button class="btn pri sm" data-play="${a.id}">Assistir</button>')
rep("Os vídeos abrem no YouTube: a página da plataforma não permite tocar vídeo de outro site aqui dentro. ","Os vídeos tocam aqui mesmo; o título abre no YouTube. ")
rep("  document.querySelectorAll('[data-seen]').forEach(b=>b.onclick=",
"""  document.querySelectorAll('[data-play]').forEach(b=>b.onclick=()=>{ const row=b.closest('.simrow'); const nx=row.nextElementSibling; if(nx&&nx.classList.contains('ytbox')){nx.remove();b.textContent='Assistir';return} const box=document.createElement('div'); box.className='ytbox'; box.style.cssText='position:relative;width:100%;max-width:100%;aspect-ratio:16/9;margin:6px 0 12px'; box.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+encodeURIComponent(b.dataset.play)+'?rel=0" title="Aula" style="position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:8px" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>'; row.after(box); b.textContent='Fechar'; });
  document.querySelectorAll('[data-seen]').forEach(b=>b.onclick=""")
rep("O tutor IA só funciona com a página aberta no claude.ai, logado na sua conta.","O tutor IA funciona só na versão do claude.ai: <a href=\"https://claude.ai/artifact/KMMxfikPC7cV323XHVfhQE\" target=\"_blank\" rel=\"noopener\">abrir lá</a>.")
# 3) documento completo
SB_JS='<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"></script>\n'
h=('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
   '<meta name="description" content="Plataforma gratuita de estudo para concursos com questões reais, gabaritos oficiais e aulas gratuitas.">\n'
   '<style>[hidden]{display:none!important}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}</style>\n'+SB_JS+h+'\n</html>\n')
import os; os.makedirs(os.path.dirname(OUT),exist_ok=True)
open(OUT,'w').write(h); print(OUT,len(h))

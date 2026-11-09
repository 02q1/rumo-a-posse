"""Acrescenta provas novas a data/questions.json (nov/2026).

FCC 2022-2023 (TRTs): caderno em PDF digital do acervo público arquivos.qconcursos.com; gabarito tipo 1 lido na
página oficial de gabaritos da FCC (concursosfcc.com.br/concursos/<spi>/gabaritos) e ajustado com o relatório oficial
de "alteração de gabarito e atribuição de questões" (questão atribuída = anulada).
Cebraspe 2024-2025 (STM, CNJ, TRT10): caderno e gabarito definitivo do CDN oficial do Cebraspe.

Cada questão passa pelos mesmos filtros do build original: texto conferido com o PDF bruto, fora as que dependem
de imagem, fórmula, sublinhado ou texto de apoio não extraído, e fora as repetidas.
uso: python3 tools/add_sources.py   (baixa os PDFs para tools/cache/)"""
import json, os, re, subprocess, sys, collections, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'legacy'))
from verify_raw import check, norm
from classify import classify
from cleanfn import clean
CACHE = os.path.join(ROOT, 'tools', 'cache'); os.makedirs(CACHE, exist_ok=True)
DATA = os.path.join(ROOT, 'data', 'questions.json')
D = json.load(open(DATA, encoding='utf-8'))
srcs, texts, qs = D['sources'], D['texts'], D['questions']
excl = collections.Counter(D.get('report', {}).get('excluidas', {}))

def get(url, name):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        open(p, 'wb').write(urllib.request.urlopen(req, timeout=60).read())
    return p

IMG = re.compile(r'gráfico|figura|imagem|ilustraç|charge|esquema|diagrama|(quadro|tabela)\s+(a seguir|abaixo|acima|seguinte|apresentad)|fluxograma|cartograma|mapa a seguir|histograma|boxplot|diagrama de', re.I)
FMT = re.compile(r'sublinhad|destacad|em negrito|em itálico|grifad', re.I)
NEEDTXT = re.compile(r'\b(o texto|do texto|no texto|ao texto|texto [IV]+|trecho|texto 1|texto 2)\b', re.I)
SYM = {'': '×', '': '−', '': '+', '': '=', '': '÷', '': '≤', '': '≥', '': '±', '': '°', '': '•'}
seen = {norm(q['stem'])[:160] for q in qs}
added = collections.Counter()
def drop(why): excl[why] += 1

def remove_src(sid):
    global qs
    D['questions'] = qs = [q for q in qs if q['src'] != sid]

# ------------------------------------------------------------------ FCC
QC = 'https://arquivos.qconcursos.com/prova/arquivo_prova/'
FCCS = 'https://www.concursosfcc.com.br/concursos/'
FCCJ = 'Anulada pela FCC após recursos (questão atribuída a todos os candidatos, conforme relatório oficial da FCC).'
FCC = [
 # sid, id qconcursos, slug, órgão, órgão curto, ano, cargo, tipo, spi FCC, relatório, gabarito tipo 1, anuladas
 ('fcc_trt4_22_aa', 88706, 'fcc-2022-trt-4-regiao-rs-analista-judiciario-area-administrativa', 'TRT4 (Tribunal Regional do Trabalho da 4ª Região – RS)', 'TRT4', 2022,
  'Analista Judiciário – Área Administrativa (caderno A02, tipo 1)', 'aj_adm', 'trt4r122', 'relatorio_atribuicao_e_alteracao_de_gabarito__2_.pdf',
  'ACBCBEADDABEEABCDAEBCDBAECBDEACEECDAACDCAEAACEEABDBDABDCCDBE', (1, 33)),
 ('fcc_trt18_23_aj', 92290, 'fcc-2023-trt-18-regiao-go-analista-judiciario-area-judiciaria', 'TRT18 (Tribunal Regional do Trabalho da 18ª Região – GO)', 'TRT18', 2023,
  'Analista Judiciário – Área Judiciária (caderno H08, tipo 1)', 'aj_jud', 'trt18122', 'trt18122_atribuicao_e_alteracao_gabaritos.pdf',
  'BACEDBDBACEDACEDABACEADBCADBECCADAEBCBDEEDBEDAACBCBCAEDDBECA', ()),
 ('fcc_trt9_22_aj', 91845, 'fcc-2022-trt-9-regiao-pr-analista-judiciario-area-judiciaria', 'TRT9 (Tribunal Regional do Trabalho da 9ª Região – PR)', 'TRT9', 2022,
  'Analista Judiciário – Área Judiciária (caderno A01, tipo 1)', 'aj_jud', 'trt9r122', 'atribuicao_de_questoes.pdf',
  'CEDABCDBCEBDEABAAEDCAEADECBCBDBEBDAACDEBAECDDBACCEBACEDDECAB', (44, 57)),
 ('fcc_trt14_22_aj', 89977, 'fcc-2022-trt-14-regiao-ro-e-ac-analista-judiciario-area-judiciaria', 'TRT14 (Tribunal Regional do Trabalho da 14ª Região – RO e AC)', 'TRT14', 2022,
  'Analista Judiciário – Área Judiciária (caderno B02, tipo 1)', 'aj_jud', 'trt14122', 'alteracao_de_gabaritos_atribuicao_de_questoes.pdf',
  'CADBEAEBCDEACDBECCDADAACBDEDADCBEEDCABACEDDCBDAEBABAEEBBCDBC', ()),
 ('fcc_trt22_22_aj', 89434, 'fcc-2022-trt-22-regiao-pi-analista-judiciario-area-judiciaria', 'TRT22 (Tribunal Regional do Trabalho da 22ª Região – PI)', 'TRT22', 2022,
  'Analista Judiciário – Área Judiciária (caderno I09, tipo 1)', 'aj_jud', 'trt22121', 'alteracao_e_atribuicao_de_questoes.pdf',
  'CEDABEDCCDBEABACABEDDBAECECDABEACDEBCDBACBADDBECEABDACECBDEA', (43,)),
]
TIPO_NOME = {'aj_adm': 'Analista Judiciário – Área Administrativa', 'aj_jud': 'Analista Judiciário – Área Judiciária', 'aj_cg': 'Analista Judiciário – Conhecimentos Gerais',
             'tec': 'Técnico (nível médio: tribunais e MPU)'}
for sid, qid, slug, orgao, curto, ano, cargo, tipo, spi, rel, gab, anul in FCC:
    remove_src(sid)
    pdf = get(f'{QC}{qid}/{slug}-prova.pdf', sid + '.pdf')
    pj = os.path.join(CACHE, sid + '.json')
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'parse_fcc.py'), pdf, pj, '60'], check=True, capture_output=True)
    P = json.load(open(pj)); items, tx = P['qs'], P['texts']
    G = {i + 1: c for i, c in enumerate(gab)}
    for n in anul: G[n] = None
    nota = ('Questões ' + ', '.join(map(str, anul)) + ' anuladas (atribuídas) pela FCC.') if anul else 'Nenhuma questão deste caderno foi anulada ou alterada no relatório oficial da FCC.'
    srcs[sid] = {'id': sid, 'banca': 'FCC', 'orgao': orgao, 'orgao_curto': curto, 'ano': ano, 'cargo': cargo, 'formato': 'MC', 'tipo': tipo, 'tipo_nome': TIPO_NOME[tipo],
                 'prova': f'{QC}{qid}/{slug}-prova.pdf', 'gabarito': f'{FCCS}{spi}/gabaritos/todos.html', 'ajuste': f'{FCCS}{spi}/{rel}',
                 'origem': 'Caderno copiado do acervo público de provas (arquivos.qconcursos.com). Gabarito tipo 1 conferido na página oficial de gabaritos da FCC e no relatório oficial de alteração/atribuição de questões. ' + nota}
    bad = set(check(pdf, items))
    for it in items:
        n = it['n']; stem = ''.join(SYM.get(c, c) for c in it['stem']); opts = {k: ''.join(SYM.get(c, c) for c in v) for k, v in it['opts'].items()}
        tid = it.get('text') if tx.get(it.get('text') or '', '') else None
        whole = stem + ' ' + ' '.join(opts.values())
        if re.search(r'[\x00-\x08\x0b-\x1f-]', whole) or any(not re.search(r'[0-9A-Za-zÀ-ú]', o) for o in opts.values()): drop('fórmula com símbolos ilegíveis no PDF'); continue
        if len(opts) != 5: drop('alternativas cortadas na extração do PDF'); continue
        if n in bad: drop('texto não conferiu com o PDF (layout com caixa/fórmula)'); continue
        if IMG.search(stem) or it.get('img') or re.search(r'\b(na|nas|da|das|pela) (foto|fotos|figura|imagem|charge|tirinha)\b', stem, re.I): drop('depende de imagem/gráfico/tabela'); continue
        if FMT.search(stem): drop('depende de formatação (sublinhado/destaque)'); continue
        if tid and (IMG.search(tx[tid]) or FMT.search(tx[tid])): drop('texto de apoio com imagem ou destaque'); continue
        if not tid and NEEDTXT.search(stem) and len(stem) < 400: drop('depende de texto de apoio não extraído'); continue
        k = norm(stem)[:160]
        if k in seen: drop('repetida em outro caderno'); continue
        seen.add(k)
        st = re.sub(r'(?<![.:?!”])\n(?!\(|“|[IVX]+\s)', ' ', clean(stem))
        q = {'id': f'{sid}-{n}', 'src': sid, 'n': n, 'fmt': 'MC', 'disc': classify(whole, it.get('sec')), 'auto': True, 'tema': it.get('sec') or '',
             'stem': st, 'opts': [clean(opts[x]) for x in 'ABCDE'], 'ans': G[n], 'anulada': G[n] is None, 'com': None}
        if q['anulada']: q['just'] = srcs[sid]['ajuste']
        if tid:
            q['text'] = f'{sid}-{tid}'; texts[q['text']] = tx[tid]
        qs.append(q); added[sid] += 1

# ------------------------------------------------------------------ Cebraspe (Certo/Errado)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
CEB = 'https://cdn.cebraspe.org.br/concursos/'
CE = [
 # sid, pasta, código do caderno, órgão, curto, ano, cargo, tipo
 ('stm25_cg1', 'stm_25', '072_STM_CG1_01', 'STM (Superior Tribunal Militar)', 'STM', 2025, 'Conhecimentos Gerais (analistas, inclusive Área Judiciária)', 'aj_cg'),
 ('stm25_001', 'stm_25', '072_STM_001_01', 'STM (Superior Tribunal Militar)', 'STM', 2025, 'Analista Judiciário – Área Administrativa (específicos)', 'aj_adm'),
 ('stm25_007', 'stm_25', '072_STM_007_01', 'STM (Superior Tribunal Militar)', 'STM', 2025, 'Analista Judiciário – Área Judiciária (específicos)', 'aj_jud'),
 ('trt10_24_cb1', 'trt10_24', '050_TRT10_CB1_01', 'TRT10 (Tribunal Regional do Trabalho da 10ª Região – DF e TO)', 'TRT10', 2025, 'Conhecimentos Básicos (analistas e técnicos)', 'aj_cg'),
 ('cnj24_cb2', 'cnj_24', '979_CNJ_CB2_01', 'CNJ (Conselho Nacional de Justiça)', 'CNJ', 2024, 'Conhecimentos Básicos (Analista Judiciário – Área Judiciária)', 'aj_cg'),
 ('cnj24_006', 'cnj_24', '979_CNJ_006_01', 'CNJ (Conselho Nacional de Justiça)', 'CNJ', 2024, 'Analista Judiciário – Área Judiciária (específicos)', 'aj_jud'),
]
def paras_of(c):
    c = c.split('rascunho.')[-1]; c = re.sub(r'^.*?OS ESPECÍFICOS --\s*', '', c, flags=re.S); c = re.sub(r'^.*?NTOS (GERAIS|BÁSICOS) --\s*', '', c, flags=re.S)
    return [p.strip() for p in re.split(r'\n\s*\n', c) if p.strip()]
for sid, pasta, code, orgao, curto, ano, cargo, tipo in CE:
    remove_src(sid)
    url = f'{CEB}{pasta}/arquivos/{code}.pdf'; gurl = f'{CEB}{pasta}/arquivos/Gab_Definitivo_{code}.pdf'
    pdf = get(url, code + '.pdf'); gpdf = get(gurl, 'G_' + code + '.pdf')
    pj = os.path.join(CACHE, sid + '.json')
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'parse_ce.py'), pdf, gpdf, pj], check=True, capture_output=True)
    items = json.load(open(pj))
    srcs[sid] = {'id': sid, 'banca': 'Cebraspe', 'orgao': orgao, 'orgao_curto': curto, 'ano': ano, 'cargo': cargo, 'formato': 'CE', 'tipo': tipo, 'tipo_nome': TIPO_NOME[tipo],
                 'prova': url, 'gabarito': gurl}
    RAWL = [l.strip() for l in subprocess.run(['pdftotext', '-raw', pdf, '-'], capture_output=True, text=True).stdout.split('\n')]
    bad = set(check(pdf, [{'n': i['n'], 'stem': i['text'], 'opts': {}} for i in items]))
    carry = ''; FIXCMD = {}
    for it in items:
        prev, carry = carry, ''
        n = it['n']; paras = [p.replace('', '−') for p in paras_of(it['ctx'])]; stem = it['text'].replace('', '−')
        if n in bad: drop('texto não conferiu com o PDF (layout com caixa/fórmula)'); continue
        whole = ' '.join(paras) + ' ' + stem
        if IMG.search(whole): drop('depende de imagem/gráfico/tabela'); continue
        if FMT.search(whole): drop('depende de formatação (sublinhado/destaque)'); continue
        if re.search(r'[\x00-\x08\x0b-\x1f܀-࿿-]', whole): drop('fórmula com símbolos ilegíveis no PDF'); continue
        if not re.search(r'[.?!)”"\]’0-9]\s*$', stem.strip()):
            cut = stem.strip().rfind('. ')
            if cut > 40: carry = stem.strip()[cut + 2:]; stem = stem.strip()[:cut + 1]
            else: drop('enunciado cortado na extração do PDF'); continue
        k = norm(stem)[:160]
        if k in seen: drop('repetida em outro caderno'); continue
        seen.add(k)
        cmd = re.sub(r'\s+', ' ', paras[-1]) if paras else ''; txt = None
        if cmd[:1].islower() and cmd in FIXCMD: cmd = FIXCMD[cmd]
        elif cmd[:1].islower() and prev: FIXCMD[cmd] = cmd = prev + ' ' + cmd
        if len(paras) > 1:
            body = '\n\n'.join(paras[:-1]); body = re.sub(r'\n[ \t]{4,}', '\n\n', body); body = re.sub(r'(?<!\n)\n(?!\n)', ' ', body); body = re.sub(r'[ \t]+', ' ', body).strip()
            if body[:1].islower():
                head = body[:35]
                for li, l in enumerate(RAWL):
                    if l.startswith(head) and li > 0 and RAWL[li - 1] and not RAWL[li - 1].startswith('CEBRASPE'):
                        body = RAWL[li - 1] + ' ' + body; break
                if body[:1].islower(): drop('depende de texto de apoio não extraído'); continue
            found = [kk for kk, v in texts.items() if v == body]
            if found: txt = found[0]
            else: txt = f'{sid}-t{len(texts)}'; texts[txt] = body
        q = {'id': f'{sid}-{n}', 'src': sid, 'n': n, 'fmt': 'CE', 'disc': classify(stem, None, cmd), 'auto': True, 'tema': '', 'cmd': cmd, 'text': txt,
             'stem': stem, 'ans': None if it['gab'] == 'X' else it['gab'], 'anulada': it['gab'] == 'X', 'com': None}
        if txt and tipo == 'aj_cg' and re.search(r'texto (precedente|anterior)|linguístic', cmd): q['disc'] = 'Língua Portuguesa'
        if q['anulada']: q['just'] = gurl
        qs.append(q); added[sid] += 1

D['report'] = {'excluidas': dict(excl)}
json.dump(D, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(dict(added), 'total', len(qs))

"""Amplia dl/data.json (165 questões originais) com CNU 2024, mais cargos do TRF6 e MPU 2025.
Cada questão nova: texto conferido com o PDF (verify_raw) e gabarito lido do PDF oficial definitivo."""
import json, re, sys, subprocess, collections, unicodedata
S = '/tmp/claude-0/-home-user/478c6bdf-f475-5683-bd52-c80df6bd2f12/scratchpad/'
sys.path.insert(0, S + 'tools')
from gabs import cnu, fgv
from verify_raw import check, norm
from classify import classify
from cleanfn import clean
base = json.load(open(S + 'dl/data.json'))
base['questions'] = [q for q in base['questions'] if q['src'] in ('trf6cg', 'trf6aj', 'agenersa')]
srcs = base['sources']; texts = base['texts']; qs = base['questions']
MAP = {'Administração Geral': 'Administração Geral e Pública', 'Administração de Materiais': 'Gestão de Materiais e Logística', 'AFO': 'AFO e Orçamento Público',
       'Raciocínio Lógico': 'Raciocínio Lógico e Matemática', 'Economia do Setor Público': 'Economia e Regulação', 'Regulação': 'Economia e Regulação',
       'Direitos Humanos': 'Direitos Humanos e Inclusão', 'Direitos da Pessoa com Deficiência': 'Direitos Humanos e Inclusão', 'Economia e Regulação': 'Economia e Regulação'}
for q in qs: q['disc'] = MAP.get(q['disc'], q['disc'])
seen = {norm(q['stem'])[:160] for q in qs}
excl = collections.Counter(); exlist = []
IMG = re.compile(r'gráfico|figura|imagem|ilustraç|charge|esquema|diagrama|(quadro|tabela)\s+(a seguir|abaixo|acima|seguinte|apresentad)|fluxograma|cartograma|mapa a seguir|histograma|boxplot|diagrama de', re.I)
FMT = re.compile(r'sublinhad|destacad|em negrito|em itálico|grifad', re.I)
NEEDTXT = re.compile(r'\b(o texto|do texto|no texto|ao texto|the text|paragraph|texto [IV]+|trecho|texto 1|texto 2)\b', re.I)
def drop(sid, n, why): excl[why] += 1; exlist.append((sid, n, why))
CNU = 'https://www.gov.br/gestao/pt-br/concursonacional/'
GM = CNU + 'gabaritos-finais/cpnu2024_gabaritosoficiais_todos-os-blocos-manha.pdf'
GT = CNU + 'gabaritos-finais/cpnu2024_gabaritosoficiais_todos-os-blocos-tarde.pdf'
REC = CNU + 'gabaritos-finais/cpnu2024_respostas_recursos_todos-os-blocos.pdf'
CEB = 'https://cdn.cebraspe.org.br/concursos/TRF6_24/arquivos/'
JUST = CEB + 'TRF6_24_JUSTIFICATIVAS_DE_ALTERAES_DE_GABARITO.PDF'
MPUG = 'https://conhecimento.fgv.br/sites/default/files/concursos/mpu-gabarito-definitivo.pdf'
FGVC = 'https://conhecimento.fgv.br/sites/default/files/concursos/'
EIXO7 = {1: 'Eixo 1', 2: 'Eixo 2', 3: 'Eixo 3', 4: 'Eixo 4', 5: 'Eixo 5'}
def add_mc(sid, meta, pdf, parsed, gab, tema_fn, sec_fix=None, just=None):
    srcs[sid] = dict(meta, id=sid, formato='MC')
    items = json.load(open(S + parsed)); tx = {}
    if isinstance(items, dict): tx = items['texts']; items = items['qs']
    bad = set(check(S + pdf, items))
    for it in items:
        n = it['n']; stem = it['stem']
        SYM = {'\uf0b4': '×', '\uf02d': '−', '\uf02b': '+', '\uf03d': '=', '\uf0b8': '÷', '\uf0a3': '≤', '\uf0b3': '≥', '\uf061': 'α', '\uf062': 'β', '\uf064': 'δ', '\uf065': 'ε', '\uf06c': 'λ', '\uf06d': 'μ', '\uf070': 'π', '\uf073': 'σ', '\uf071': 'θ', '\uf044': 'Δ', '\uf053': 'Σ', '\uf0b1': '±', '\uf0d6': '√', '\uf0a5': '∞', '\uf0b9': '≠', '\uf0bb': '≈', '\uf0b0': '°', '\uf0b7': '•'}
        stem = ''.join(SYM.get(c, c) for c in stem); it['opts'] = {k: ''.join(SYM.get(c, c) for c in v) for k, v in it['opts'].items()}
        if re.search(r'[\x00-\x08\x0b-\x1f\ue000-\uf8ff]', stem + ''.join(it['opts'].values())): print('ILEG', sid, n, sorted({hex(ord(c)) for c in stem + ''.join(it['opts'].values()) if re.match(r'[\x00-\x08\x0b-\x1f\ue000-\uf8ff]', c)}), file=sys.stderr); drop(sid, n, 'fórmula com símbolos ilegíveis no PDF'); continue
        if n in bad: drop(sid, n, 'texto não conferiu com o PDF (layout com caixa/fórmula)'); continue
        if IMG.search(stem): drop(sid, n, 'depende de imagem/gráfico/tabela'); continue
        if FMT.search(stem): drop(sid, n, 'depende de formatação (sublinhado/destaque)'); continue
        if it.get('img'): drop(sid, n, 'depende de imagem/gráfico/tabela'); continue
        if re.search(r'\b(na|nas|da|das|pela) (foto|fotos|figura|imagem|charge|tirinha)\b|evidenciad[oa]s\s+n[ao]s?\s+fotos?', stem, re.I): drop(sid, n, 'depende de imagem/gráfico/tabela'); continue
        if any(not re.search(r'[0-9A-Za-zÀ-ú]', o) for o in it['opts'].values()): drop(sid, n, 'fórmula com símbolos ilegíveis no PDF'); continue
        if IMG.search(tx.get(it.get('text'), '')) or FMT.search(tx.get(it.get('text'), '')): drop(sid, n, 'texto de apoio com imagem ou destaque'); continue
        if not it.get('text') and NEEDTXT.search(stem) and len(stem) < 400: drop(sid, n, 'depende de texto de apoio não extraído'); continue
        if n not in gab: drop(sid, n, 'sem gabarito'); continue
        k = norm(stem)[:160]
        if k in seen: drop(sid, n, 'repetida em outro caderno'); continue
        seen.add(k)
        sec = sec_fix(n) if sec_fix else it.get('sec')
        st = re.sub(r'(?<![.:?!”])\n(?!\(|“|[IVX]+\s)', ' ', clean(stem))
        q = {'id': f'{sid}-{n}', 'src': sid, 'n': n, 'fmt': 'MC', 'disc': classify(stem + ' ' + ' '.join(it['opts'].values()), sec), 'auto': True,
             'tema': tema_fn(n, sec), 'stem': st, 'opts': [clean(it['opts'][x]) for x in 'ABCDE'],
             'ans': gab[n], 'anulada': gab[n] is None, 'com': None}
        if q['anulada'] and just: q['just'] = just
        if it.get('text'):
            q['text'] = f"{sid}-{it['text']}"; texts[q['text']] = tx[it['text']]
        qs.append(q)
# ---- CNU 2024 (Cesgranrio) ----
m7 = cnu(S + 'dl/cnu/gab_manha.pdf', r'^\s*BLOCO 7 – GESTÃO')
add_mc('cnu7m', {'banca': 'Cesgranrio', 'orgao': 'CNU 2024 (MGI) – Bloco 7', 'ano': 2024, 'cargo': 'Gestão Governamental e Adm. Pública – Conhecimentos Gerais (manhã, gabarito 1)',
       'prova': CNU + 'caderno-de-provas/manha/prova-7-gabarito-1-gestao-governamental-e-administacao-publica-manha.pdf', 'gabarito': GM},
       'dl/cnu/prova-7-gabarito-1-gestao-governamental-e-administacao-publica-manha.pdf', 'parsed/cnu_7.json', m7, lambda n, s: 'Conhecimentos Gerais (comum a todos os blocos)', just=REC)
t7 = cnu(S + 'dl/cnu/gab_tarde.pdf', r'BLOCO 7 .*TARDE – GABARITO 1')
add_mc('cnu7t', {'banca': 'Cesgranrio', 'orgao': 'CNU 2024 (MGI) – Bloco 7', 'ano': 2024, 'cargo': 'Gestão Governamental e Adm. Pública – Específicas (tarde, gabarito 1)',
       'prova': CNU + 'caderno-de-provas/tarde/prova-15-gabarito-1-gestao-governamental-e-administracao-publica-tarde.pdf', 'gabarito': GT},
       'dl/cnu/prova-15-gabarito-1-gestao-governamental-e-administracao-publica-tarde.pdf', 'parsed/cnu15.json', t7, lambda n, s: EIXO7[(n - 1) // 10 + 1], just=REC)
t6 = cnu(S + 'dl/cnu/gab_tarde.pdf', r'BLOCO 6 .*TARDE – GABARITO 1')
add_mc('cnu6t', {'banca': 'Cesgranrio', 'orgao': 'CNU 2024 (MGI) – Bloco 6', 'ano': 2024, 'cargo': 'Setores Econômicos e Regulação – Específicas (tarde, gabarito 1)',
       'prova': CNU + 'caderno-de-provas/tarde/prova-14-gabarito-1-setores-economicos-e-regulacao-tarde.pdf', 'gabarito': GT},
       'dl/cnu/prova-14-gabarito-1-setores-economicos-e-regulacao-tarde.pdf', 'parsed/cnu_14.json', t6, lambda n, s: EIXO7[(n - 1) // 10 + 1], just=REC)
# ---- MPU 2025 (FGV) ----
for code, title, cargo in [('a07', 'Analista do MPU - Direito - 1', 'Analista do MPU – Direito'), ('a17', 'Analista do MPU - Perito em Economia - 1', 'Analista do MPU – Perito em Economia'),
                           ('t01', 'Técnico do MPU - Administração - 1', 'Técnico do MPU – Administração')]:
    g = fgv(S + 'dl/mpu_fgv_gab.pdf', title)
    fix = (lambda n: 'Língua Portuguesa' if n <= 20 else None) if code == 't01' else None
    def sec_fix(n, code=code, fix=fix):
        if fix and fix(n): return fix(n)
        return next(q['sec'] for q in json.load(open(S + f'parsed/mpu_{code}.json')) if q['n'] == n)
    add_mc('mpu' + code, {'banca': 'FGV', 'orgao': 'MPU (Ministério Público da União)', 'ano': 2025, 'cargo': cargo + ' (tipo 1)',
           'prova': FGVC + {'a07': 'a07-analista-do-mpu-direitoa07', 'a17': 'a17-analista-do-mpu-perito-em-economiaa17', 't01': 't01-tecnico-do-mpu-administracaot01'}[code] + '-tipo-1.pdf', 'gabarito': MPUG},
           f'dl/fgv/{code}.pdf', f'parsed/mpu_{code}.json', g, lambda n, s: s or '', sec_fix)
# ---- TJRR 2024 (FGV) ----
TJG = FGVC + 'tjrr_gabarito_definitivo_v3.pdf'
TJJUST = 'Anulada pela FGV por decisão judicial (comunicado de anulação de questões da prova objetiva do TJRR).'
for code, title, cargo, fn in [('101', 'Analista Judiciário - Apoio à Gestão - TIPO 1', 'Analista Judiciário – Apoio à Gestão', 'cns101t01-analista-judiciario-apoio-a-gestao.pdf'),
                               ('107', 'Analista Judiciário - Direito - TIPO 1', 'Analista Judiciário – Direito (Advogado)', 'cns107t01-analista-judiciario-advogado.pdf')]:
    g = fgv(S + 'dl/fgv2/tjrr_gabarito_definitivo_v3.pdf', title)
    add_mc('tjrr' + code, {'banca': 'FGV', 'orgao': 'TJRR (Tribunal de Justiça de Roraima)', 'ano': 2024, 'cargo': cargo + ' (tipo 1)', 'prova': FGVC + fn, 'gabarito': TJG},
           'dl/fgv2/' + fn, f'parsed/tjrr_{code}.json', g, lambda n, s: s or '', just=TJJUST)
# ---- FCC (provas e gabaritos FCC copiados do acervo aberto Estude Grátis; definitivo conferido com as alterações oficiais da FCC) ----
from fcc_gabs import G as FG
EG = 'https://www.estudegratis.com.br/images/provas/'
FCCS = 'https://www.concursosfcc.com.br/concursos/'
FCCJ = 'Anulada pela FCC após recursos (questão atribuída a todos os candidatos, conforme publicação oficial da FCC).'
EGM = json.load(open(S + 'dl/eg/meta.json'))
for sid, slug, orgao, ano, cargo, aj, nota in [
    ('trf4_19_aj', 'prova-analista-judiciario-area-judiciaria-trf-4a-regiao-2019', 'TRF4 (Tribunal Regional Federal da 4ª Região)', 2019, 'Analista Judiciário – Área Judiciária (caderno 01, tipo 1)', FCCS + 'trf4r119/atribuicoes_de_gabarito.pdf', 'Questões 24, 40 e 47 anuladas pela FCC.'),
    ('trt6_18_aa', 'prova-analista-judiciario-area-administrativa-trt-6a-regiao-pe-2018', 'TRT6 (Tribunal Regional do Trabalho da 6ª Região – PE)', 2018, 'Analista Judiciário – Área Administrativa (caderno C03, tipo 1)', FCCS + 'trt6r117/atribuicoes_e_alteracao_de_gabarito.pdf', 'Sem alterações para o C03 na publicação oficial.'),
    ('trt15_18_aj', 'prova-analista-judiciario-area-judiciaria-trt-15a-regiao-sp-2018', 'TRT15 (Tribunal Regional do Trabalho da 15ª Região – Campinas)', 2018, 'Analista Judiciário – Área Judiciária (caderno 02, tipo 1)', FCCS + 'trt15117/atribuicoes_e_alteracao_de_gabarito.pdf', 'Questões 16 e 30 anuladas pela FCC.'),
    ('trt15_18_aa', 'prova-analista-judiciario-area-administrativa-trt-15a-regiao-sp-2018', 'TRT15 (Tribunal Regional do Trabalho da 15ª Região – Campinas)', 2018, 'Analista Judiciário – Área Administrativa (caderno 03, tipo 1)', FCCS + 'trt15117/atribuicoes_e_alteracao_de_gabarito.pdf', 'Gabarito da questão 17 alterado pela FCC para A.'),
    ('trt2_18_aj', 'prova-analista-judiciario-area-judiciaria-trt-2a-regiao-sp-2018', 'TRT2 (Tribunal Regional do Trabalho da 2ª Região – SP)', 2018, 'Analista Judiciário – Área Judiciária (caderno AJ01, tipo 1)', FCCS + 'trt2r118/edital_resultado_preliminar_trt2r218.pdf', 'Edital oficial de resultado: nenhuma questão do AJ01 anulada ou alterada.'),
    ('trt2_18_aa', 'prova-analista-judiciario-area-administrativa-trt-2a-regiao-sp-2018', 'TRT2 (Tribunal Regional do Trabalho da 2ª Região – SP)', 2018, 'Analista Judiciário – Área Administrativa (caderno AJ03, tipo 1)', FCCS + 'trt2r118/edital_resultado_preliminar_trt2r218.pdf', 'Edital oficial de resultado: nenhuma questão do AJ03 anulada ou alterada.')]:
    m = EGM[slug]
    add_mc('fcc_' + sid, {'banca': 'FCC', 'orgao': orgao, 'ano': ano, 'cargo': cargo, 'prova': m['prova_arquivo'], 'gabarito': m['prova_gabarito'], 'ajuste': aj,
           'origem': 'Prova e gabarito copiados do acervo aberto Estude Grátis; gabarito definitivo conferido com a publicação oficial da FCC. ' + nota,
           'antiga': ano < 2021},
           f'dl/eg/{slug}/prova.pdf', f'parsed/fcc_{sid}.json', FG[sid], lambda n, s: s or '', just=FCCJ)
# ---- TRT24 2025 (FGV, reaplicação) / TRT16 2022 / TJMS 2024 ----
ANUL = 'Anulada pela FGV no gabarito definitivo.'
T24G = FGVC + 'gabaritodefinitivo_trt24-analista.pdf'
for code, title, cargo, fn in [('103', 'Analista Judiciário - Área Administrativa - Sem Especialidade - 1', 'Analista Judiciário – Área Administrativa', 'area-administrativa-sem-especialidadecns103-tipo-1.pdf'),
                               ('101', 'Analista Judiciário - Área Judiciária – Sem Especialidade - 1', 'Analista Judiciário – Área Judiciária', 'area-judiciaria-sem-especialidadecns101-tipo-1.pdf')]:
    add_mc('trt24_' + code, {'banca': 'FGV', 'orgao': 'TRT24 (Tribunal Regional do Trabalho da 24ª Região – MS)', 'ano': 2025, 'cargo': cargo + ' (reaplicação, tipo 1)', 'prova': FGVC + fn, 'gabarito': T24G},
           'dl/fgv2/' + fn, f'parsed/trt24_{code}.json', fgv(S + 'dl/fgv2/gabaritodefinitivo_trt24-analista.pdf', title), lambda n, s: s or '', just=ANUL)
fn = 'analista_judiciario_area_administrativa_-_qualquer_areacnsm003_tipo_1.pdf'
add_mc('trt16_003', {'banca': 'FGV', 'orgao': 'TRT16 (Tribunal Regional do Trabalho da 16ª Região – MA)', 'ano': 2022, 'cargo': 'Analista Judiciário – Área Administrativa (tipo 1)', 'prova': FGVC + fn,
       'gabarito': FGVC + 'trt_-_16_2022_-_gabarito_definitivo_8913849131354864.pdf'},
       'dl/fgv2/' + fn, 'parsed/trt16_003.json', fgv(S + 'dl/fgv2/trt_-_16_2022_-_gabarito_definitivo_8913849131354864.pdf', 'Analista Judiciário - Administrativa – TIPO 1'), lambda n, s: s or '', just=ANUL)
for code, title, cargo, fn in [('af', 'Analista Judiciário - Área Fim - Tipo 1', 'Analista Judiciário – Área Fim', 'analista-judiciario-area-fimcr-01-af-tipo-1.pdf'),
                               ('am', 'Analista Judiciário - Área Meio - Tipo 1', 'Analista Judiciário – Área Meio', 'analista-judiciario-area-meiocr-02-am-tipo-1.pdf')]:
    pj = f'parsed/tjms_{code}.json'
    add_mc('tjms_' + code, {'banca': 'FGV', 'orgao': 'TJMS (Tribunal de Justiça de Mato Grosso do Sul)', 'ano': 2024, 'cargo': cargo + ' (tipo 1)', 'prova': FGVC + fn, 'gabarito': FGVC + 'tjms2024_gabarito_definitivo.pdf'},
           'dl/fgv2/' + fn, pj, fgv(S + 'dl/fgv2/tjms2024_gabarito_definitivo.pdf', title), lambda n, s: s or '',
           lambda n, pj=pj: 'Língua Portuguesa' if n <= 15 else next(q['sec'] for q in json.load(open(S + pj)) if q['n'] == n), just=ANUL)
# ---- TRF6 (Cebraspe): CG2, CG3 e cargos específicos ----
CARGOS = {'CG2': 'Conhecimentos Gerais (caderno 2, analistas de apoio especializado)', 'CG3': 'Conhecimentos Gerais (técnicos)',
          '002': 'Analista Judiciário – Análise de Dados', '006': 'Analista Judiciário – Contabilidade', '012': 'Analista Judiciário – Estatística',
          '013': 'Analista Judiciário – Governança e Gestão de TI', '023': 'Analista Judiciário – Área Judiciária', '024': 'Técnico Judiciário – Área Administrativa'}
def paras_of(c):
    c = c.split('rascunho.')[-1]; c = re.sub(r'^.*?OS ESPECÍFICOS --\s*', '', c, flags=re.S); c = re.sub(r'^.*?NTOS GERAIS --\s*', '', c, flags=re.S)
    return [p.strip() for p in re.split(r'\n\s*\n', c) if p.strip()]
for code, cargo in CARGOS.items():
    sid = 'trf6_' + code.lower(); pdf = f'dl/034_TRF6_{code}_01.pdf'
    srcs[sid] = {'id': sid, 'banca': 'Cebraspe', 'orgao': 'TRF da 6ª Região', 'ano': 2025, 'cargo': cargo, 'formato': 'CE',
                 'prova': CEB + f'034_TRF6_{code}_01.PDF', 'gabarito': CEB + f'Gab_Definitivo_034_TRF6_{code}_01.PDF'}
    items = json.load(open(S + f'parsed/trf6_{code}.json'))
    RAWL = [l.strip() for l in subprocess.run(['pdftotext', '-raw', S + pdf, '-'], capture_output=True, text=True).stdout.split('\n')]
    bad = set(check(S + pdf, [{'n': i['n'], 'stem': i['text'], 'opts': {}} for i in items]))
    carry = ''; FIXCMD = {}
    for it in items:
        prev, carry = carry, ''
        n = it['n']; paras = [p.replace('\uf02d', '−') for p in paras_of(it['ctx'])]; stem = it['text'].replace('\uf02d', '−')
        if ' cidade IBGE Uberaba' in stem: stem = stem.split(' cidade IBGE Uberaba')[0].strip()  # tabela do item seguinte que vazou
        if n in bad: drop(sid, n, 'texto não conferiu com o PDF (layout com caixa/fórmula)'); continue
        whole = ' '.join(paras) + ' ' + stem
        if IMG.search(whole): drop(sid, n, 'depende de imagem/gráfico/tabela'); continue
        if FMT.search(whole): drop(sid, n, 'depende de formatação (sublinhado/destaque)'); continue
        if re.search(r'[\x00-\x08\x0b-\x1f\u0700-\u0fff\ue000-\uf8ff]', whole): drop(sid, n, 'fórmula com símbolos ilegíveis no PDF'); continue
        if not re.search(r'[.?!)”"\]’0-9]\s*$', stem.strip()):  # final do item contaminado pelo bloco seguinte
            cut = stem.strip().rfind('. ')
            if cut > 40: carry = stem.strip()[cut + 2:]; stem = stem.strip()[:cut + 1]
            else: drop(sid, n, 'enunciado cortado na extração do PDF'); continue
        k = norm(stem)[:160]
        if k in seen: drop(sid, n, 'repetida em outro caderno'); continue
        seen.add(k)
        cmd = re.sub(r'\s+', ' ', paras[-1]) if paras else ''; txt = None
        if cmd[:1].islower() and cmd in FIXCMD: cmd = FIXCMD[cmd]
        elif cmd[:1].islower() and prev: FIXCMD[cmd] = cmd = prev + ' ' + cmd  # início do enunciado que ficou no item anterior
        if len(paras) > 1:
            body = '\n\n'.join(paras[:-1]); body = re.sub(r'\n[ \t]{4,}', '\n\n', body); body = re.sub(r'(?<!\n)\n(?!\n)', ' ', body); body = re.sub(r'[ \t]+', ' ', body).strip()
            if body[:1].islower():  # primeira linha do texto perdida na extração: recupera do PDF bruto
                head = body[:35]
                for li, l in enumerate(RAWL):
                    if l.startswith(head) and li > 0 and RAWL[li - 1] and not RAWL[li - 1].startswith('CEBRASPE'):
                        body = RAWL[li - 1] + ' ' + body; break
                if body[:1].islower(): print('AVISO texto começa truncado:', sid, n, body[:60], file=sys.stderr)
            found = [kk for kk, v in texts.items() if v == body]
            if found: txt = found[0]
            else: txt = f'{sid}-t{len(texts)}'; texts[txt] = body
        q = {'id': f'{sid}-{n}', 'src': sid, 'n': n, 'fmt': 'CE', 'disc': classify(stem, None, cmd), 'auto': True, 'tema': cargo, 'cmd': cmd, 'text': txt,
             'stem': stem, 'ans': None if it['gab'] == 'X' else it['gab'], 'anulada': it['gab'] == 'X', 'com': None}
        if txt and re.search(r'preceding text|previous text|the text', cmd, re.I): q['disc'] = 'Língua Inglesa'
        elif txt and code.startswith('CG') and re.search(r'texto (precedente|anterior)|linguístic', cmd): q['disc'] = 'Língua Portuguesa'
        if q['anulada']: q['just'] = JUST
        qs.append(q)
# tabela TABCIDADES dos cadernos TRF6 002/013 (no PDF ela fica entre dois itens; conferida no texto bruto)
texts['trf6_002-tab'] = 'Tabela TABCIDADES\n\ncidade | IBGE\n\nUberaba | 3170107\n\nUberlândia | 3170206\n\nAraguari | 3103504'
for q in qs:
    if 'TABCIDADES' in (q.get('cmd') or '') and not q.get('text'): q['text'] = 'trf6_002-tab'
for q in qs:
    if q['disc'] == 'Regimento Interno': q['disc'] = 'Regimento Interno (TRF6)' if q['src'].startswith('trf6') else 'Direito Administrativo'
# ---- Vunesp (cadernos baixados pelo Elias no PCI Concursos; gabarito definitivo conferido em publicação oficial) ----
from vun_gabs import G as VG
VSEC = [(r'portugu', 'Língua Portuguesa'), (r'matemática financeira', 'Raciocínio Lógico e Matemática'), (r'raciocínio|matemática', 'Raciocínio Lógico e Matemática'), (r'estatística', 'Estatística'),
        (r'informática', 'Tecnologia da Informação e Dados'), (r'direito constitucional', 'Direito Constitucional'), (r'direito administrativo', 'Direito Administrativo'), (r'direito tributário', 'Direito Tributário'),
        (r'contabilidade|demonstrações contábeis', 'Contabilidade'), (r'administração (financeira|orçamentária)', 'AFO e Orçamento Público'), (r'administração pública', 'Administração Geral e Pública'),
        (r'economia|sistema financeiro|avaliação econômica', 'Economia e Regulação'), (r'auditoria|controle externo', 'Controle Externo e Auditoria'), (r'obras', 'Obras e Engenharia'),
        (r'criminolog|criminalística|medicina legal|biologia|física|química', 'Ciências Forenses')]
PCI = 'https://www.pciconcursos.com.br/provas/download/'
DOETCE = 'https://doe.tce.sp.gov.br/pdf/2025/07/doe-tce-2025-07-22.pdf'
VJ = {'vun_tce001': 'Anulada no gabarito definitivo publicado no DOE-TCESP de 22/07/2025.', 'vun_tce002': 'Anulada após recursos (DOE-TCESP de 22/07/2025).',
      'vun_pcsp_perito': 'Anulada após recursos (comunicado da Academia de Polícia, PC-1/2023).', 'vun_tjsp_cont': 'Anulada no gabarito definitivo (edital do TJSP).'}
for sid, pdfn, orgao, ano, cargo, slug, gab, nota in [
    ('vun_tce001', 'tcesp-2025-auditor-ci-administracao_auditor_de_controle_interno_administracao.pdf', 'TCE-SP (Tribunal de Contas do Estado de São Paulo)', 2025, 'Auditor de Controle Externo – Administração (prova 001, versão 1)', 'auditor-de-controle-interno-administracao-tce-sp-vunesp-2025', DOETCE,
     'Gabarito definitivo publicado pelo TCE-SP no Diário Oficial Eletrônico de 22/07/2025: questões 14 e 16 anuladas. Remuneração no edital de 2025: R$ 17.743,05.'),
    ('vun_tce002', 'tcesp-2025-auditor-controle-interno_auditor_de_controle_interno.pdf', 'TCE-SP (Tribunal de Contas do Estado de São Paulo)', 2025, 'Auditor de Controle Externo (prova 002, versão 1)', 'auditor-de-controle-interno-tce-sp-vunesp-2025', 'https://doe.tce.sp.gov.br/pdf/2025/06/doe-tce-2025-06-17.pdf',
     'Gabarito oficial do DOE-TCESP de 17/06/2025, com as anulações das questões 14 e 16 publicadas no resultado dos recursos (DOE-TCESP de 22/07/2025); nenhuma resposta alterada. Remuneração no edital de 2025: R$ 17.743,05.'),
    ('vun_pcsp_perito', 'pcsp-2023-perito-criminal_perito_criminal.pdf', 'Polícia Civil de SP', 2023, 'Perito Criminal (prova preambular, versão 1)', 'perito-criminal-policia-civil-sp-vunesp-2023', PCI + 'perito-criminal-policia-civil-sp-vunesp-2023',
     'Gabarito após recursos, em comunicado oficial da Academia de Polícia: questões 25, 26, 28, 67 e 68 anuladas. Remuneração no edital PC-1/2023: a partir de R$ 12.954,40.'),
    ('vun_tjsp_cont', 'tjsp-2025-contador_contador_judiciario.pdf', 'TJ-SP (Tribunal de Justiça de São Paulo)', 2025, 'Contador Judiciário (versão 1)', 'contador-judiciario-tj-sp-vunesp-2025', PCI + 'contador-judiciario-tj-sp-vunesp-2025',
     'Gabarito definitivo em edital do TJSP: questão 47 anulada. Remuneração no edital 03/2025: R$ 9.536,23 (jul/2025), mais auxílios.')]:
    d = json.load(open(S + f'parsed/{sid}.json'))
    imgt = set(d.get('img_texts', []))
    for it in d['qs']:
        if it.get('text') in imgt: it['img'] = True
    for it in [it for it in d['qs'] if len(it['opts']) < 5]: drop(sid, it['n'], 'alternativas cortadas na extração do PDF')
    d['qs'] = [it for it in d['qs'] if len(it['opts']) == 5]
    json.dump(d, open(S + f'parsed/{sid}.ok.json', 'w'), ensure_ascii=False)
    SECOV = {'vun_pcsp_perito': [(44, 52, 'Física'), (53, 61, 'Química')], 'vun_tjsp_cont': [(49, 64, 'Contabilidade pública')]}.get(sid, [])
    SECS = {it['n']: it['sec'] for it in d['qs']}
    def vsec(n, SECOV=SECOV, SECS=SECS): return next((t for a, b, t in SECOV if a <= n <= b), SECS.get(n, ''))
    add_mc(sid, {'banca': 'Vunesp', 'orgao': orgao, 'ano': ano, 'cargo': cargo, 'prova': PCI + slug, 'gabarito': gab,
           'origem': 'Caderno copiado do PCI Concursos (cópia pública). ' + nota},
           'vun/' + pdfn, f'parsed/{sid}.ok.json', VG[sid], lambda n, s: s or '', vsec, just=VJ[sid])
    for q in qs:
        if q['src'] != sid: continue
        sc = vsec(q['n']).lower()
        for pat, dd in VSEC:
            if re.search(pat, sc): q['disc'] = dd; q['auto'] = False; break
TIPOS = [
 ('aj_adm', 'Analista Judiciário – Área Administrativa', ['trf6aj', 'fcc_trt6_18_aa', 'fcc_trt15_18_aa', 'fcc_trt2_18_aa', 'trt24_103', 'trt16_003', 'tjms_am', 'tjrr101']),
 ('aj_jud', 'Analista Judiciário – Área Judiciária', ['trf6_023', 'fcc_trf4_19_aj', 'fcc_trt15_18_aj', 'fcc_trt2_18_aj', 'trt24_101', 'tjrr107', 'tjms_af']),
 ('aj_cg', 'Analista Judiciário – Conhecimentos Gerais', ['trf6cg', 'trf6_cg2']),
 ('aj_esp', 'Analista Judiciário – Especialidades (TI, Dados, Contabilidade, Estatística)', ['trf6_002', 'trf6_006', 'trf6_012', 'trf6_013', 'vun_tjsp_cont']),
 ('tc', 'Tribunal de Contas – Auditor de Controle Externo', ['vun_tce001', 'vun_tce002']),
 ('policia', 'Polícia Civil – Perito Criminal', ['vun_pcsp_perito']),
 ('tec', 'Técnico (nível médio: tribunais e MPU)', ['trf6_024', 'trf6_cg3', 'mput01']),
 ('mpu', 'Analista do MPU', ['mpua07', 'mpua17']),
 ('cnu_gestao', 'CNU – Gestão Governamental (APO, EPPGG)', ['cnu7m', 'cnu7t']),
 ('regulacao', 'Regulação (agências e CNU Bloco 6)', ['agenersa', 'cnu6t'])]
for k, nome, ids in TIPOS:
    for i in ids: srcs[i]['tipo'] = k; srcs[i]['tipo_nome'] = nome
semtipo = [i for i in srcs if 'tipo' not in srcs[i]]
if semtipo: print('fontes sem tipo:', semtipo, file=sys.stderr)
for s_ in srcs.values():
    s_['orgao_curto'] = re.split(r' \(|,| –', s_['orgao'])[0].replace('TRF da 6ª Região', 'TRF6').replace('CNU 2024 (MGI)', 'CNU')
import glob, importlib.util
EXTRA = {}; DISC = {}; DROPS = {}
for f in sorted(glob.glob(S + 'tools/com_*.py')):
    spec = importlib.util.spec_from_file_location('m', f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); EXTRA.update(m.C)
    DISC.update(getattr(m, 'D', {})); DROPS.update(getattr(m, 'DROP', {}))
for q in list(qs):
    if q['id'] in DROPS:
        qs.remove(q); excl[DROPS[q['id']]] += 1; exlist.append((q['src'], q['id'].split('-')[-1], DROPS[q['id']]))
for q in qs:
    if q['id'] in DISC: q['disc'] = DISC[q['id']]; q['auto'] = False
for q in qs:
    if not q['com'] and q['id'] in EXTRA: q['com'] = EXTRA[q['id']]
missing = [k for k in EXTRA if k not in {q['id'] for q in qs}]
if missing: print('comentários sem questão:', missing, file=sys.stderr)
json.dump({'sources': srcs, 'texts': texts, 'questions': qs}, open(S + 'dl/data2.json', 'w'), ensure_ascii=False)
rep = {'total': len(qs), 'anuladas': sum(q['anulada'] for q in qs), 'com_comentario': sum(bool(q['com']) for q in qs),
       'por_banca': collections.Counter(srcs[q['src']]['banca'] for q in qs), 'por_fonte': collections.Counter(q['src'] for q in qs),
       'por_materia': collections.Counter(q['disc'] for q in qs).most_common(), 'excluidas': excl, 'excluidas_por_fonte': collections.Counter(s for s, _, _ in exlist)}
json.dump(rep, open(S + 'dl/report.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(rep, ensure_ascii=False, indent=1))

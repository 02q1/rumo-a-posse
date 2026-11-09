"""Parser de cadernos FCC (uma coluna, questões '12.  texto', alternativas '(A)  ...').
uso: parse_fcc.py <pdf> <out.json> <n_questoes>
Saída: {'qs': [{n, sec, stem, opts{A..E}, text}], 'texts': {id: texto}}.
Textos de apoio vêm do aviso 'Atenção: Para responder às questões de números X a Y, baseie-se no texto abaixo.'"""
import subprocess, re, json, sys
pdf, out, NQ = sys.argv[1], sys.argv[2], int(sys.argv[3])
raw = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
raw = re.sub(r'\s*Via @\w+', '', raw)  # marca d'água de cópias públicas
pages = raw.split('\f')[1:]  # pula a capa
QSTART = re.compile(r'^(\d{1,2})\.\s{2,}(\S.*)$')
OPT = re.compile(r'^\s{2,}\(([A-E])\)\s+(.*)$')
ATT = re.compile(r'^\s*Aten[çc][ãa]o:.*?quest(?:ão|ões) de n[úu]meros? (\d+)(?: (?:a|e) (\d+))?', re.I)
FOOT = re.compile(r'^\S+-\S.*\s{5,}\d+\s*$')
STOP = re.compile(r'^\s{10,}(PROVA DISCURSIVA-REDAÇÃO|ESTUDO DE CASO|REDAÇÃO|PROVA DISCURSIVA|DISCURSIVA|PROVA DE ESTUDO DE CASO|PROVA DE REDAÇÃO)\s*$', re.I)
lines = []
for p in pages:
    for l in p.split('\n'):
        if not l.strip() or 'Caderno de Prova' in l or FOOT.match(l) or re.match(r'^\s*\d+\s{5,}\S+-\S', l) or re.fullmatch(r'[\soa]+', l): continue
        lines.append(l.rstrip())
qs, texts = [], {}
sec, cur, opt, mode, tx, txr = '', None, None, None, None, None
pending_title = False
rng = {}
def close_text():
    global tx
    if tx is not None:
        k = f'T{txr[0]}'
        texts[k] = tx['title'] + '\n\n' + '\n'.join(tx['lines']) if tx['title'] else '\n'.join(tx['lines'])
        for n in range(txr[0], txr[1] + 1): rng[n] = k
    tx = None
for l in lines:
    if STOP.match(l) and len(qs) >= NQ: break
    m = ATT.match(l)
    if m:
        close_text(); a = int(m.group(1)); b = int(m.group(2) or a)
        txr = (a, b); tx = {'title': '', 'lines': []}; cur = None; mode = 'text'; continue
    mq = QSTART.match(l)
    if mq and int(mq.group(1)) == len(qs) + 1:
        close_text()
        cur = {'n': int(mq.group(1)), 'sec': sec, 'stem': mq.group(2).strip(), 'opts': {}}; qs.append(cur); opt = None; mode = 'q'; continue
    ind = len(l) - len(l.lstrip()); s = l.strip()
    if len(qs) >= NQ and opt == 'E' and ind >= 20 and (s.isupper() or re.match(r'(Instruções|Atenção|Utilize)', s)): break
    if '@' in s and ind >= 20:
        if cur is not None: cur['img'] = True
        continue
    centered = ind >= 30 and len(s) < 70 and not s.startswith('(')
    if mode == 'text':
        if centered and not tx['lines'] and not tx['title']: tx['title'] = s; continue
        tx['lines'].append(s if ind < 3 else ('§' + s if ind < 12 else s)); continue
    if centered and re.fullmatch(r'[A-ZÁÉÍÓÚ][A-Za-zÀ-ú ,\-–]{3,}(?: \d+ª? Região)?', s) and '@' not in s and not re.search(r'[.,;:?]$', s) and (cur is None or opt == 'E'):
        if s.isupper(): continue
        sec = s; cur = None; mode = None; continue
    if cur is None: continue
    mo = OPT.match(l)
    if mo and (mo.group(1) == 'A' or opt) and mo.group(1) not in cur['opts']:
        opt = mo.group(1); cur['opts'][opt] = mo.group(2).strip(); continue
    if opt: cur['opts'][opt] += ' ' + s
    else: cur['stem'] += '\n' + s
close_text()
def fixo(t):
    t = re.sub(r'\b(\d{1,3}) (salário|turno|lugar|parágrafo|colocad[oa]|grau|andar|semestre|trimestre)\b', r'\1º \2', t)
    t = re.sub(r'\b(no|o|do|ao|até o) (\d{1,3}) dia\b', r'\1 \2º dia', t)
    t = re.sub(r'(\w)-[ \n]+([a-zà-ú])', r'\1\2', t)
    t = re.sub(r'\b([Nn]) (?=\d)', r'\1º ', t)
    return re.sub(r'\((\d+)\s+(parágrafo|linha|período)', r'(\1º \2', t)
for q in qs:
    q['stem'] = fixo(q['stem']); q['opts'] = {k: fixo(v) for k, v in q['opts'].items()}
    if q['n'] in rng: q['text'] = rng[q['n']]
    q['stem'] = re.sub(r'\((\d+)\s+(parágrafo|linha|período)', r'(\1º \2', q['stem'])
    for k in q['opts']: q['opts'][k] = re.sub(r'\((\d+)\s+(parágrafo|linha|período)', r'(\1º \2', q['opts'][k])
# junta parágrafos do texto: linhas começadas por § abrem parágrafo
for k, t in texts.items():
    head, _, body = t.partition('\n\n') if '\n\n' in t else ('', '', t)
    paras = []
    for ln in body.split('\n'):
        if ln.startswith('§') or not paras: paras.append(ln.lstrip('§'))
        elif re.match(r'^\(?(Adaptado|Fonte|Disponível|[A-ZÁÉ][A-Za-zçãé]+, [A-Z])', ln) and paras[-1].rstrip().endswith(('.', '”', ')', '?', '!')): paras.append(ln)
        else: paras[-1] += ' ' + ln
    texts[k] = (head + '\n\n' if head else '') + '\n\n'.join(re.sub(r'(\w)-\s+([a-zà-ú])', r'\1\2', p.strip()) for p in paras)
json.dump({'qs': qs, 'texts': texts}, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(qs), 'questões;', len(texts), 'textos')

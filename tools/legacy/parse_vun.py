"""Parser de cadernos Vunesp (duas colunas). uso: parse_vun.py <pdf> <out.json> <n_questoes>
Lê coluna esquerda e depois direita de cada página (pdfplumber), marca questão com imagem/tabela."""
import pdfplumber, re, json, sys
pdf, out, NQ = sys.argv[1], sys.argv[2], int(sys.argv[3])
lines = []  # (texto, tem_img_proxima)
with pdfplumber.open(pdf) as P:
    import collections
    REP = collections.Counter((round(im['x0']), round(im['top']), round(im['width'])) for pg in P.pages for im in pg.images)
    for pi, pg in enumerate(P.pages):
        if pi == 0: continue
        W, H = pg.width, pg.height; mid = W / 2
        c = pg.crop((0, 18, W, H - 45))
        ws = c.extract_words(keep_blank_chars=True, x_tolerance=2.5)
        rows = {}
        for w in ws: rows.setdefault(round(w['top'] / 3), []).append(w)
        imgs = [im for im in pg.images if im['height'] > 15 and REP[(round(im['x0']), round(im['top']), round(im['width']))] < 3]
        items = []  # (top, kind, side, text)
        for k in sorted(rows):
            r = sorted(rows[k], key=lambda w: w['x0']); top = r[0]['top']
            full = any(w['x0'] < mid - 8 and w['x1'] > mid + 8 for w in r)
            if full: items.append((top, 'F', 0, re.sub(r'\s+', ' ', ' '.join(w['text'] for w in r)).strip(), r[0]['x0'])); continue
            for side, grp in ((0, [w for w in r if w['x1'] <= mid + 8]), (1, [w for w in r if w['x1'] > mid + 8])):
                if grp: items.append((top, 'C', side, re.sub(r'\s+', ' ', ' '.join(w['text'] for w in grp)).strip(), grp[0]['x0']))
        for ln in pg.lines + pg.rects:
            if ln['width'] > 60 and 18 < ln['top'] < H - 45:
                imgs.append({'x0': ln['x0'], 'width': ln['width'], 'top': ln['top']})
        for im in imgs:
            cx = im['x0'] + im['width'] / 2
            kind = 'F' if im['width'] > W * 0.55 else 'C'
            items.append((im['top'], kind, 0 if cx < mid else 1, '@@IMG', 0))
        items.sort(key=lambda t: (t[0], t[2]))
        seg = []; segs = []
        for it in items:
            if seg and (it[1] == 'F') != (seg[-1][1] == 'F'): segs.append(seg); seg = []
            seg.append(it)
        if seg: segs.append(seg)
        for sg in segs:
            def mk(ts):
                xs = [t[4] for t in ts if t[3] != '@@IMG']
                m0 = min(xs) if xs else 0
                return [[('\x01' if t[4] > m0 + 6 and t[3] != '@@IMG' else '') + t[3]] for t in ts]
            if sg[0][1] == 'F': lines += mk(sg)
            else: lines += mk([t for t in sg if t[2] == 0]) + mk([t for t in sg if t[2] == 1])
L = [l[0] for l in lines if l[0].strip('\x01') and not re.search(r'pciconcursos|pcimark|Confidencial até|^[A-Z]{4}\d{4}/\d{3}', l[0]) and not re.fullmatch(r'\x01?\d{1,2}', l[0])]
import os
if os.environ.get("DBG"): print("\n".join(L))
QS = re.compile(r'^(\d{2,3})\.(?:\s+(.*))?$'); OPT = re.compile(r'^\(([A-E])\)\s*(.*)$')
LEIA = re.compile(r'^(Leia|Considere|Analise|Observe|Utilize|Os dados|As informações|O texto|Com base|Para responder|Responda)\b.*?quest(?:ão|ões)\s+(?:de\s+)?(?:n[úu]meros?\s+|n[ºo°]s?\s*)?(\d{2,3})(?:\s*(?:a|e)\s*(\d{2,3}))?', re.I)
STARTER = re.compile(r'^(Leia|Considere|Analise|Observe|Utilize|Os dados|As informações|O texto|Com base|Para responder|Responda)\b', re.I)
L2 = []
i = 0
while i < len(L):
    s_ = L[i]
    if STARTER.match(s_.lstrip('\x01')) and not LEIA.match(s_.lstrip('\x01')):
        for j in (1, 2):
            jn = ' '.join(x.lstrip('\x01') for x in L[i:i + j + 1])
            if i + j < len(L) and LEIA.match(jn) and len(jn) < 260: s_ = jn; i += j; break
        L2.append(s_); i += 1; continue
    if STARTER.match(s_) and not LEIA.match(s_):
        for j in (1, 2):
            if i + j < len(L) and LEIA.match(' '.join(L[i:i + j + 1])) and len(' '.join(L[i:i + j + 1])) < 260:
                s_ = ' '.join(L[i:i + j + 1]); i += j; break
    L2.append(s_); i += 1
L = L2
qs, texts, rng = [], {}, {}
orph = []
cur = opt = None; tx = None; txr = None; sec = ''
MONEY = re.compile(r'^(R\$\s*)?\d{1,3}(\.\d{3})+,\d{2}(\s+(R\$\s*)?\d{1,3}(\.\d{3})+,\d{2})*$')
def joinp(tx):
    paras = []
    for ln in tx:
        if ln == '@@IMG': paras.append('@@IMG'); continue
        new = ln.startswith('§') or not paras or ln.startswith(('•', '(', '*')) or paras[-1].rstrip().endswith(':') and ln[:1].isupper()
        ln = ln.lstrip('§')
        if new: paras.append(ln)
        else: paras[-1] = (paras[-1][:-1] + ln) if re.search(r'[a-zà-ú]-$', paras[-1]) and ln[:1].islower() else paras[-1] + ' ' + ln
    return '\n\n'.join(p.strip() for p in paras)
def close():
    global tx
    if tx is not None and txr:
        k = f'T{txr[0]}'; texts[k] = joinp(tx)
        for n in range(txr[0], txr[1] + 1): rng[n] = k
    tx = None
RASC = re.compile(r'\s*R\s*A\s*S\s*C\s*U\s*N\s*H\s*O\s*$', re.I)
L = [x for x in (RASC.sub('', y) if not RASC.fullmatch(y.lstrip('\x01')) else '' for y in L) if x.strip('\x01').strip()]
for i, s in enumerate(L):
    ind = s.startswith('\x01'); s = s.lstrip('\x01')
    nxt = next((x.lstrip('\x01') for x in L[i + 1:i + 4] if x != '@@IMG'), '')
    if s == '@@IMG':
        if cur is not None and tx is None: cur['img'] = True
        elif tx is not None: tx.append('@@IMG')
        continue
    m = LEIA.match(s)
    if m and len(s) < 260:
        close(); a = int(m.group(2)); b = int(m.group(3) or a); txr = (a, b); tx = ['§' + s] if len(s[m.end():].strip(' :.,')) > 3 else []; cur = None; opt = None; continue
    mq = QS.match(s)
    if mq and 1 <= int(mq.group(1)) <= NQ and int(mq.group(1)) not in {q['n'] for q in qs} and abs(int(mq.group(1)) - (qs[-1]['n'] if qs else 0)) <= 3:
        close(); st = mq.group(2) or ''
        if orph: st = ' '.join(orph) + ('\n' + st if st else '')
        orph.clear(); cur = {'n': int(mq.group(1)), 'sec': sec, 'stem': st, 'opts': {}}; qs.append(cur); opt = None; continue
    head = len(s) < 60 and not s.endswith(('.', ':', ',', ';', '?')) and not s.startswith(('(', '•')) and re.match(r'[A-Za-zÀ-ú]', s) and (QS.match(nxt) or STARTER.match(nxt)) and not re.search(r'\d', s)
    if tx is not None and not tx and len(s) < 90 and not s.endswith(('.', ',', ';')): tx.append('§' + s); continue
    if head and tx is None and (cur is None or len(cur['opts']) == 5):
        sec = s.lower().capitalize(); orph.clear(); cur = None; continue
    if tx is not None: tx.append(('§' if ind else '') + s); continue
    if cur is None: orph.append(s); continue
    mo = OPT.match(s)
    if mo and mo.group(1) == 'ABCDE'[len(cur['opts'])] if len(cur['opts']) < 5 else False:
        opt = mo.group(1); cur['opts'][opt] = mo.group(2); continue
    if opt: cur['opts'][opt] += ' ' + s
    else: cur['stem'] += '\n' + s
close()
qs.sort(key=lambda q: q['n'])
def fix(t): return re.sub(r'(\w)-\s+([a-zà-ú])', r'\1\2', re.sub(r'\b(\d)(o|a)\b(?= (parágrafo|Guerra|grau|lugar|andar))', r'\1º', t))
for q in qs:
    q['stem'] = fix(q['stem']); q['opts'] = {k: fix(v) for k, v in q['opts'].items()}
    if q['n'] in rng: q['text'] = rng[q['n']]
for q in qs:
    if any(MONEY.match(x.strip()) for x in q['stem'].split('\n')): q['img'] = True
for k in list(texts):
    if any(MONEY.match(x.strip()) for x in texts[k].split('\n')): texts[k] += '@@IMG'
    if re.search(r'@@IMG', texts[k]): texts[k + '_img'] = '1'
    texts[k] = texts[k].replace('@@IMG', '').strip()
for k in []:
    if '@@IMG' in texts[k]: texts[k] = texts[k].replace('@@IMG', ''); texts[k + '_img'] = '1'
json.dump({'qs': qs, 'texts': {k: v for k, v in texts.items() if not k.endswith('_img')}, 'img_texts': [k[:-4] for k in texts if k.endswith('_img')]}, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(qs), 'questões;', len(texts), 'textos;', sum(len(q['opts']) == 5 for q in qs), 'com 5 opções;', sum(bool(q.get('img')) for q in qs), 'com imagem')

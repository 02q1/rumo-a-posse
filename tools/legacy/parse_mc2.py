"""Parser genérico de cadernos de múltipla escolha em 2 colunas (CNU/Cesgranrio, FGV).
uso: parse_mc2.py <pdf> <out.json> <primeira_pag> [regex_filtro_extra]
Saída: lista {n, sec, stem, opts{A..E}}  (gabarito é aplicado depois, a partir do PDF oficial)."""
import subprocess, re, json, sys
pdf, out, first = sys.argv[1], sys.argv[2], int(sys.argv[3])
extra = sys.argv[4] if len(sys.argv) > 4 else None
info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
w, h = [float(x) for x in re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', info).groups()]
FILT = re.compile(r'CONCURSO P[ÚU]BLICO|NACIONAL UNIFICADO|^\s*PROVA \d+|BLOCO \d+ ?- ?(TARDE|MANH)|^\s*E ADMINISTRA|^\s*\d{1,2}\s*$|RASCUNHO|^\s*[A-ZÇ]{1,3}\s*$|^\s*O P[ÚU]BLICO|^\s*UNIFICADO|^\s*NACIONAL U')
EXF = re.compile(extra) if extra else None
lines = []
for p in range(first, pages + 1):
    for x0 in (0, w / 2):
        t = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), '-x', str(int(x0)), '-y', '0', '-W', str(int(w / 2)), '-H', str(int(h)), pdf, '-'], capture_output=True, text=True).stdout
        for l in t.split('\n'):
            if not l.strip(): continue
            s = l.rstrip()
            if re.fullmatch(r'\s*\d{1,3}\s*', s): lines.append(('NUM', int(s), 0)); continue
            if FILT.search(s) or (EXF and EXF.search(s)): continue
            ind = len(s) - len(s.lstrip())
            lines.append(('L', s.strip(), ind))
qs = []; cur = None; sec = ''; last = 0; opt = None; prevhdr = False; oind = 0
for kind, v, ind in lines:
    if kind == 'NUM':
        if v == last + 1:
            cur = {'n': v, 'sec': sec, 'stem': '', 'opts': {}}; qs.append(cur); last = v; opt = None
        continue
    titlelike = len(v) < 50 and not re.search(r'[.:;?,”"]$', v) and re.match(r'^[A-ZÁÉÍÓÚ]', v) and not v.startswith('(')
    if titlelike and (cur is None or opt == 'X' or (opt == 'E' and ind < oind + 2)):
        sec = (sec + ' ' + v) if prevhdr and sec.endswith(' e') else v; prevhdr = True; opt = 'X' if cur else opt; continue
    prevhdr = False
    if cur is None: continue
    mo = re.match(r'^\(([A-E])\)\s*(.*)$', v)
    if mo and (mo.group(1) == 'A' or opt):
        opt = mo.group(1); cur['opts'][opt] = mo.group(2); oind = ind; ecount = 0; continue
    if opt:
        if opt == 'E':
            ecount += 1
            if not (oind + 2 <= ind <= oind + 6) or ecount > 4: opt = 'X'
        if opt == 'X': continue
        if False:
            # texto após a opção E sem recuo: provavelmente lixo; anexa só se for continuação curta
            continue
        cur['opts'][opt] += '\n' + v
    else:
        cur['stem'] += '\n' + v
def dehy(s):
    s = re.sub(r'(\w)-\n(\w)', r'\1\2', s.strip()); s = s.replace('- -', '-')
    s = re.sub(r'(\s[A-Z]){1,4}\s*$', '', s)
    return s
for q in qs:
    q['stem'] = dehy(q['stem']); q['opts'] = {k: re.sub(r'\s*\n\s*', ' ', dehy(v)) for k, v in q['opts'].items()}
json.dump(qs, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(qs), 'questões;', sum(len(q['opts']) != 5 for q in qs), 'com opções incompletas')

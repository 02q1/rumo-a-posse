"""Leitura dos gabaritos oficiais definitivos (PDF) — CNU (Cesgranrio) e FGV (tabelas número/letra)."""
import subprocess, re
def txt(pdf): return subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
def cnu(pdf, header_regex, gab='1'):
    """Retorna {n: letra ou None (anulada)} para o bloco/gabarito pedido. O título pode ocupar 1 ou 2 linhas."""
    lines = txt(pdf).split('\n'); out = {}; on = False
    for k, l in enumerate(lines):
        if not on:
            if re.search(header_regex, l):
                h = l if 'GABARITO' in l else l + ' ' + (lines[k + 1] if k + 1 < len(lines) else '')
                if re.search(r'GABARITO ' + gab + r'\b', h): on = True; skip = 'GABARITO' not in l
            continue
        if skip: skip = False; continue
        if re.search(r'BLOCO \d|GABARITO \d', l): break
        for n, a in re.findall(r'(\d+)\s*-\s*(Anulada|[A-E])\b', l):
            out[int(n)] = None if a == 'Anulada' else a
    return out
def fgv(pdf, title):
    lines = [l for l in txt(pdf).split('\n') if l.strip()]; out = {}
    i = next(k for k, l in enumerate(lines) if l.strip() == title)
    k = i + 1
    while k + 1 < len(lines) and re.fullmatch(r'[\d\s]+', lines[k].strip()):
        nums = lines[k].split(); ans = lines[k + 1].split()
        assert len(nums) == len(ans), (title, nums, ans)
        for n, a in zip(nums, ans): out[int(n)] = None if a == '*' else a
        k += 2
    return out
if __name__ == '__main__':
    D = 'dl/'
    print(cnu(D + 'cnu/gab_tarde.pdf', r'BLOCO 7 .*TARDE – GABARITO 1'))
    m = cnu(D + 'cnu/gab_manha.pdf', r'^\s*BLOCO 7 – GESTÃO'); print(len(m))
    print(len(cnu(D + 'cnu/gab_tarde.pdf', r'BLOCO 6 .*TARDE – GABARITO 1')))
    for t in ['Analista do MPU - Direito - 1', 'Analista do MPU - Perito em Economia - 1', 'Técnico do MPU - Administração - 1']:
        g = fgv(D + 'mpu_fgv_gab.pdf', t); print(t, len(g), [k for k, v in g.items() if v is None])

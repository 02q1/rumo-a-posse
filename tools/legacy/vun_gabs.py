"""Gabaritos Vunesp (versão 1). Fontes oficiais: DOE-TCESP 17/06/2025 (preliminar) e 22/07/2025 (definitivo/recursos);
comunicado da Academia de Polícia (PCSP, pós-recursos); edital do TJSP (definitivo, Contador)."""
import re
V = '/tmp/claude-0/-home-user/478c6bdf-f475-5683-bd52-c80df6bd2f12/scratchpad/vun/'
def block(path, start_pat, nq, skip=0):
    L = open(path, encoding='utf-8', errors='replace').read().splitlines()
    idx = [i for i, l in enumerate(L) if re.search(start_pat, l)][skip]
    g = {}
    for l in L[idx + 1:]:
        for n, a in re.findall(r'(\d{1,3})\s*-\s*([A-EN])\b', l):
            n = int(n)
            if n == len(g) + 1: g[n] = None if a == 'N' else a
        if len(g) >= nq: break
    assert len(g) == nq, (path, len(g))
    return g
def first_after(path, anchor, pat, nq):
    L = open(path, encoding='utf-8', errors='replace').read().splitlines()
    a = [i for i, l in enumerate(L) if re.search(anchor, l)][0]
    b = [i for i in range(a, len(L)) if re.search(pat, L[i])][0]
    tmp = V + 'off/_tmp.txt'; open(tmp, 'w').write('\n'.join(L[b:]))
    return block(tmp, pat, nq)
G = {}
G['vun_tjsp_cont'] = block(V + 'txt/tjsp-2025-contador_gabarito_definitivo.txt', r'VERSÃO 1', 80)
G['vun_pcsp_perito'] = block(V + 'txt/pcsp-2023-perito-criminal_gabarito (9).txt', r'VERSÃO 1', 80)
G['vun_tce001'] = first_after(V + 'off/d22.txt', r'Gabarito definitivo após a análise', r'Versão 1', 80)
pre002 = first_after(V + 'off/t2.txt', r'002\. Prova Objetiva', r'Versão 1', 80)
# DOE-TCESP 22/07/2025, item 2: recursos contra a prova 002 deferidos -> anuladas 14 e 16 (versão 1); nenhuma alteração de resposta
G['vun_tce002'] = {n: (None if n in (14, 16) else a) for n, a in pre002.items()}
pre001 = first_after(V + 'off/t2.txt', r'001\. Prova Objetiva', r'Versão 1', 80)
if __name__ == '__main__':
    for k, g in G.items(): print(k, len(g), [n for n, a in g.items() if a is None])
    print('001 pre vs def:', {n: (pre001[n], G['vun_tce001'][n]) for n in pre001 if pre001[n] != G['vun_tce001'][n]})
    import subprocess
    pci = block(V + 'txt/tcesp-2025-auditor-controle-interno_gabarito (7).txt', r'Versão 1', 80, skip=0)
    print('PCI(7) primeiro bloco = 001?', pci == pre001, ' = 002?', pci == pre002)

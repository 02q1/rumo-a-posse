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

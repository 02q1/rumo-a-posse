"""Gabaritos FCC lidos (visualmente) das imagens do gabarito FCC no acervo Estude Grátis e ajustados
com as alterações/anulações oficiais publicadas pela FCC (concursosfcc.com.br). None = anulada (atribuída)."""
def g(s, anul=(), alt=None):
    s = s.replace(' ', ''); d = {i + 1: c for i, c in enumerate(s)}
    for n in anul: d[n] = None
    for n, c in (alt or {}).items(): d[n] = c
    return d
G = {
 # TRF4 2019, opção 01 AJ Judiciária, tipo 1; atribuídas 24, 40, 47 (atribuicoes_de_gabarito.pdf, trf4r119)
 'trf4_19_aj': g('CADEBCCDAB ECCAEBADCD EDBBADECDC DDBAEADBBE DBACEEDCAB', anul=(24, 40, 47)),
 # TRT6 2018, C03 AJ Administrativa, tipo 1; sem alterações para C03 (atribuicoes_e_alteracao_de_gabarito.pdf, trt6r117)
 'trt6_18_aa': g('DECABCDAEC BBCCADEEBB DACBDDEAEC DCAEEAECDA BCBEEDDBAC DABDDACBCE ABEECBDEBA'),
 # TRT15 2018, opção 02 AJ Judiciária, tipo 1; atribuídas 16 e 30 (trt15117)
 'trt15_18_aj': g('BEBDECAEAA CDBDCDECBA DBEBADBEAC EDABBCDEDC EABECABACC DDEBBDABCE', anul=(16, 30)),
 # TRT15 2018, opção 03 AJ Administrativa, tipo 1; Q17 alterada para A (trt15117)
 'trt15_18_aa': g('BBDCECABCE ADEADBCDAE ABACBACDBE DEBBDCEEAD DADCDDCAEA ACEEDBBCEB', alt={17: 'A'}),
 # TRT2 2018, AJ01 AJ Judiciária e AJ03 AJ Administrativa, tipo 1; sem atribuições/alterações para AJ01/AJ03
 # (edital_resultado_preliminar_trt2r218.pdf, item II, lista só TJ05, AJ08, AJ16, AJ06)
 'trt2_18_aj': g('CBEADAABED CDCECABEDB DCAAEDBBAC BDACADBCCE ACBEDEACDA BBCEBDECAA DBCEEADBCA'),
 'trt2_18_aa': g('CBEADAABED CDCECABEDB DCAAEDBBAC DECBDABEEC ADBEACADBE CCBDEBDAAC EDBCACADEB'),
}
for k, v in G.items(): assert len(v) in (50, 60, 70), (k, len(v))

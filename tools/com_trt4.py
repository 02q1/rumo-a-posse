"""Comentários (IA, conferidos com o gabarito oficial) para a prova FCC TRT4 2022 – AJ Adm.
Cada comentário começa com 'Gabarito X.' e o script aborta se X != ans."""
import json, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'questions.json'
SRC = 'fcc_trt4_22_aa'
C = {
11: "Gabarito B. O texto conta uma história com personagens (o homem e o peixinho), tempo ('Era uma vez', 'um dia') e sequência de ações: tipologia narrativa.",
14: "Gabarito A. 'Maria' é o interlocutor a quem o narrador se dirige, ou seja, vocativo, e por isso vem isolado por vírgula. Nas demais, a vírgula separa advérbio, oração adverbial deslocada ou interjeição.",
15: "Gabarito B. 'fora pescado' = verbo ser (mais-que-perfeito) + particípio: voz passiva analítica (o peixinho sofre a ação de pescar).",
16: "Gabarito C. Algarismo 2 na posição do andar: os 15 apartamentos do 2º andar. Nos dois últimos algarismos (01 a 15) o 2 aparece em 02 e 12, ou seja, 2 por andar × 6 andares = 12. Total: 15 + 12 = 27.",
17: "Gabarito D. 1+2+…+8 = 36, então cada caixa soma 18. Com três cartões em A, se o 1 estivesse em A os outros dois somariam 17 (impossível, máximo 8+7=15); se o 2 estivesse em A precisariam somar 16 (também impossível). Logo 1 e 2 estão em B.",
18: "Gabarito A. Chamando o número de x: x + 15 = x + x + x/2 ⇒ 15 = 1,5x ⇒ x = 10.",
19: "Gabarito E. Para usar o menor número de caixas, cada caixa deve ter o maior número possível de bombons que divida 96 e 84: MDC(96, 84) = 12. Caixas: 96/12 + 84/12 = 8 + 7 = 15.",
20: "Gabarito B. Testando 2015: Antonio (2022) erra por 7, Bruno (2027) por 12 e Carlos (2010) por 5, exatamente os erros 12, 7 e 5 em outra ordem.",
21: "Gabarito C. Lei 8.112/1990: reversão é o retorno do aposentado (art. 25); reintegração é a reinvestidura do estável quando invalidada a demissão (art. 28); recondução é o retorno do estável ao cargo anterior (art. 29).",
22: "Gabarito D. Art. 33 da Lei 8.112: a vacância decorre de exoneração, demissão, promoção, readaptação, aposentadoria, posse em outro cargo inacumulável e falecimento. Reintegração, recondução e reversão são formas de provimento.",
23: "Gabarito B. Art. 156, §1º: o presidente da comissão pode denegar pedidos impertinentes, meramente protelatórios ou de nenhum interesse. Erros: a comissão é de três servidores estáveis (art. 149); as reuniões são sigilosas (art. 150); o prazo de 60 dias é prorrogável por igual período (art. 152); o julgamento fora do prazo não gera nulidade (art. 169, §1º).",
24: "Gabarito A. Pelo Regimento Interno do TRT4, a eleição para os cargos de direção é por escrutínio secreto, em sessão ordinária do Tribunal Pleno, e os eleitos tomam posse perante os pares em sessão plenária extraordinária.",
25: "Gabarito E. No Regimento Interno do TRT4, tanto fixar o horário de funcionamento dos serviços e unidades judiciárias quanto eleger os integrantes das Comissões Temporárias são competências do Órgão Especial.",
26: "Gabarito C. Segundo o Regimento Interno do TRT4, cada Turma é composta por até quatro julgadores, dos quais apenas três participam de cada julgamento.",
27: "Gabarito B. Art. 5º, II, da LGPD: dado pessoal sensível é o que trata de origem racial ou étnica, convicção religiosa, opinião política, filiação sindical, saúde, vida sexual, dado genético ou biométrico.",
28: "Gabarito D. Art. 14, §3º, da LGPD: os dados de crianças podem ser coletados sem consentimento quando necessários para contatar os pais ou responsável, uma única vez e sem armazenamento, ou para sua proteção, e nunca podem ser repassados a terceiro sem consentimento.",
29: "Gabarito E. As sanções descritas (perda dos bens acrescidos, suspensão dos direitos políticos até 14 anos, multa equivalente ao acréscimo) são as do art. 12, I, para enriquecimento ilícito (art. 9º). Receber vantagem para facilitar alienação de bem público por preço inferior ao de mercado é hipótese do art. 9º. As demais alternativas descrevem dano ao erário (art. 10) ou atentado a princípios (art. 11).",
30: "Gabarito A. Art. 15, §2º, da Lei 14.133: o acréscimo de 10% a 30% na habilitação econômico-financeira do consórcio não se aplica a consórcios formados integralmente por ME e EPP. Erros: admite-se o somatório dos quantitativos de cada consorciado; consórcio é permitido, salvo vedação justificada; o edital pode limitar o número de consorciadas; a substituição depende de autorização expressa.",
31: "Gabarito C. Para a banca, férias remuneradas com acréscimo (o terço constitucional) e avaliação por resultados são práticas encontradas tanto na Administração direta quanto na iniciativa privada. Participação nos lucros e demissão sem justa causa não se aplicam ao servidor estatutário.",
32: "Gabarito E. Na estrutura matricial o profissional responde a duas linhas de autoridade: à chefia hierárquica da unidade e à coordenação técnica (aqui, a área de TI). É exatamente a dupla subordinação descrita.",
33: "Questão anulada pela banca.",
34: "Gabarito C. A Resolução CNJ 347/2020 lista entre as diretrizes da governança das contratações a promoção da meritocracia e da profissionalização dos agentes. As contratações compartilhadas são estimuladas, e não evitadas.",
35: "Gabarito D. Resolução CNJ 400/2021: coleta seletiva solidária é a destinação dos resíduos recicláveis às associações e cooperativas de catadores de materiais recicláveis.",
36: "Gabarito A. Decreto 1.171/1994, Seção I: toda ausência injustificada desmoraliza o serviço público e quase sempre leva à desordem nas relações humanas. Erros: o servidor decide também entre o justo e o injusto, o honesto e o desonesto; ele próprio também paga os tributos que o remuneram; a função pública integra-se à vida particular; todos têm direito à verdade.",
37: "Gabarito A. Maslow propôs a pirâmide de necessidades: fisiológicas, segurança, sociais, estima e autorrealização. A alternativa B é Herzberg, C e D são as teorias X e Y de McGregor, e E é Skinner (reforço).",
38: "Gabarito C. Liderança transacional é baseada em troca (recompensa pelo desempenho); a transformacional inspira, estimula intelectualmente e leva os liderados a superar os próprios interesses e crescer.",
39: "Gabarito D. Simon distingue decisões programadas (rotineiras, repetitivas, com solução já padronizada) de não programadas (situações novas, não estruturadas). O critério é o grau de recorrência ou ineditismo da situação.",
40: "Gabarito C. A gestão de pessoas é responsabilidade de linha (cada gestor gerencia sua equipe) e função de staff (o órgão de RH presta assessoria e consultoria). É a descentralização descrita por Chiavenato.",
41: "Gabarito A. O modelo de fluxo de pessoal mapeia entradas, saídas, promoções e transferências. É vegetativo e conservador, adequado a organizações estáveis e inadequado para empresas em expansão. A alternativa C descreve o modelo baseado na procura do produto.",
42: "Gabarito E. Lewin: descongelamento (abandono das práticas antigas), mudança (aprendizado das novas) e recongelamento (incorporação e estabilização do novo comportamento).",
43: "Gabarito A. Art. 5º, XVI, da CF: a reunião pacífica independe de autorização, mas não pode frustrar outra anteriormente convocada para o mesmo local, exigido apenas o prévio aviso. Os militantes avisaram primeiro, então a segunda manifestação não pode ocorrer ali.",
44: "Gabarito A. A idade mínima para deputado estadual é 21 anos (art. 14, §3º, VI, c) e o cargo não é privativo de brasileiro nato; exige domicílio eleitoral na circunscrição. Senador exige 35 anos; governador, 30; deputado federal exige 21 anos.",
45: "Gabarito C. Súmula Vinculante 43: é inconstitucional toda modalidade de provimento que permita ao servidor investir-se, sem concurso, em cargo que não integra a carreira em que foi investido (ex.: ascensão funcional). A e E contrariam as SV 37 e 42; B, a SV 15; D, a SV 55.",
46: "Gabarito E. Art. 114, I, da CF: compete à Justiça do Trabalho processar e julgar as ações oriundas da relação de trabalho, abrangidos os entes de direito público externo e da Administração direta e indireta. Erros: a arbitragem é facultada (§1º); a supervisão é do CSJT (art. 111-A, §2º, II); a JT julga também as ações entre sindicatos (III); o MPT ajuíza o dissídio, mas quem decide é a JT (§3º).",
47: "Gabarito E. Art. 193, §1º, da CLT: o adicional de periculosidade é de 30% sobre o salário-base, sem acréscimos de gratificações, prêmios ou participações. 30% × R$ 1.500 = R$ 450.",
48: "Gabarito A. Súmula 450 do TST: é devido o pagamento em dobro da remuneração de férias, incluído o terço, quando o empregador descumpre o prazo do art. 145 da CLT (pagamento até 2 dias antes do início). Atenção: em 2022 o STF (ADPF 501) declarou essa súmula inconstitucional; hoje a banca pode cobrar o entendimento do STF.",
49: "Gabarito B. Art. 484-A da CLT (extinção por acordo): o aviso prévio indenizado e a indenização do FGTS são devidos pela metade. Aviso: R$ 1.800 ÷ 2 = R$ 900. Multa do FGTS: 20% (metade de 40%) × R$ 2.500 = R$ 500.",
50: "Gabarito D. Art. 461, §1º, da CLT (após a Reforma de 2017): equiparação exige diferença de tempo de serviço para o mesmo empregador não superior a 4 anos e de tempo na função não superior a 2 anos.",
51: "Gabarito B. Art. 443, §3º, da CLT: no contrato intermitente a prestação de serviços não é contínua, alterna períodos de serviço e de inatividade, determinados em horas, dias ou meses. Não há garantia de jornada mínima.",
52: "Gabarito D. A estabilidade do cipeiro (art. 10, II, a, do ADCT e art. 165 da CLT) protege apenas os representantes eleitos pelos empregados, titulares e suplentes (Súmula 339 do TST). O membro indicado pelo empregador não tem estabilidade.",
53: "Gabarito A. I e III estão corretas. II erra porque a capacidade processual excepcional alcança apenas órgãos de cúpula (independentes e autônomos) na defesa de suas prerrogativas, e não qualquer órgão. IV erra porque a teoria adotada é a do órgão (imputação), e não a do mandato.",
54: "Gabarito B. STF (RE 611.874, Tema 386): é possível realizar etapa de concurso em data e horário diversos por motivo de crença religiosa, desde que haja razoabilidade, preservação da isonomia e nenhum ônus desproporcional à Administração.",
55: "Gabarito D. Art. 6º, LX, da Lei 14.133: agente de contratação é a pessoa designada entre servidores efetivos ou empregados públicos dos quadros permanentes para tomar decisões, acompanhar o trâmite da licitação, impulsionar o procedimento e executar as demais atividades até a homologação.",
56: "Gabarito C. Art. 109 da Lei 14.133: a Administração pode estabelecer vigência por prazo indeterminado nos contratos em que seja usuária de serviço público oferecido em regime de monopólio, desde que comprovada, a cada exercício, a existência de crédito orçamentário.",
57: "Gabarito C. Receitas de capital: amortização de empréstimos (27 mi) + alienação de bens imóveis (12 mi) = R$ 39 mi. Impostos, valores mobiliários (receita patrimonial) e indenizações e restituições são receitas correntes; a ARO é receita extraorçamentária.",
58: "Gabarito D. Art. 5º, I, da LRF: a LOA conterá, em anexo, demonstrativo da compatibilidade da programação dos orçamentos com os objetivos e metas do Anexo de Metas Fiscais da LDO. A avaliação de metas e a situação do RPPS são conteúdos da LDO (art. 4º).",
59: "Gabarito B. Art. 43, §1º, I, da Lei 4.320: o superávit financeiro apurado em balanço patrimonial do exercício anterior é fonte para abertura de créditos suplementares e especiais.",
60: "Gabarito E. Art. 12, §4º, da Lei 4.320: o planejamento e a execução de obras são investimentos, que pertencem à categoria econômica Despesa de Capital.",
}
STEM18 = "Sabendo-se que □ representa um número e que □ + 15 = □ + □ + (□/2), o número representado por □ é"
d = json.loads(P.read_text())
n = 0
for q in d['questions']:
    if q['src'] != SRC or q['n'] not in C: continue
    c = C[q['n']]
    if q['anulada'] or q['ans'] is None:
        assert c.startswith('Questão anulada'), q['n']
    else:
        assert c.startswith(f"Gabarito {q['ans']}."), (q['n'], q['ans'])
    if not q.get('com'):
        q['com'] = c; q['comIA'] = True; n += 1
    if q['n'] == 18: q['stem'] = STEM18
P.write_text(json.dumps(d, ensure_ascii=False, separators=(',', ':')))
print('comentários adicionados:', n)

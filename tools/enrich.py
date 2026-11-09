"""Reclassifica matérias e adiciona o assunto (campo `ass`) em data/questions.json.

Uso: python3 tools/enrich.py
- Questões com matéria automática (`auto`) passam por regras fortes (lei citada, regimento,
  resolução do CNJ) antes do classificador por palavras-chave.
- `ass` é um assunto fino dentro da matéria, usado no edital verticalizado e nos filtros.
"""
import json, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'legacy'))
from classify import classify  # noqa: E402

P = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
LEG = 'Legislação do tribunal'
MERGE = {'Regimento Interno': LEG, 'Regimento Interno do tribunal': LEG}

STRONG = [
    (r'regimento interno', LEG),
    (r'resolução (?:n[º°.o]*\s*)?\d+[./]?\d*(?:/\d{4})? do (?:conselho nacional de justiça|conselho superior da justiça do trabalho)|resolução (?:cnj|csjt)|código de conduta', LEG),
    (r'lindb|lei de introdução às normas', 'Direito Processual e Civil'),
    (r'notári|serventia|emolumento|extrajudicial|registrador|6\.015/1973|8\.935', 'Direito Notarial e Registral'),
    (r'comunicaç(?:ão|ões) oficia|redação oficial|manual de redação', 'Língua Portuguesa'),
    (r'8\.112|14\.133|8\.429|9\.784|12\.527|13\.709|lgpd|lei geral de proteção de dados|11\.416', 'Direito Administrativo'),
    (r'13\.146|pessoa com deficiência', 'Direitos Humanos e Inclusão'),
]

A = {
 'Língua Portuguesa': [
  ('Crase', r'crase|acento grave'),
  ('Pontuação', r'vírgula|pontuaç|ponto e vírgula|travess|dois-pontos|parênteses'),
  ('Concordância', r'concord|plural|singular'),
  ('Regência', r'regência|regid|preposição'),
  ('Pronomes e colocação', r'pronom|próclise|ênclise|mesóclise|colocação'),
  ('Verbos e vozes', r'tempo verbal|modo verbal|voz passiva|voz ativa|forma verbal|flexão verbal|correlação|verbo'),
  ('Conectivos e coesão', r'conectivo|conjunção|coes|referente|retoma|remete|articul'),
  ('Reescrita', r'reescrit|substituíd|substituiç|reescrev|mantendo-se|sem prejuízo|alteraç'),
  ('Redação oficial', r'comunicaç(?:ão|ões) oficia|redação oficial|ofício|manual de redação'),
  ('Semântica e vocabulário', r'sinônim|significado|vocábulo|conota|denota|figura de linguagem|metáfora|ironia'),
  ('Ortografia e acentuação', r'ortograf|acentu|grafia|hífen'),
  ('Morfossintaxe', r'sujeito|objeto direto|objeto indireto|predicad|adjunto|oração subordinada|oração coordenada|classe gramatical|advérbio|adjetivo|substantiv'),
 ],
 'Raciocínio Lógico e Matemática': [
  ('Lógica proposicional', r'proposiç|tabela-verdade|tabela verdade|equivalen|negação|condicional|bicondicional|tautolog|contradição|contingência'),
  ('Argumentação e diagramas', r'argument|premissa|silogism|todo |nenhum |algum '),
  ('Porcentagem e juros', r'porcent|%|juros|desconto|acréscimo|lucro|prejuízo'),
  ('Razão, proporção e regra de três', r'razão|proporç|regra de três|divid|partes'),
  ('Contagem e probabilidade', r'probabilidade|combinaç|permutaç|arranjo|maneiras|modos distintos|anagrama'),
  ('Sequências e padrões', r'sequência|padrão|termo|progressão'),
  ('Estatística básica', r'média|mediana|moda|desvio|variância'),
  ('Conjuntos', r'conjunto|interseç|diagrama de venn|venn'),
 ],
 'Direito Constitucional': [
  ('Controle de constitucionalidade', r'\badi\b|\badc\b|\badpf\b|controle de constitucionalidade|inconstitucional|difuso|concentrado'),
  ('Direitos e garantias fundamentais', r'art\. 5|direitos fundamentais|habeas|mandado de segurança|mandado de injunção|ação popular|direitos individuais|inviolab|sigilo|garantia'),
  ('Direitos sociais', r'direitos sociais|trabalhador|art\. 7|sindic|greve'),
  ('Nacionalidade e direitos políticos', r'nacionalidade|nato|naturaliz|direitos políticos|elegib|inelegib|partido'),
  ('Organização do Estado e competências', r'união|estados|municípios|competência|federa|distrito federal|territór'),
  ('Administração pública na CF', r'art\. 37|servidor|cargo público|estabilidade|acumula|teto'),
  ('Poder Judiciário', r'judiciário|tribunal|\bstf\b|\bstj\b|\btst\b|\bcnj\b|juiz|magistra|súmula vinculante'),
  ('Poder Legislativo e processo legislativo', r'congresso|senado|câmara|deputad|senador|processo legislativo|medida provisória|emenda|lei complementar|\bcpi\b'),
  ('Poder Executivo', r'presidente da república|ministro de estado|crime de responsabilidade'),
  ('Funções essenciais à Justiça', r'ministério público|defensoria|advocacia'),
  ('Princípios e aplicabilidade das normas', r'princípios fundamentais|eficácia|aplicabilidade|norma constitucional|preâmbulo|fundamentos'),
 ],
 'Direito Administrativo': [
  ('Licitações e contratos (Lei 14.133)', r'licita|14\.133|pregão|contrat|dispensa|inexigib|registro de preços'),
  ('Servidores (Lei 8.112)', r'8\.112|servidor|estágio probatório|licença|vencimento|remoção|redistribuiç|posse|provimento|vacância|disciplinar|penalidade|demissão|advertência|readapta|reversão|reintegra|recondu'),
  ('Improbidade administrativa', r'improbidade|8\.429|14\.230'),
  ('LAI e LGPD', r'12\.527|acesso à informação|lgpd|13\.709|dados pessoais|transparência'),
  ('Processo administrativo (Lei 9.784)', r'9\.784|processo administrativo|recurso administrativo|delega|avoca'),
  ('Atos administrativos', r'ato administrativo|atos administrativos|convalida|revoga|anula|vício|atributo|presunção|autoexecutoriedade|imperatividade'),
  ('Poderes administrativos', r'poder de polícia|poder hierárquico|poder disciplinar|poder regulamentar|abuso de poder|desvio de finalidade|excesso de poder'),
  ('Organização administrativa', r'autarquia|fundação|empresa pública|sociedade de economia mista|administração indireta|descentraliza|desconcentra|órgão público|consórcio'),
  ('Responsabilidade civil do Estado', r'responsabilidade civil|responsabilidade objetiva|indeniza|dano'),
  ('Serviços públicos e concessões', r'serviço público|serviços públicos|concess|permissão|8\.987|parceria público|11\.079'),
  ('Controle da administração', r'controle externo|tribunal de contas|controle interno|tomada de contas|controle judicial'),
  ('Terceiro setor', r'organização social|organizações sociais|oscip|13\.019|terceiro setor'),
  ('Princípios da administração', r'princípio|legalidade|impessoalidade|moralidade|publicidade|eficiência'),
 ],
 'Direito do Trabalho e Processual do Trabalho': [
  ('Recursos trabalhistas', r'recurso ordinário|recurso de revista|agravo|embargos de declaração|depósito recursal|recurso'),
  ('Execução trabalhista', r'execução|penhora|embargos à execução|liquidação'),
  ('Procedimento e audiência', r'audiência|reclamação|sumaríssimo|petição inicial|revelia|contestação|prova|sentença|conciliação|arquivamento|custas'),
  ('Competência e organização da Justiça do Trabalho', r'competência|vara do trabalho|jurisdição|juiz do trabalho'),
  ('Jornada, intervalos e férias', r'jornada|horas extras|intervalo|descanso|férias|repouso|banco de horas|teletrabalho|sobreaviso'),
  ('Remuneração e adicionais', r'salário|remuneração|gorjeta|13º|gratificação natalina|equiparação|adicional|insalubr|periculos'),
  ('Extinção do contrato e FGTS', r'rescis|dispensa|justa causa|aviso prévio|fgts|estabilidade|garantia de emprego'),
  ('Direito coletivo', r'sindic|convenção coletiva|acordo coletivo|greve|dissídio'),
  ('Contrato de trabalho e sujeitos', r'contrato de trabalho|empregad|empregador|vínculo|terceiriza|grupo econômico|sucessão|doméstic|aprendiz|estagi'),
  ('Prescrição', r'prescri|decadência'),
 ],
 'AFO e Orçamento Público': [
  ('Créditos adicionais', r'crédito adiciona|créditos adiciona|suplementar|crédito especial|extraordinário'),
  ('LRF', r'101/2000|responsabilidade fiscal|\blrf\b|despesa com pessoal|\brgf\b|\brreo\b'),
  ('Despesa pública', r'despesa|empenho|liquidação|restos a pagar|exercícios anteriores'),
  ('Receita pública', r'receita|arrecada|estágios da receita'),
  ('Princípios orçamentários', r'princípio|unidade|universalidade|anualidade|exclusividade|não afetação'),
  ('PPA, LDO e LOA', r'\bppa\b|\bldo\b|\bloa\b|plano plurianual|diretrizes orçamentárias|lei orçamentária|ciclo orçamentário'),
  ('MCASP e demonstrações', r'mcasp|balanço|demonstraç|patrimonial|variações patrimoniais|contábil'),
 ],
 'Gestão de Pessoas': [
  ('Liderança', r'lideran|líder'),
  ('Motivação', r'motiva|maslow|herzberg|expectativa'),
  ('Gestão do desempenho', r'desempenho|avaliação'),
  ('Clima e cultura organizacional', r'clima|cultura'),
  ('Gestão por competências', r'competênci'),
  ('Mudança organizacional', r'mudança|inovação|diagnóstico'),
  ('Conflitos e comportamento', r'conflit|comportamento|equipe|grupo|negociação'),
  ('Processo decisório', r'decisão|decisório'),
  ('Recrutamento, seleção e capacitação', r'recrutamento|seleção|treinamento|capacitação|desenvolvimento'),
 ],
 'Administração Geral e Pública': [
  ('Planejamento estratégico e indicadores', r'estratégi|swot|missão|visão|balanced|\bbsc\b|indicador'),
  ('Modelos de administração pública', r'patrimonialis|burocr|gerencial|nova gestão pública|governança|accountability'),
  ('Processos e qualidade', r'processo|qualidade|pdca|melhoria|desburocrat'),
  ('Gestão de projetos', r'projeto|pmbok|escopo|cronograma'),
  ('Estrutura organizacional', r'estrutura organizacional|departamentaliz|centraliza|organograma'),
  ('Controle e avaliação', r'controle|avaliação'),
 ],
 'Direito Processual e Civil': [
  ('LINDB', r'lindb|lei de introdução'),
  ('Recursos no CPC', r'recurso|apelação|agravo|embargos'),
  ('Tutelas provisórias', r'tutela'),
  ('Competência, partes e atos processuais', r'competência|citação|intimação|prazo|litisconsór|intervenção de terceiros|partes|petição inicial|sentença|prova'),
  ('Parte geral do Código Civil', r'pessoa natural|pessoa jurídica|personalidade|capacidade|domicílio|bens|negócio jurídico|prescrição|decadência'),
  ('Obrigações, contratos e responsabilidade civil', r'obrigaç|contrat|responsabilidade civil|indeniza'),
 ],
 'Legislação do tribunal': [
  ('Regimento interno', r'regimento'),
  ('Resoluções do CNJ e do CSJT', r'resolução|cnj|csjt'),
  ('Ética e conduta', r'ética|conduta'),
 ],
}


LAW = {'Direito Administrativo': [(r'8\.429|improbidade', 'Improbidade administrativa'), (r'8\.112', 'Servidores (Lei 8.112)'),
        (r'14\.133', 'Licitações e contratos (Lei 14.133)'), (r'9\.784', 'Processo administrativo (Lei 9.784)'), (r'12\.527|13\.709|lgpd', 'LAI e LGPD')],
        'AFO e Orçamento Público': [(r'101/2000|responsabilidade fiscal', 'LRF')]}


def ass_of(q):
    rules = A.get(q['disc'])
    t = ' '.join([q.get('cmd') or '', q['stem'], ' '.join(q.get('opts') or [])]).lower()
    if not rules:
        return ''
    for rx, name in LAW.get(q['disc'], []):
        if re.search(rx, t):
            return name
    best, bs = '', 0
    for name, rx in rules:
        s = len(re.findall(rx, t))
        if s > bs:
            best, bs = name, s
    if not best and q['disc'] == 'Língua Portuguesa':
        return 'Interpretação de texto'
    if not best and q['disc'] == 'Raciocínio Lógico e Matemática':
        return 'Problemas aritméticos'
    return best


def main():
    d = json.load(open(P))
    moved = 0
    for q in d['questions']:
        q['disc'] = MERGE.get(q['disc'], q['disc'])
        if q.get('auto') and not q.get('ia'):
            t = ' '.join([q.get('cmd') or '', q['stem']]).lower()
            for rx, disc in STRONG:
                if re.search(rx, t):
                    if q['disc'] != disc:
                        q['disc'] = disc; moved += 1
                    break
            else:
                if q['disc'] in ('Outros temas', 'Atualidades e Realidade Brasileira', 'Economia e Regulação') and SRC_TEMA(q):
                    nd = classify(q['stem'], q.get('tema'), q.get('cmd') or '')
                    if nd != q['disc']:
                        q['disc'] = nd; moved += 1
        q['ass'] = ass_of(q)
    json.dump(d, open(P, 'w'), ensure_ascii=False, separators=(',', ':'))
    n = sum(1 for q in d['questions'] if q['ass'])
    print('matéria corrigida:', moved, '| com assunto:', n, 'de', len(d['questions']))


def SRC_TEMA(q):
    return bool(q.get('tema'))


if __name__ == '__main__':
    main()

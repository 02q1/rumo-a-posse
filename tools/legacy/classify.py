"""Classificação automática de matéria por palavras-chave (marcada como automática no app)."""
import re
R = [
 ('Regimento Interno', r'regimento interno'),
 ('Direito do Trabalho e Processual do Trabalho', r'\bclt\b|trabalhist|empregad[oa]|empregador|reclamaç|justiça do trabalho|\btst\b|\btrt\b|aviso prévio|horas extras|jornada de trabalho|depósito recursal|vara do trabalho|contrato de trabalho|rescisão|fgts|insalubr|periculos'),
 ('Direito Tributário', r'tribut|execução fiscal|116/2003|\biss\b|icms|imposto sobre|fato gerador|lançamento tributário'),
 ('Direito Previdenciário', r'previdênci|aposentadoria|benefício previdenci'),
 ('Língua Inglesa', r'\b(the|text|paragraph|word|excerpt|which|that)\b'),
 ('Língua Portuguesa', r'pronome|vírgula|concordância|regência|crase|oração|sintátic|reescrit|sentido do texto|correção gramatical|coesão|coerência|pleonasm|sinônim|vocábulo|frase|segmento|período|tempo verbal|conjunção'),
 ('Raciocínio Lógico e Matemática', r'argument|proposiç|silogism|falácia|tabela.verdade|premissa|conclusão lógica|argumento válido|contradição|tautologia|probabilidade|permutaç|combinaç|arranjo|porcentagem|juros|progressão'),
 ('Estatística', r'estatístic|amostra|média|variância|desvio padrão|distribuição normal|regressão|hipótese nula|intervalo de confiança|estimador|correlação|mediana|quartil'),
 ('Tecnologia da Informação e Dados', r'pdpj|hibernate|java|crisp|data mart|data mining|postgres|bpmn|dados|big data|banco de dados|sql|python|algoritmo|machine learning|aprendizado de máquina|nuvem|cloud|hadoop|software|rede neural|inteligência artificial|business intelligence|data warehouse|etl|api|microsserviç|segurança da informação|criptograf|blockchain|power bi|dashboard'),
 ('Direito Constitucional', r'constituição|constitucional|emenda|supremo|stf|direitos fundamentais|poder legislativo|congresso|senado|câmara dos deputados|mandado de segurança|habeas|ação direta'),
 ('Direito Administrativo', r'impessoalidade|moralidade|princípios da administração|concurso público|homologação|consórcio|licitaç|14\.133|8\.112|9\.784|ato administrativo|administração pública direta|autarquia|servidor público|improbidade|poder de polícia|concessão|permissão de serviço|processo administrativo|contrato administrativo|responsabilidade civil do estado|agentes públicos|lei de acesso|12\.527'),
 ('Direito Processual e Civil', r'processo civil|cpc|petição|sentença|recurso|citação|competência|tutela|perícia|juiz|código civil|prescrição|contrato|obrigaç'),
 ('Direito Penal e Processual Penal', r'crime|penal|pena|inquérito|ação penal|denúncia|prisão'),
 ('Direitos Humanos e Inclusão', r'direitos humanos|deficiência|acessibilidade|discriminaç|igualdade racial|agenda 2030|onu|convenção|idoso|criança|indígena'),
 ('Ética e Integridade', r'ética|código de ética|conflito de interesses|integridade|anticorrupç|12\.846|compliance'),
 ('AFO e Orçamento Público', r'orçament|loa|ldo|ppa|crédito adicional|receita pública|despesa pública|empenho|liquidação|restos a pagar|responsabilidade fiscal|101/2000|tesouro|4\.320|programação financeira'),
 ('Contabilidade', r'mcasp|contábil|contabilidade|balanço|patrimônio líquido|ativo|passivo|depreciação|lançamento|demonstraç|dre|mensurad'),
 ('Economia e Regulação', r'firma|custo marginal|alavancagem|\bbeta\b|economia|econômic|mercado|monopólio|oligopól|elasticidade|demanda|oferta|inflação|pib|juros|câmbio|balanço de pagamentos|regulaç|agência reguladora|tarifa|falha de mercado|externalidade|assimetria'),
 ('Políticas Públicas', r'política pública|políticas públicas|agenda|implementação|avaliação de impacto|formulação|ciclo de polític|stakeholders|participação social|controle social|federalismo|descentralizaç'),
 ('Gestão de Pessoas', r'gestão de pessoas|liderança|motivação|clima organizacional|competência|capacitação|treinamento|desempenho|conflito|negociação|equipe|recrutamento|seleção|comportamento organizacional|estresse'),
 ('Gestão de Projetos e Processos', r'projeto|pmbok|cronograma|escopo|stakeholder|processo de negócio|bpm|mapeamento de processos|maturidade|gerenciamento de riscos|gestão de riscos|risco'),
 ('Administração Geral e Pública', r'planejamento estratégico|estratégi|missão|visão|swot|balanced scorecard|bsc|okr|governança|gestão pública|administração pública|nova gestão pública|burocracia|eficiência|controle|organizaç|cadeia de valor|governo digital|governo eletrônico|inovação'),
 ('Gestão de Materiais e Logística', r'estoque|almoxarifado|logística|compras|patrimônio|material|bens|inventário|curva abc|fornecedor'),
 ('Arquivologia', r'arquiv|documento|gestão documental|temporalidade|sigad|preservação digital|protocolo'),
 ('Sustentabilidade', r'sustentab|ambiental|clima|emissões|energia|matriz energética|resíduos'),
 ('Comunicação Pública', r'comunicação|mídia|publicidade|imprensa'),
 ('Atualidades e Realidade Brasileira', r'brasil|desigualdade|sus|saúde|educação|federal|redemocratização'),
]
SEC = {'Língua Portuguesa': 'Língua Portuguesa', 'Noções de Administração Pública': 'Administração Geral e Pública',
       'Noções de Direitos Humanos e Fundamentais e de Acessibilidade': 'Direitos Humanos e Inclusão', 'Legislação Institucional': 'Legislação Institucional (MPU)',
       'Noções de Sustentabilidade': 'Sustentabilidade', 'Noções de Direito Administrativo': 'Direito Administrativo',
       'Raciocínio Lógico-matemático': 'Raciocínio Lógico e Matemática', 'Raciocínio Lógico Matemático': 'Raciocínio Lógico e Matemática', 'Atualidades': 'Atualidades e Realidade Brasileira'}
SECKW = [('Raciocínio', 'Raciocínio Lógico e Matemática'), ('Matemática', 'Raciocínio Lógico e Matemática'), ('Português', 'Língua Portuguesa'), ('Língua Portuguesa', 'Língua Portuguesa'),
 ('Informática', 'Tecnologia da Informação e Dados'), ('Pessoas com Deficiência', 'Direitos Humanos e Inclusão'), ('Ética', 'Ética e Integridade'),
 ('Regimento Interno', 'Regimento Interno do tribunal'), ('Processual do Trabalho', 'Direito do Trabalho e Processual do Trabalho'), ('Direito do Trabalho', 'Direito do Trabalho e Processual do Trabalho'),
 ('Processual Penal', 'Direito Penal e Processual Penal'), ('Direito Penal', 'Direito Penal e Processual Penal'), ('Processual Civil', 'Direito Processual e Civil'), ('Direito Civil', 'Direito Processual e Civil'),
 ('Direito Constitucional', 'Direito Constitucional'), ('Direito Administrativo', 'Direito Administrativo'), ('Tributário', 'Direito Tributário'), ('Previdenciário', 'Direito Previdenciário'),
 ('Orçamento', 'AFO e Orçamento Público'), ('Gestão de Pessoas', 'Gestão de Pessoas'), ('Administração Geral', 'Administração Geral e Pública'), ('Administração Pública', 'Administração Geral e Pública'),
 ('Arquivologia', 'Arquivologia'), ('Atualidades', 'Atualidades e Realidade Brasileira')]
def classify(text, sec=None, cmd=''):
    if sec in SEC: return SEC[sec]
    for kw, d in SECKW:
        if sec and kw.lower() in sec.lower() and len(sec) < 90: return d
    if sec and sec.strip().upper() == 'LÍNGUA PORTUGUESA': return 'Língua Portuguesa'
    t = text.lower(); c = cmd.lower(); best = None; bs = 0
    for d, rx in R:
        sc = len(re.findall(rx, t)) + 3 * len(re.findall(rx, c))
        if d == 'Língua Inglesa': sc = sc if sc >= 4 else 0
        if sc > bs: best, bs = d, sc
    return best or 'Outros temas'

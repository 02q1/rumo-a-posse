
"use strict";
const DATA = window.RUMO_DATA || JSON.parse(document.getElementById('data').textContent);
const Q = DATA.questions, SRC = DATA.sources, TXT = DATA.texts;
const QBY = Object.fromEntries(Q.map(q=>[q.id,q]));
const $ = (s,el=document)=>el.querySelector(s);
const esc = s => String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const today = ()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
const addDays=(iso,n)=>{const d=new Date(iso+'T12:00:00');d.setDate(d.getDate()+n);return d.toISOString().slice(0,10)};
const DISCS = [...new Set(Q.map(q=>q.disc))];
const yt = q => 'https://www.youtube.com/results?search_query='+encodeURIComponent(q+' aula concurso');
const VIDS = {"interpretação de texto Cebraspe": [{"id": "zCLWSXM9orI", "t": "Como a CESPE/CEBRASPE cobra Português? Resolva essas 14 questões e domine a banca!", "c": "Prof. Álvaro Ferreira", "d": "1:06:20"}, {"id": "22iA3PPjr7c", "t": "INTERPRETAÇÃO de TEXTOS para CONCURSO - Nunca mais erre!", "c": "Prof. Álvaro Ferreira", "d": "45:34"}], "reescrita de frases Cebraspe": [{"id": "o7RTwzdAdbc", "t": "REESCRITURA TEXTUAL PARA PROVAS - Aula 18 - Profa. Pamba - Texto", "c": "Professora Pamba", "d": "19:17"}, {"id": "aB-hABpmp1o", "t": "REESCRITURA DE TEXTOS: não existe aula disso (e eu provo em 12 questões)", "c": "Prof. Álvaro Ferreira", "d": "1:17:55"}], "crase": [{"id": "5uMooAjtVis", "t": "CRASE - As 6 regras mais cobradas em CONCURSO (Teoria + Questões)", "c": "Prof. Álvaro Ferreira", "d": "35:59"}, {"id": "lb59rQIFqak", "t": "CRASE PARA PROVAS (CONCURSOS E VESTIBULARES) TEORIA + RESOLUÇÃO DE EXERCÍCIOS - Profa. Pamba", "c": "Professora Pamba", "d": "28:25"}], "concordância verbal": [{"id": "jdqhnVUvqOc", "t": "🔴 CONCORDÂNCIA VERBAL - Teoria e Questões para Concurso", "c": "Prof. Álvaro Ferreira", "d": "49:36"}, {"id": "IjVd1jviQrA", "t": "CONCORDÂNCIA VERBAL E NOMINAL (Gramática para Concursos) - Professora Pamba", "c": "Professora Pamba", "d": "1:01:05"}], "lógica proposicional equivalências": [{"id": "KXm8Hi-I_G0", "t": "RACIOCÍNIO LÓGICO - PROPOSIÇÕES E TABELA VERDADE - Professora Angela Matemática", "c": "Professora Angela Matemática", "d": "14:13"}, {"id": "N2YDVpAryak", "t": "PROPOSIÇÕES LÓGICAS - AULA 1", "c": "Felippe Loureiro", "d": "32:23"}], "falácias argumentação Cebraspe": [{"id": "5NPPjMh_ulo", "t": "RLM para Concursos: Aprenda o que são Argumentações Lógicas de uma forma fácil e rápida", "c": "Focus Concursos", "d": "27:25"}, {"id": "Hi4Wlt51GO4", "t": "Aprenda Argumentação Lógica com Diagramas Lógicos Passo a Passo!", "c": "Felippe Loureiro", "d": "44:31"}], "negação de proposições": [{"id": "4QK69EOKHOo", "t": "Negações Lógicas para Concursos Públicos Aula 1", "c": "Felippe Loureiro", "d": "15:17"}, {"id": "sJ607Nw8R7A", "t": "Raciocínio Lógico para Concursos - ⁠Negação Lógica", "c": "Felippe Loureiro", "d": "59:25"}], "Lei 8.112 completa": [{"id": "X1gVuOekuyM", "t": "Lei 8.112/1990 Esquematizada - Parte 1 - Prof. Herbert Almeida", "c": "Estratégia Concursos", "d": "3:05:30"}, {"id": "yKtte_WyK3w", "t": "LEI 8112/90 - Estatuto dos SERVIDORES PÚBLICOS (Resumo para Concursos - Atualizado)", "c": "Me Julga - Cíntia Brunelli", "d": "16:44"}], "Lei 9.784 processo administrativo": [{"id": "JvyuHXnHWZM", "t": "Lei 9.784-99: Processo Administrativo Federal - Prof. Herbert Almeida", "c": "Estratégia Concursos", "d": "3:49:27"}, {"id": "RDprdxE4O54", "t": "Lei 9.784/99 - Processo Administrativo Federal - Resumo para Concursos | Direito Administrativo", "c": "Me Julga - Cíntia Brunelli", "d": "9:56"}], "Lei 14.133 licitações": [{"id": "Pecf9lc-UGo", "t": "Nova Lei de Licitações e Contratos - Lei 14.133/2021: Esquematizada para concursos públicos", "c": "Estratégia Concursos", "d": "3:55:01"}, {"id": "qXe73cK0lkU", "t": "Resumo de Licitações Públicas - Lei 14133", "c": "Prof. Herbert Almeida", "d": "57:12"}], "poder de polícia STF tema 532": [{"id": "0_trvGt9wHk", "t": "Delegação do Poder de Polícia: tudo que você PRECISA saber", "c": "Estratégia Carreira Jurídica", "d": "11:50"}, {"id": "OFVGEMVP8jk", "t": "Poder de Policia (Direito Administrativo): Resumo Completo", "c": "Direito Desenhado", "d": "8:16"}], "LAI e LGPD": [{"id": "rIsXdYV_Nmw", "t": "Direito Digital: Foco na LGPD e na LAI - Melhor que Black Friday", "c": "Estratégia Concursos", "d": "3:19:45"}, {"id": "So9Lhgbq2sk", "t": "DIREITO DIGITAL e LGPD (Resumo) - LEI GERAL DE PROTEÇÃO DE DADOS PESSOAIS | Privacidade na Internet", "c": "Me Julga - Cíntia Brunelli", "d": "13:15"}], "direitos fundamentais": [{"id": "N4abkOIQ1j4", "t": "Direitos e Garantias Fundamentais (Resumo) | Direito Constitucional", "c": "Me Julga - Cíntia Brunelli", "d": "12:59"}, {"id": "4MCSM4nvZeo", "t": "Direitos e Garantias Fundamentais: Resumo em UMA AULA", "c": "Estratégia Concursos", "d": "3:46:51"}], "organização do Estado competências": [{"id": "hG3jqNmo1io", "t": "ORGANIZAÇÃO DO ESTADO (Resumo) | Direito Constitucional", "c": "Me Julga - Cíntia Brunelli", "d": "12:40"}, {"id": "SGZbPsNHwL8", "t": "REPARTIÇÃO DE COMPETÊNCIAS | Direito Constitucional", "c": "Me Julga - Cíntia Brunelli", "d": "13:36"}], "Poder Judiciário constituição": [{"id": "xSFGp-UtZ-E", "t": "PODER JUDICIÁRIO na Constituição Federal | Direito Constitucional", "c": "Me Julga - Cíntia Brunelli", "d": "14:19"}, {"id": "hjlVFk0OgbE", "t": "Poder Judiciário na Constituição - Prof. Ricardo Vale", "c": "Estratégia Concursos", "d": "3:08:46"}], "eficácia das normas constitucionais": [{"id": "kaLV24DI6ls", "t": "Eficácia e Aplicabilidade das NORMAS CONSTITUCIONAIS - Normas Plenas, Contidas e Limitadas", "c": "Me Julga - Cíntia Brunelli", "d": "14:33"}, {"id": "OLzMo6vDQPU", "t": "Normas de eficácia PLENA, CONTIDA E LIMITADA - Dicas simples para aprender!", "c": "Me Julga - Cíntia Brunelli", "d": "8:10"}], "Lei de improbidade 14.230 alterações": [{"id": "LkpK6hCClcE", "t": "Resumo de Improbidade Administrativa", "c": "Prof. Herbert Almeida", "d": "29:31"}, {"id": "TnywC2Rb54c", "t": "Lei 8.429/92 (e L14230): Improbidade Administrativa - a Lei que SEMPRE CAI em concurso", "c": "Estratégia Concursos", "d": "2:34:27"}], "Lei anticorrupção 12.846": [{"id": "VEOAXMi4e5I", "t": "LEI ANTICORRUPÇÃO (Lei 12.846/13) - Resumo para Concursos", "c": "Me Julga - Cíntia Brunelli", "d": "11:02"}, {"id": "nOD1s5fc9Zs", "t": "Aula 10: Legislação Anticorrupção: Lei nº 12.846/2013 e Decreto nº 8.420/2015 - Concurso Caixa 2024", "c": "Retorno Interno - Com Renan Duarte", "d": "31:22"}], "Código de ética Decreto 1.171": [{"id": "e6Xy82Q7p8M", "t": "Questões de Ética no Serviço Público para Concursos - Decreto 1171/94", "c": "Nova Concursos", "d": "55:17"}, {"id": "7rNy8ua-JLY", "t": "Aula de Ética no Serviço Público professor Tiago Vidal | Concurso PRF Agente Administrativo-AlfaCon", "c": "AlfaCon", "d": "26:21"}], "AFO orçamento público PPA LDO LOA": [{"id": "qypPax2d4ug", "t": "ORÇAMENTO PÚBLICO  - Resumo | PPA, LDO e LOA | Lei Orçamentária | Responsabilidade Fiscal", "c": "Me Julga - Cíntia Brunelli", "d": "10:23"}, {"id": "Qdloj5WdLxI", "t": "AFO para Concursos: PPA, LDO e LOA - Resumo Completo - Semana do Consumidor Concurseiro", "c": "Estratégia Concursos", "d": "3:22:37"}], "princípios orçamentários": [{"id": "BkMXYAYwu3M", "t": "AFO sem Mistérios - Princípios Orçamentários | Com Anderson Ferreira", "c": "Gran Cursos Online", "d": "1:35:05"}, {"id": "mEs3_UseET4", "t": "ADMINISTRAÇÃO FINANCEIRA E ORÇAMENTÁRIA PARA CONCURSOS 2022 - AULA 1/3 - AlfaCon", "c": "AlfaCon", "d": "1:01:00"}], "créditos adicionais": [{"id": "v9JAa_oUWfQ", "t": "AFO sem Mistérios - Créditos Adicionais | Com Anderson Ferreira", "c": "Gran Cursos Online", "d": "55:18"}, {"id": "l_6y35NLLDc", "t": "Créditos Ordinários e Adicionais (Suplementar, Especial e Extraordinário) (Aula 25)", "c": "Diego Jacques / Finanças & Orçamento Público", "d": "36:09"}], "cultura organizacional Schein": [{"id": "Ki9Ez-xiy0E", "t": "Cultura e Clima Organizacional  - Aula Completa - Prof. Rodrigo Rennó", "c": "Rodrigo Rennó", "d": "50:47"}, {"id": "H9_AEB9SgMU", "t": "13.03. Aula de Cultura Organizacional (Administração)", "c": "TecConcursos", "d": "37:11"}], "processo decisório Simon": [{"id": "aMvX3vXQZbE", "t": "Processo Decisório / Tomada de Decisão - Aula Completa - Rodrigo Rennó", "c": "Rodrigo Rennó", "d": "1:02:57"}, {"id": "f_KVbdt3Ov4", "t": "15. Aula do Processo Decisório (Administração) - Parte 1", "c": "TecConcursos", "d": "30:52"}], "gestão de projetos PMBOK": [{"id": "U1Sweidt0Vs", "t": "Gestão de projetos - Aula completa|Prof. Marcelo Soares", "c": "Prof. Marcelo Soares", "d": "1:52:39"}, {"id": "tYXGfChVV28", "t": "Ricardo Vargas Explica o PMBOK® Guide 7a Edição Publicado pelo PMI", "c": "Ricardo Vargas", "d": "1:44:49"}], "administração de materiais curva ABC": [{"id": "ZPxibqZF8Ao", "t": "Classificação de Materiais - Administração de Recursos Materiais", "c": "Rodrigo Rennó", "d": "1:21:12"}, {"id": "CiFwih4XHNU", "t": "Gestão de ESTOQUE usando CURVA ABC (passo a passo)", "c": "Ser Logístico", "d": "16:02"}], "gestão de estoques ponto de pedido": [{"id": "dHoegcRIJfc", "t": "03.01. Aula de Noções de Gestão de Estoques (Administração de Recursos Materiais)", "c": "TecConcursos", "d": "26:59"}, {"id": "qBz4RoIn7Aw", "t": "Administração de Recursos Materiais - Introdução - Prof. Rodrigo Rennó", "c": "Rodrigo Rennó", "d": "1:23:36"}], "funções do Estado Musgrave": [{"id": "KiOoNsoAbA8", "t": "Aula 01.2 - Funções Econômicas do Estado (Alocativa, Distributiva, Estabilizadora)", "c": "Diego Jacques / Finanças & Orçamento Público", "d": "11:24"}, {"id": "9_VIsCcDoT0", "t": "Funções do Governo em Mapa Mental - Alocativa, Distributiva, Estabilizadora e Regulatória", "c": "Mapas Mentais com Chirley", "d": "5:33"}], "falhas de mercado": [{"id": "JjvYhrUzRS4", "t": "Regulação e Agências Reguladoras: Falhas de Mercado", "c": "Prof Lucas Martins", "d": "1:02:34"}, {"id": "E1IOloq0xz8", "t": "Bloco 9 CNU - Questões FGV/FCC - FALHAS DE MERCADO - Regulação e Agências Reguladoras", "c": "Entre Provas e Páginas", "d": "40:50"}], "agências reguladoras regulação econômica": [{"id": "5YPn2CSaRLk", "t": "Agências Reguladoras: o que mais cai em concursos públicos", "c": "Estratégia Carreira Jurídica", "d": "21:07"}, {"id": "P6tTIwhhFWs", "t": "AGÊNCIAS REGULADORAS", "c": "Aprovação PGE", "d": "29:49"}], "análise de impacto regulatório": [{"id": "7O5mZjUo9QQ", "t": "Análise de Impacto Regulatório", "c": "Irene Nohara", "d": "34:29"}, {"id": "fIMP9_Rpk_4", "t": "Análise de Impacto Regulatório e Avaliação de Resultado Regulatório (Resumo) | CNU Bloco 9 Regulação", "c": "Paulo Gabriel", "d": "10:22"}], "concessões Lei 8.987": [{"id": "eHSv5IF9t3A", "t": "Lei 8.987/95 - Concessões e Permissões de Serviços Públicos - AlfaCon", "c": "AlfaCon", "d": "2:06:06"}, {"id": "T4bj9HkCjWM", "t": "Mega revisão + questões de Serviços Públicos", "c": "Thállius Moraes - Simplifica", "d": "1:56:00"}], "Declaração Universal dos Direitos Humanos": [{"id": "6GSRf9AIqig", "t": "Declaração Universal dos Direitos Humanos | DUDH em 30m", "c": "Ricardo Torques", "d": "28:15"}, {"id": "Lb_9wBvjugk", "t": "Declaração Universal dos Direitos Humanos (1948) - Resumo e Importância", "c": "Me Julga - Cíntia Brunelli", "d": "13:10"}], "Agenda 2030 ODS": [{"id": "1hf-dpWFEdU", "t": "Agenda 2030 da ONU | O que você precisa para Gabaritar!", "c": "Ricardo Torques", "d": "19:10"}, {"id": "Ih7VgcNICx8", "t": "CNU 2025: Bloco 6 | Objetivos de Desenvolvimento Sustentável (ODS) e a Agenda 2030", "c": "Gran Cursos Online", "d": "1:12:06"}], "Estatuto da Pessoa com Deficiência": [{"id": "sctA6VSPmVc", "t": "Estatuto da Pessoa com Deficiência em 30 minutos: o que cai nas provas de concurso?", "c": "Ricardo Torques", "d": "27:31"}, {"id": "u62NnbOgEA4", "t": "ESTATUTO DA PESSOA COM DEFICIÊNCIA (Lei 13.146/15) - RESUMO - Lei Brasileira de Inclusão", "c": "Me Julga - Cíntia Brunelli", "d": "14:28"}], "ciclo de políticas públicas": [{"id": "AYbagoNSdIQ", "t": "POLÍTICAS PÚBLICAS: conceito e ciclo! Aula simples e objetiva para você entender de uma vez!", "c": "Professora Camila Miranda", "d": "25:22"}, {"id": "Ug3FQXMszZY", "t": "CNU Pós-Edital: Políticas Públicas em UMA AULA - Prof. Rodrigo Rennó", "c": "Estratégia Concursos", "d": "3:36:50"}], "tipologia de Lowi políticas públicas": [{"id": "57gvIG7F3_A", "t": "CNU: Introdução às Políticas Públicas:  conceitos e tipologias", "c": "SOMA Concursos", "d": "31:29"}, {"id": "zezRGcdm5TQ", "t": "POLÍTICAS PÚBLICAS - O que são? | Importância, tipos, exemplos e para que servem (RESUMO)", "c": "Me Julga - Cíntia Brunelli", "d": "10:54"}], "avaliação de políticas públicas": [{"id": "Eytlr8NhIYc", "t": "Políticas Públicas para Concursos Públicos - Teoria e Questões Comentadas", "c": "Rodrigo Rennó", "d": "2:26:33"}, {"id": "lRM3gkvuxvw", "t": "Políticas Públicas do ZERO para o CNU - Semana Nacional dos Concursos Públicos 2025", "c": "Estratégia Concursos", "d": "2:28:55"}], "business intelligence data warehouse": [{"id": "9c5CrHeOa7s", "t": "Concurso BB - Informática para Concursos - Business Intelligence (BI)  com Danilo Vilanova #opior", "c": "Professor Danilo Vilanova | Informática Concursos", "d": "28:23"}, {"id": "V07Pk4de-5M", "t": "Data Warehouse / Data Lake / Data Lakehouse // Dicionário do Programador", "c": "Código Fonte TV", "d": "15:10"}], "CRISP-DM": [{"id": "QrU5VHLZ1iw", "t": "CRISP DM Methodology | A Step-by-Step method to execute a Data Science project", "c": "the outlier 73", "d": "8:11"}, {"id": "qjSqIHUD2lw", "t": "3. Aula 3 - Metodologia de Trabalho CRISP DM", "c": "Professor Máiron Chaves", "d": "9:22"}], "SQL para concursos": [{"id": "yifCmXP_sm8", "t": "EA SEFAZ GO: Linguagem SQL - Prof. Renê Garcez", "c": "Estratégia Concursos", "d": "2:02:31"}, {"id": "OFLMhFuArXQ", "t": "SQL Saia do ZERO em APENAS UMA AULA", "c": "Jerry Strazzeri", "d": "22:56"}], "big data Hadoop": [{"id": "IBHOJI2hR2A", "t": "Noções de Big Data", "c": "Prof. Marcel Rios | Informática", "d": "28:01"}, {"id": "MFl2AHx0dPs", "t": "Revisão Completa para concursos: Banco de Dados, NoSQL, BI, Big Data, Mineração de Dados", "c": "Samyr Abdo - Domine TI Concursos", "d": "1:44:27"}], "estatística para concursos inferência": [{"id": "OfGi3LaN7qc", "t": "Curso Completo de Estatística - Direto ao Ponto - Prof. Jhoni Zini", "c": "Estratégia Concursos", "d": "3:17:08"}, {"id": "2j3kjH5m4M4", "t": "Estatística para Concursos Públicos - Saindo do zero - Prof. Jhoni Zini", "c": "Estratégia Concursos", "d": "3:24:10"}], "distribuição normal": [{"id": "CcIhlbN1U9Q", "t": "DISTRIBUIÇÃO NORMAL DE PROBABILIDADES ✅ EP 01", "c": "Prof. MURAKAMI - MATEMÁTICA RAPIDOLA", "d": "9:23"}, {"id": "rMfJID2l4Fs", "t": "Distribuição Normal : Definição e Fórmula", "c": "Aplicadas Descomplicadas", "d": "11:18"}], "amostragem estatística concurso": [{"id": "-N0ID7HFWco", "t": "Estatística para iniciantes - Começando do Zero - Edital PF - AlfaCon", "c": "AlfaCon", "d": "2:01:29"}, {"id": "Oj3aSpJxhd0", "t": "Concurso PC PE 2024 - Aula de Estatística - AlfaCon", "c": "AlfaCon", "d": "1:39:58"}], "contabilidade pública MCASP": [{"id": "9eqkaOH2hzY", "t": "Contabilidade Pública DO ZERO para Concursos - Semana Nacional EC", "c": "Estratégia Concursos", "d": "3:45:12"}, {"id": "swaP1wkVTAI", "t": "Contabilidade Pública para Concurso - Aula 001 - Introdução a CASP", "c": "Prof. Marcelo Pierri Junior", "d": "34:29"}], "PCASP": [{"id": "nB0DDOOC9YM", "t": "Curso de Contabilidade Pública em Questões - Prof. Gilmar Possati", "c": "Estratégia Concursos", "d": "3:29:05"}, {"id": "ykON_Sb785Y", "t": "RESUMÃO CONTABILIDADE PÚBLICA: TUDO O QUE VOCÊ PRECISA SABER", "c": "Contabilidade Facilitada", "d": "22:04"}], "balanço patrimonial setor público": [{"id": "ykON_Sb785Y", "t": "RESUMÃO CONTABILIDADE PÚBLICA: TUDO O QUE VOCÊ PRECISA SABER", "c": "Contabilidade Facilitada", "d": "22:04"}, {"id": "nJJWDb2kxyM", "t": "BALANÇO PATRIMONIAL DO ZERO [EM 27 MINUTOS] 🔴", "c": "CFC Academy", "d": "27:35"}], "processo civil CPC 2015 concurso": [{"id": "BWKBZpDZKS8", "t": "Direito Processual Civil do ZERO - Melhor que Black Friday", "c": "Estratégia Concursos", "d": "2:20:26"}, {"id": "kzuPeRSrzac", "t": "Competência | Processo Civil Desenhado", "c": "Ricardo Torques", "d": "39:40"}], "recursos no CPC": [{"id": "9k5ETWUFX2Y", "t": "Recursos | Processo Civil Desenhado", "c": "Ricardo Torques", "d": "34:45"}, {"id": "Fe1NA_BZwoU", "t": "TEORIA GERAL DOS RECURSOS - Resumo | Conceito, Requisitos e Efeitos | Processo Civil", "c": "Me Julga - Cíntia Brunelli", "d": "12:14"}], "direito do trabalho para tribunais": [{"id": "ChvJAt0EfHM", "t": "Direito do Trabalho para TRTs 2026: Top 3 assuntos mais cobrados", "c": "Estratégia Concursos", "d": "1:13:07"}, {"id": "ozN5MyO-MdY", "t": "Hora da Verdade TRT SP: Direito do Trabalho - Prof. Antônio Daud", "c": "Estratégia Concursos", "d": "3:47:01"}], "processo do trabalho recursos": [{"id": "ZYo8gkbnmVU", "t": "Processo do Trabalho Simplificado - Recursos - Prof. Thallius Moraes", "c": "Estratégia Concursos", "d": "2:51:36"}, {"id": "wDFBuEhBIrg", "t": "Todas as fases do processo do trabalho em uma aula - Prof. Bruno Klippel", "c": "Prof. Bruno Klippel", "d": "1:43:17"}], "reforma trabalhista Lei 13.467": [{"id": "ELEMQwQIsiY", "t": "A lei na sua prova - Lei 13.467/17: A Reforma Trabalhista", "c": "Gran Jurídico", "d": "1:04:11"}, {"id": "bKSt0On31MQ", "t": "ALTERAÇÕES DA REFORMA TRABALHISTA | Lei nº 13.467/2017", "c": "Cátia Ceratti", "d": "7:43"}], "crimes contra a administração pública": [{"id": "veoRK9HfTFc", "t": "CRIMES CONTRA A ADMINISTRAÇÃO PÚBLICA (RESUMO) - Peculato, Corrupção, Prevaricação e Concussão", "c": "Me Julga - Cíntia Brunelli", "d": "9:18"}, {"id": "jH8VAgYuaiQ", "t": "Direito Penal Especial - Dos Crimes contra a Administração Pública com Lucas Fávero", "c": "Focus Concursos", "d": "1:06:56"}], "inquérito policial": [{"id": "KhCuXohkhP0", "t": "Curso Gratuito | Direito Processual Penal para Concursos: Inquérito", "c": "Gran Cursos Online", "d": "1:55:16"}, {"id": "LKC-WndRbEU", "t": "INQUÉRITO POLICIAL ESQUEMATIZADO | DIREITO PROCESSUAL PENAL", "c": "Focus Concursos", "d": "1:09:12"}], "prisão e liberdade provisória": [{"id": "LF2oDroayFw", "t": "Curso Gratuito | Direito Processual Penal para Concursos: Prisão Temporária e Preventiva", "c": "Gran Cursos Online", "d": "1:33:41"}, {"id": "uRbaVbpiWfQ", "t": "PRISÕES E MEDIDAS CAUTELARES - Prisão Preventiva, Temporária, Liberdade Provisória, Medidas Diversas", "c": "Me Julga - Cíntia Brunelli", "d": "19:52"}], "regime geral de previdência social": [{"id": "wiu5W2BI12c", "t": "Aula de Direito Previdenciário | Começando do Zero INSS - AlfaCon", "c": "AlfaCon", "d": "59:58"}, {"id": "xWA6q-NtgtM", "t": "REGIMES DE PREVIDÊNCIA -  Regime Geral, Regime Próprio e Previdência Complementar | RGPS, RPPS, RPC", "c": "Me Julga - Cíntia Brunelli", "d": "23:56"}], "reforma da previdência EC 103/2019": [{"id": "hf67eANVXLs", "t": "REFORMA DA PREVIDÊNCIA - Regras Permanentes e Regras de Transição | Direito Previdenciário", "c": "Me Julga - Cíntia Brunelli", "d": "21:01"}, {"id": "bA_R8dHXfJM", "t": "Reforma da Previdência - Atualização para as provas de concursos", "c": "Gran Cursos Online", "d": "2:06:38"}], "benefícios previdenciários": [{"id": "FOccMVfgUsE", "t": "Concurso INSS | DOMINE Benefícios Previdenciários com Este Resumão Completo!", "c": "Gran Cursos Online", "d": "41:11"}, {"id": "fjH4LwqOyrI", "t": "INSS Direito Previdenciário para quem nunca estudou - Prof. Rubens Mauricio", "c": "Estratégia Concursos", "d": "2:18:16"}], "gestão por competências": [{"id": "3Uav1QsTS6o", "t": "Gestão por Competências - Aula Completa - Prof. Rodrigo Rennó", "c": "Rodrigo Rennó", "d": "25:58"}, {"id": "pEy9aGjOu0w", "t": "Questões CEBRASPE - Gestão por Competências - Petronio Castro", "c": "Prof. Petronio Castro - Administração", "d": "40:01"}], "avaliação de desempenho": [{"id": "RFzZbauQ2xA", "t": "Gestão do Desempenho - Administração de Recursos Humanos", "c": "Rodrigo Rennó", "d": "1:02:28"}, {"id": "xMUhr5NZifI", "t": "Gestão de Desempenho - Petronio Castro", "c": "Prof. Petronio Castro - Administração", "d": "26:29"}], "liderança e motivação": [{"id": "6dJyysPLq0s", "t": "Liderança - Aula Completa - Prof. Rodrigo Rennó", "c": "Rodrigo Rennó", "d": "59:57"}, {"id": "ajwMge4NNXw", "t": "Teorias de Motivação - Aula Completa - Prof. Rodrigo Rennó", "c": "Rodrigo Rennó", "d": "49:12"}]};
const ytw = id => 'https://www.youtube.com/watch?v='+id;

/* ---------- Estado e persistência ---------- */
const BLANK = ()=>({v:1, updatedAt:0, xp:0, goal:20, days:{}, ans:{}, srs:{}, cards:{}, sims:[], plan:{alvo:'tribunal', horas:15}, badges:{}, daily:{}, xpd:{}, vid:{}, perfil:{nome:''}, fav:{}, notes:{}, ed:{}, red:[], agenda:{dias:[1,1,1,1,1,1,0],min:[90,90,90,90,90,180,0]}});
let S = BLANK();
const LS='bancaAberta.v1';
try{ const raw=localStorage.getItem(LS); if(raw) S=Object.assign(BLANK(),JSON.parse(raw)); }catch(e){}
let dbRef=null, saveTimer=null, saving=false, pending=false;
function persist(){
  S.updatedAt=Date.now();
  try{ localStorage.setItem(LS, JSON.stringify(S)); }catch(e){}
  if(!dbRef) return;
  clearTimeout(saveTimer); saveTimer=setTimeout(flush,1500);
}
async function flush(){
  if(!dbRef) return;
  if(saving){pending=true;return}
  saving=true; setSync('Sincronizando…');
  try{ await dbRef.set(JSON.parse(JSON.stringify(S))); setSync(IS_ART?'Salvo na sua conta do claude.ai ✓':'Sincronizado ✓'); }
  catch(e){ setSync(e&&e.code==='quota_exceeded'?'Limite de armazenamento atingido':'Sem conexão; salvo neste aparelho'); }
  saving=false; if(pending){pending=false;flush()}
}
/* ---------- Sincronização: conta do claude.ai (artifact) ou Supabase (site) ---------- */
let SYNC_TXT='Salvo neste aparelho';
function setSync(t){ if(t) SYNC_TXT=t; document.querySelectorAll('[data-sync]').forEach(el=>el.textContent=SYNC_TXT); }
const IS_ART=!!(window.claude&&window.claude.use);
function localSave(){ try{localStorage.setItem(LS,JSON.stringify(S))}catch(e){} }
function backupUI(){
  const slot=document.getElementById('bkSlot'); if(!slot) return;
  slot.innerHTML='<div class="row" style="gap:6px"><button class="btn sm" id="bkOut">Exportar backup</button><button class="btn sm" id="bkIn">Importar backup</button><input type="file" id="bkFile" accept="application/json,.json" hidden></div><div class="note" id="bkMsg" style="margin-top:6px">Guarda ou restaura todo o seu progresso em um arquivo.</div>';
  const msg=t=>{document.getElementById('bkMsg').textContent=t};
  document.getElementById('bkOut').onclick=()=>{ try{
    const blob=new Blob([JSON.stringify(S)],{type:'application/json'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
    a.download='rumo-a-posse-backup-'+today()+'.json'; document.body.appendChild(a); a.click(); a.remove(); msg('Backup exportado.');
  }catch(e){msg('Não consegui exportar.')} };
  document.getElementById('bkIn').onclick=()=>document.getElementById('bkFile').click();
  document.getElementById('bkFile').onchange=async ev=>{ const f=ev.target.files[0]; if(!f) return; try{
    const d=JSON.parse(await f.text()); if(!d||typeof d!=='object'||Array.isArray(d)) throw 0;
    S=Object.assign(BLANK(),mergeS(S,d)); persist(); render(); toast('Backup importado e somado ao progresso atual.');
  }catch(e){ msg('Arquivo inválido.') } ev.target.value=''; };
}
let SB=null, UID=null, MAIL=null;
async function artStart(){
  try{
    const timer=setTimeout(()=>setSync('Salvo neste navegador'),10000);
    const [db,user]=await Promise.all([claude.use('db'),claude.use('user')]);
    if(!db||!user){clearTimeout(timer);return}
    const id=await user.id(); if(!id){clearTimeout(timer);return}
    const ref=db.collection('data/users/'+id).doc('progresso');
    const snap=await ref.get(); clearTimeout(timer);
    if(snap.exists){ const m=mergeS(S,snap.data()); if(JSON.stringify(m)!==JSON.stringify(S)){ S=Object.assign(BLANK(),m); localSave(); render(); } }
    UID=id; MAIL='sua conta do claude.ai'; dbRef={set:obj=>ref.set(obj)};
    if(S.updatedAt) await flush();
    setSync('Salvo na sua conta do claude.ai ✓'); authUI();
  }catch(e){ setSync('Salvo neste navegador'); }
}
async function sbStart(){
  try{
    if(!window.supabase) return;
    SB=supabase.createClient('https://yqiwcighfohcdovhihvp.supabase.co','sb_publishable_qN-5otd_jUA2eJWr8efzkg_q6uCBI_t',{auth:{persistSession:true,detectSessionInUrl:false}});
    const {data:{session}}=await SB.auth.getSession();
    if(session&&session.user) await sbUser(session.user);
    authUI();
  }catch(e){ authUI(); }
}
function mergeS(a,b){
  const r=JSON.parse(JSON.stringify(a)), nw=(b.updatedAt||0)>(a.updatedAt||0);
  const mx=(k)=>{ r[k]=Object.assign({},a[k]||{}); for(const d in (b[k]||{})) r[k][d]=Math.max(r[k][d]||0,b[k][d]||0); };
  mx('days'); mx('xpd'); r.xp=Math.max(a.xp||0,b.xp||0);
  r.ans=Object.assign({},a.ans||{}); r.srs=Object.assign({},a.srs||{});
  for(const id in (b.ans||{})){ const x=(a.ans||{})[id], y=b.ans[id]; if(!x||(y.n||0)>(x.n||0)){ r.ans[id]=y; if(b.srs&&b.srs[id]) r.srs[id]=b.srs[id]; else delete r.srs[id]; } }
  for(const id in (b.srs||{})) if(!(id in r.srs)&&!(b.ans&&b.ans[id]&&(a.ans||{})[id]&&(a.ans[id].n||0)>=(b.ans[id].n||0))) r.srs[id]=b.srs[id];
  r.cards=nw?Object.assign({},a.cards||{},b.cards||{}):Object.assign({},b.cards||{},a.cards||{});
  r.daily=Object.assign({},a.daily||{}); for(const d in (b.daily||{})){ const x=r.daily[d], y=b.daily[d]; if(!x||(y.n||0)>(x.n||0)) r.daily[d]=y; }
  r.badges=Object.assign({},b.badges||{},a.badges||{}); r.vid=Object.assign({},b.vid||{},a.vid||{});
  ['fav','notes','ed'].forEach(k=>{ r[k]=nw?Object.assign({},a[k]||{},b[k]||{}):Object.assign({},b[k]||{},a[k]||{}); });
  const uniq=(x,y,key)=>{ const seen=new Set(), out=[]; for(const s of [].concat(x||[],y||[])){ const k=key(s); if(!seen.has(k)){seen.add(k);out.push(s)} } return out; };
  r.sims=uniq(a.sims,b.sims,s=>JSON.stringify(s)).sort((x,y)=>String(x.d).localeCompare(String(y.d)));
  r.red=uniq(nw?b.red:a.red,nw?a.red:b.red,s=>s.id||JSON.stringify(s)).slice(-30);
  if(nw){ r.goal=b.goal; r.plan=b.plan; r.perfil=Object.assign({},a.perfil||{},b.perfil||{}); r.agenda=b.agenda||a.agenda; }
  r.updatedAt=Math.max(a.updatedAt||0,b.updatedAt||0);
  return r;
}
async function pullMerge(){
  if(!SB||!UID) return false;
  const {data,error}=await SB.from('progresso').select('data').eq('user_id',UID).maybeSingle();
  if(error) throw error;
  if(!(data&&data.data)) return false;
  const m=mergeS(S,data.data);
  if(JSON.stringify(m)===JSON.stringify(S)) return false;
  S=Object.assign(BLANK(),m); localSave(); render(); return true;
}
let pulling=false;
async function autoPull(){
  if(!SB||!UID||pulling||document.hidden) return; pulling=true;
  try{ setSync('Sincronizando…'); const ch=await pullMerge(); if(ch) await dbRef.set(JSON.parse(JSON.stringify(S))); setSync('Sincronizado ✓'); }
  catch(e){ setSync('Sem conexão; salvo neste aparelho'); } pulling=false;
}
async function sbUser(u){
  UID=u.id; MAIL=u.email;
  dbRef={ set: async obj=>{
    let cur=obj;
    try{ const {data}=await SB.from('progresso').select('data').eq('user_id',UID).maybeSingle();
      if(data&&data.data){ const m=mergeS(S,data.data); cur=m; if(JSON.stringify(m)!==JSON.stringify(S)){ S=Object.assign(BLANK(),m); localSave(); render(); } } }catch(e){}
    const {error}=await SB.from('progresso').upsert({user_id:UID,data:cur,updated_at:new Date().toISOString()}); if(error) throw error; } };
  try{ const ch=await pullMerge(); if(ch||S.updatedAt) await flush(); setSync('Sincronizado ✓'); }
  catch(e){ setSync('Sem conexão; salvo neste aparelho'); }
}
document.addEventListener('visibilitychange',()=>{ if(!document.hidden) autoPull(); });
window.addEventListener('focus',()=>autoPull());
setInterval(autoPull,60000);
function authUI(){
  const el=document.getElementById('authSlot'); if(!el) return;
  setSync();
  if(IS_ART){ el.innerHTML='<p class="note" style="margin:0">Nesta versão, o progresso é salvo na sua conta do claude.ai e aparece em qualquer aparelho em que você abrir este link.</p>'; return; }
  const inp='padding:8px 10px;border:1px solid var(--line2);border-radius:7px;background:var(--paper);color:var(--ink);flex:1;min-width:150px;font:inherit';
  if(MAIL){ el.innerHTML='<div class="row"><span>Sincronizando como <b>'+esc(MAIL)+'</b></span><button class="btn sm" id="sbOut">Sair</button></div>';
    document.getElementById('sbOut').onclick=async()=>{await SB.auth.signOut(); UID=null;MAIL=null;dbRef=null; setSync('Salvo neste aparelho'); authUI();}; return; }
  el.innerHTML='<form id="sbForm" style="display:flex;gap:8px;flex-wrap:wrap"><input id="sbMail" type="email" required placeholder="e-mail" autocomplete="username" style="'+inp+'"><input id="sbPass" type="password" required minlength="6" placeholder="senha (mín. 6)" autocomplete="current-password" style="'+inp+'"><button class="btn pri" type="submit">Entrar</button><button class="btn" id="sbNew" type="button">Criar conta</button></form><div class="note" id="sbMsg" style="margin-top:6px">Opcional. Sem conta, tudo fica salvo só neste navegador.</div>';
  const msg=t=>{document.getElementById('sbMsg').textContent=t};
  async function go(kind){
    const m=document.getElementById('sbMail').value.trim(), pw=document.getElementById('sbPass').value;
    if(!SB){msg('Servidor indisponível agora.');return} if(!m||pw.length<6){msg('Informe e-mail e senha de 6+ caracteres.');return}
    msg('Aguarde…');
    const r=kind==='new'?await SB.auth.signUp({email:m,password:pw}):await SB.auth.signInWithPassword({email:m,password:pw});
    if(r.error){ msg(r.error.message==='Invalid login credentials'?'E-mail ou senha incorretos.':'Erro: '+r.error.message); return }
    if(!r.data.session){ msg('Conta criada. Confirme o e-mail que o sistema enviou e depois entre.'); return }
    await sbUser(r.data.session.user); authUI();
  }
  document.getElementById('sbForm').onsubmit=ev=>{ev.preventDefault();go('in')};
  document.getElementById('sbNew').onclick=()=>go('new');
}
if(IS_ART) artStart(); else sbStart();

/* ---------- Gamificação ---------- */
const LEVELS=['Candidato','Inscrito','Em preparação','Constante','Competitivo','Aprovável','Classificado','Nomeado','Empossado'];
const lvl = xp => { const i=Math.min(LEVELS.length-1,Math.floor(xp/300)); return {i, name:LEVELS[i], into:xp-i*300, need:300}; };
function activity(n=1){ const d=today(); S.days[d]=(S.days[d]||0)+n; }
function streak(){ let s=0, d=today(); if(!S.days[d]) d=addDays(d,-1); while(S.days[d]){s++; d=addDays(d,-1)} return s; }
function gain(x,msg){ const before=lvl(S.xp).i; S.xp+=x; const d=today(); S.xpd=S.xpd||{}; S.xpd[d]=(S.xpd[d]||0)+x; const after=lvl(S.xp).i; if(after>before){ toast('Novo nível: '+LEVELS[after]); } else if(msg) toast(msg); checkBadges(); }
function weekXP(off=0){ let t=0; const base=new Date(today()+'T12:00:00'); const dow=(base.getDay()+6)%7; const start=addDays(today(),-dow-7*off); for(let i=0;i<7;i++){ t+=(S.xpd||{})[addDays(start,i)]||0 } return t; }
/* Sem efeitos de confete: feedback discreto */
function confetti(){}
/* Missões do dia */
function dayRec(){ const d=today(); S.daily=S.daily||{}; if(!S.daily[d]){ S.daily[d]={n:0,ok:0,max:0,rev:0,disc:{},banca:{},claimed:{}}; const ks=Object.keys(S.daily).sort(); while(ks.length>30) delete S.daily[ks.shift()]; } return S.daily[d]; }
let COMBO=0, LASTBONUS=0;
function hashStr(t){ let h=0; for(const ch of t) h=(h*31+ch.charCodeAt(0))|0; return Math.abs(h); }
function missions(){
  const D=dayRec(), h=hashStr(today()), bancas=['Cebraspe','FGV','Cesgranrio','FCC'], b=bancas[h%4];
  const foco=planRows()[0]?.d||'Língua Portuguesa';
  const pool=[
    {id:'combo',t:'5 acertos seguidos',sub:'Sequência sem erro na mesma sessão',cur:D.max,goal:5},
    {id:'rev',t:'Revise 5 itens da fila',sub:'A revisão espaçada é o que fixa a matéria',cur:D.rev,goal:5},
    {id:'foco',t:'8 questões de '+foco,sub:'Matéria prioritária do seu plano',cur:D.disc[foco]||0,goal:8},
    {id:'banca',t:'6 questões da '+b,sub:'Treino do estilo da banca',cur:D.banca[b]||0,goal:6},
    {id:'acc',t:'Feche o dia com 70% de acerto',sub:'Mínimo de 10 questões',cur:D.n>=10?Math.round(100*D.ok/D.n):0,goal:70,pct:true},
  ];
  const a=pool[h%pool.length], c=pool[(h+2)%pool.length];
  return [{id:'meta',t:'Bata a meta: '+S.goal+' questões',sub:'Ajustável no Início',cur:D.n,goal:S.goal},a,c].map(m=>({...m,done:m.cur>=m.goal,claimed:!!D.claimed[m.id]}));
}
function checkMissions(){ const D=dayRec(); missions().forEach(m=>{ if(m.done&&!D.claimed[m.id]){ D.claimed[m.id]=1; setTimeout(()=>{ gain(50); toast('Meta concluída: '+m.t+' · +50 XP'); },600); } }); }
const BADGES=[
  ['1º','Primeiro acerto',()=>Object.values(S.ans).some(a=>a.ok)],
  ['50','50 questões',()=>Object.keys(S.ans).length>=50],
  ['500','500 questões',()=>Object.keys(S.ans).length>=500],
  ['x10','10 acertos seguidos',()=>Object.values(S.daily||{}).some(d=>d.max>=10)],
  ['MIS','Todas as metas do dia',()=>Object.values(S.daily||{}).some(d=>Object.keys(d.claimed||{}).length>=3)],
  ['7d','7 dias seguidos',()=>streak()>=7],
  ['SIM','Simulado completo',()=>S.sims.length>0],
  ['80%','80% numa matéria',()=>DISCS.some(d=>{const r=discStats(d);return r.n>=8&&r.pct>=80})],
  ['META','Meta do dia',()=>(S.days[today()]||0)>=S.goal],
  ['REV','10 revisões',()=>Object.values(S.srs).filter(x=>x.reps>=2).length>=10],
];
function checkBadges(){ BADGES.forEach(([k,n,f])=>{ if(!S.badges[k]&&f()){S.badges[k]=today(); setTimeout(()=>toast('Conquista: '+n),900)} }) }
let toastT; function toast(t){ let el=$('.toast'); if(!el){el=document.createElement('div');el.className='toast';el.setAttribute('role','status');document.body.appendChild(el)} el.textContent=t; el.hidden=false; clearTimeout(toastT); toastT=setTimeout(()=>el.hidden=true,2200) }

/* ---------- Revisão espaçada (Leitner/SM-2 simplificado) ---------- */
const STEPS=[1,3,7,15,30,60];
function schedule(store,id,ok){
  const it=store[id]||{step:-1,reps:0};
  it.step = ok ? Math.min(STEPS.length-1,it.step+1) : 0;
  it.reps++; it.due=addDays(today(), ok?STEPS[it.step]:1); store[id]=it;
}
const dueQs = ()=>Object.entries(S.srs).filter(([id,x])=>x.due<=today()&&QBY[id]&&!QBY[id].anulada).map(([id])=>id);

function record(q,choice){
  const ok = choice===q.ans;
  const a=S.ans[q.id]||{n:0,hits:0,hist:[]};
  a.n++; if(ok)a.hits++; a.ok=ok; a.last=choice; a.d=today(); a.hist.push([today(),ok?1:0]); if(a.hist.length>10)a.hist.shift();
  const D=dayRec(), wasDue=S.srs[q.id]&&S.srs[q.id].due<=today();
  D.n++; if(ok)D.ok++; if(wasDue)D.rev++; D.disc[q.disc]=(D.disc[q.disc]||0)+1; const bn=SRC[q.src].banca; D.banca[bn]=(D.banca[bn]||0)+1;
  COMBO=ok?COMBO+1:0; D.max=Math.max(D.max||0,COMBO); LASTBONUS=ok&&COMBO>1?Math.min(10,2*(COMBO-1)):0;
  S.ans[q.id]=a; schedule(S.srs,q.id,ok); activity(); gain((ok?10:3)+LASTBONUS); checkMissions(); persist();
  return ok;
}
function discStats(d,src){ let n=0,h=0; Q.forEach(q=>{ if(d&&q.disc!==d) return; if(src&&SRC[q.src].banca!==src) return; if(q.ia) return; const a=S.ans[q.id]; if(a&&!q.anulada){n++; if(a.ok)h++} }); return {n,h,pct:n?Math.round(100*h/n):0}; }
function statsWhere(f){ let n=0,h=0; Q.forEach(q=>{ if(!f(q)||q.anulada) return; const a=S.ans[q.id]; if(a){n++; if(a.ok)h++} }); return {n,h,pct:n?Math.round(100*h/n):0}; }
const REAL=Q.filter(q=>!q.ia), IAQ=Q.filter(q=>q.ia);
const TIPOS=[]; Object.values(SRC).forEach(s=>{ if(s.tipo&&!TIPOS.some(x=>x[0]===s.tipo)) TIPOS.push([s.tipo,s.tipo_nome]); });
const TORD=['aj_adm','aj_jud','aj_cg','aj_esp','tc','tec','mpu','cnu_gestao','regulacao','policia','ia']; TIPOS.sort((a,b)=>(TORD.indexOf(a[0])+99)%108-(TORD.indexOf(b[0])+99)%108);
const srcLabel=s=>s.ia?'Inédita (IA) · estilo '+s.banca:`${s.orgao_curto||s.orgao} ${s.ano}`;
const ANTIGA='Prova anterior a mudanças importantes na lei (Reforma da Previdência de 2019, Lei 14.133/2021 de licitações, Lei 14.230/2021 de improbidade). O gabarito reflete a lei da época: confira a lei atual.';

/* ---------- Componentes ---------- */
function supportHTML(key){
  const paras=(TXT[key]||'').split(/\n\n/);
  if(paras.some(p=>p.includes(' | '))){
    const rows=paras.filter(p=>p.includes(' | ')).map(p=>p.split(' | '));
    const head=paras.filter(p=>!p.includes(' | ')).map(p=>`<p><b>${esc(p)}</b></p>`).join('');
    return '<div class="support" tabindex="0" aria-label="Tabela de apoio">'+head+'<div style="overflow-x:auto"><table style="border-collapse:collapse;font-family:var(--mono,monospace)">'+rows.map((r,i)=>'<tr>'+r.map(c=>`<${i?'td':'th'} style="border:1px solid currentColor;padding:4px 10px;text-align:left">${esc(c)}</${i?'td':'th'}>`).join('')+'</tr>').join('')+'</table></div></div>';
  }
  return '<div class="support" tabindex="0" aria-label="Texto de apoio">'+paras.map(p=>`<p class="${p.length<140&&/(\(com adaptações\)|Internet:|p\. \d|\d{4})/.test(p)||p.length<70?'src':''}">${esc(p)}</p>`).join('')+'</div>';
}
function metaHTML(q){
  const s=SRC[q.src];
  if(s.ia) return `<div class="qmeta"><span class="qnum">${q.fmt==='CE'?'Item':'Questão'} ${q.n}</span><span class="chip ia">Inédita (IA)</span><span>No estilo ${esc(s.banca)} · não caiu em prova</span><span class="chip ghost">${esc(q.disc)}</span></div>`;
  return `<div class="qmeta"><span class="qnum">${q.fmt==='CE'?'Item':'Questão'} ${q.n}</span><span class="chip">${esc(s.banca)}</span><span>${esc(s.orgao_curto||s.orgao)} · <b>${s.ano}</b> · ${esc(s.cargo)}</span>${s.antiga?`<span class="chip warn" title="${esc(ANTIGA)}">Prova de ${s.ano}: confira a lei atual</span>`:''}<span class="chip ghost" ${q.auto?'title="Matéria definida por classificação automática (palavras-chave); pode haver erro"':''}>${esc(q.disc)}${q.auto?' · auto':''}</span>${q.anulada?'<span class="chip warn">Anulada</span>':''}</div>`;
}
function linksHTML(q){
  const s=SRC[q.src];
  return `<div class="links">${s.ia?'':`<a href="${s.prova}" target="_blank" rel="noopener">Prova original (PDF)</a><a href="${s.gabarito}" target="_blank" rel="noopener">Gabarito</a>`}${s.ajuste?`<a href="${s.ajuste}" target="_blank" rel="noopener">Anulações e alterações (site da FCC)</a>`:''}${q.just?`<a href="${q.just}" target="_blank" rel="noopener">Justificativa da banca</a>`:''}${q.lei?`<a href="${q.lei}" target="_blank" rel="noopener">Lei seca</a>`:''}${AULAS[q.disc]?`<a href="#aulas" data-aula="${esc(q.disc)}">Aulas de ${esc(q.disc)}</a>`:`<a href="${yt(q.auto?q.disc:q.tema)}" target="_blank" rel="noopener">Buscar aulas: ${esc(q.auto?q.disc:q.tema)}</a>`}</div>`;
}
function ring(v,max,label){
  const p=Math.min(1,v/max), r=40, c=2*Math.PI*r;
  return `<svg class="ring" viewBox="0 0 96 96" role="img" aria-label="${label}"><circle cx="48" cy="48" r="${r}" fill="none" stroke="var(--line)" stroke-width="8"/><circle cx="48" cy="48" r="${r}" fill="none" stroke="var(--accent)" stroke-width="8" stroke-linecap="round" stroke-dasharray="${c*p} ${c}" transform="rotate(-90 48 48)"/><text x="48" y="46" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-weight="600" font-size="18" fill="var(--ink)">${v}</text><text x="48" y="64" text-anchor="middle" font-size="10" fill="var(--muted)">de ${max}</text></svg>`;
}

/* ---------- Resolver questão (usado em Questões e Revisão) ---------- */
function questionCard(q,{onNext,showNext=true,ctx=''}={}){
  const el=document.createElement('section'); el.className='panel'; el.style.display='flex'; el.style.flexDirection='column'; el.style.gap='14px';
  const a=S.ans[q.id];
  el.innerHTML = metaHTML(q) + (q.text?supportHTML(q.text):'') + (q.cmd?`<div class="cmd">${esc(q.cmd)}</div>`:'') + `<div class="stem">${esc(q.stem)}</div>` +
    (q.fmt==='CE' ? `<div class="ce" role="group" aria-label="Julgue o item"><button class="opt" data-c="C"><span class="bub">C</span>Certo</button><button class="opt" data-c="E"><span class="bub">E</span>Errado</button></div>`
      : `<div class="opts" role="group" aria-label="Alternativas">${q.opts.map((o,i)=>{const L='ABCDE'[i];return `<button class="opt" data-c="${L}"><span class="bub">${L}</span><span>${esc(o)}</span></button>`}).join('')}</div>`) +
    `<div class="fbslot"></div>${toolsHTML(q)}<div class="row between"><span class="note">${ctx}${a?` Você já respondeu ${a.n}× (${a.hits} acerto${a.hits===1?'':'s'}).`:''}</span>${showNext?'<button class="btn pri nx">Próxima</button>':''}</div>`;
  const buttons=[...el.querySelectorAll('.opt')];
  buttons.forEach(b=>b.onclick=()=>{
    const c=b.dataset.c;
    buttons.forEach(x=>x.disabled=true);
    let ok=null;
    if(!q.anulada) ok=record(q,c); else { activity(); persist(); }
    buttons.forEach(x=>{ if(!q.anulada&&x.dataset.c===q.ans) x.classList.add('right'); });
    if(ok===false) b.classList.add('wrong'); b.classList.add('sel');
    const fb=document.createElement('div');
    fb.className='fb '+(ok===null?'null':ok?'ok':'bad');
    fb.innerHTML=`<div class="h">${ok===null?'Item anulado pela banca':ok?'Correta · +'+(10+LASTBONUS)+' XP'+(COMBO>1?'<span class="combo">'+COMBO+' seguidas</span>':''):'Incorreta. Adicionada ao caderno de erros.'}</div>
      <div><b>${q.ia?'Gabarito da questão inédita:':'Gabarito oficial definitivo:'}</b> ${q.anulada?'anulado':q.ans}${q.fmt==='CE'?` (${q.ans==='C'?'Certo':q.ans==='E'?'Errado':''})`:''}</div>
      ${q.ia?`<div style="font-size:15px">${esc(q.com)}</div><div class="iabox">Questão inédita escrita por IA (Claude) no estilo da banca ${esc(SRC[q.src].banca)}. Não caiu em prova e não entra nas suas estatísticas de provas reais. Gabarito e comentário seguem a lei citada; em caso de dúvida, vale a lei seca.</div>`:q.com?`<div style="font-size:15px">${esc(q.com)}</div>
      <div class="ai">Comentário gerado por IA (Claude) e conferido com o gabarito oficial. Não é comentário da banca. Em caso de dúvida, vale a lei seca e a prova original.</div>`
      :`<div class="ai">Esta questão ainda não tem comentário escrito. O enunciado e o gabarito foram conferidos com os PDFs oficiais; para entender o porquê, use o tutor IA abaixo e confira na prova original.</div>`}
      ${SRC[q.src].antiga?`<div class="note"><b>Atenção:</b> ${esc(ANTIGA)}</div>`:''}
      ${linksHTML(q)}
      ${ok&&!q.anulada?rateHTML():''}
      <div class="row"><button class="btn sm tut">Explicar de outro jeito (tutor IA)</button></div><div class="tslot"></div>`;
    $('.fbslot',el).appendChild(fb);
    $('.tut',fb).onclick=()=>tutor(q,c,$('.tslot',fb),$('.tut',fb)); wireRate(fb,q);
    fb.querySelectorAll('[data-aula]').forEach(a=>a.onclick=()=>{AULA_OPEN=a.dataset.aula});
    renderNavDue();
  });
  const nx=$('.nx',el); if(nx) nx.onclick=()=>onNext&&onNext();
  wireTools(el,q);
  return el;
}
async function tutor(q,choice,slot,btn){
  if(!aiReady()){ slot.innerHTML=aiSetupHTML(); return; }
  btn.disabled=true; const box=document.createElement('div'); box.className='tutor'; box.textContent='Pensando…'; slot.replaceChildren(box);
  const s=SRC[q.src];
  const prompt=`${q.ia?'(Questão inédita criada por IA no estilo da banca, não é de prova real.) ':''}Você é um professor de cursinho para concursos públicos no Brasil, didático e direto. Explique para um iniciante a questão abaixo, em português, em no máximo 180 palavras: (1) a ideia central cobrada, (2) por que o gabarito oficial é esse, (3) uma dica de memorização ou pegadinha típica da banca ${s.banca}. Não contradiga o gabarito oficial; se discordar, diga apenas que vale conferir a lei. Texto simples, sem markdown.

Banca: ${s.banca} | Prova: ${s.orgao} ${s.ano}, ${s.cargo} | Matéria: ${q.disc} – ${q.tema}
${q.text?'Texto de apoio: '+TXT[q.text]+'\n':''}${q.cmd?'Comando: '+q.cmd+'\n':''}Enunciado: ${q.stem}
${q.opts?q.opts.map((o,i)=>'ABCDE'[i]+') '+o).join('\n'):'(Julgar Certo ou Errado)'}
Gabarito oficial: ${q.ans}
Resposta do aluno: ${choice}
Comentário de referência: ${q.com||'(não há comentário escrito; baseie-se no gabarito oficial)'}`;
  try{ box.textContent=await aiCall(prompt,{onText:t=>{box.textContent=t}}); }
  catch(e){ box.textContent=aiErr(e); }
  btn.disabled=false;
}

/* ---------- Views ---------- */
const V={};
const QF0=()=>({tipo:'',orgao:'',banca:'',disc:'',ass:'',status:'pend',periodo:'',origem:'real',src:'',q:''});
let QF=QF0(), qIdx=0;
const qfSet=o=>{QF=Object.assign(QF0(),o);qIdx=0};

V.painel=()=>{
  const L=lvl(S.xp), st=streak(), td=S.days[today()]||0, due=dueQs().length;
  const answered=Object.keys(S.ans).length, overall=discStats(), M=missions(), nxt=planRows()[0];
  const wk=weekXP(0), lw=weekXP(1), h=new Date().getHours(), saud=h<12?'Bom dia':h<18?'Boa tarde':'Boa noite';
  const dt=new Date().toLocaleDateString('pt-BR',{weekday:'long',day:'numeric',month:'long'});
  const nReal=REAL.length, porBanca=Object.entries(REAL.reduce((m,q)=>(m[SRC[q.src].banca]=(m[SRC[q.src].banca]||0)+1,m),{}));
  const realSrc=Object.values(SRC).filter(s=>!s.ia);
  return `
  <section class="panel hero">
    <div style="display:flex;flex-direction:column;gap:10px;min-width:0">
      <span class="note">${esc(dt)}</span>
      <h1>${saud}${S.perfil&&S.perfil.nome?', '+esc(S.perfil.nome):''}.</h1>
      <p class="sub" style="margin:0">Hoje: <b>${td} de ${S.goal}</b> questões da meta${due?` · <b>${due}</b> ${due===1?'item':'itens'} para revisar`:''}${st?` · ${st} dia${st===1?'':'s'} seguido${st===1?'':'s'}`:''}.</p>
      <div class="row"><a class="btn pri" href="#questoes" data-focus="${esc(nxt?nxt.d:'')}" style="text-decoration:none">Começar a sessão de hoje</a>${due?`<a class="btn" href="#revisao" style="text-decoration:none">Revisar ${due}</a>`:''}</div>
    </div>
    <div class="lvlbox">
      <div class="row between"><span class="stat"><span>Nível ${L.i+1} de ${LEVELS.length}</span></span><span class="xpw">${S.xp} XP</span></div>
      <b style="font-size:17px">${esc(L.name)}</b>
      <div class="bar"><i style="width:${Math.round(100*L.into/L.need)}%"></i></div>
      <span class="note">${L.i<LEVELS.length-1?`${L.need-L.into} XP para ${esc(LEVELS[L.i+1])}`:'Nível máximo'}. Acerto vale 10 XP, erro 3 XP e cada meta concluída 50 XP.</span>
      <div class="steps" aria-hidden="true">${LEVELS.map((_,k)=>`<i class="${k<=L.i?'on':''}"></i>`).join('')}</div>
    </div>
  </section>
  <div class="grid g2">
    <div class="panel"><div class="row between"><h2>Metas do dia</h2><span class="note">renovam à meia-noite</span></div>
      <div style="margin-top:4px">${M.map(m=>`<div class="mission ${m.done?'done':''}"><div class="ic">${m.done?'✓':m.id==='rev'?'↻':m.id==='acc'?'%':m.id==='combo'?'5':'#'}</div><div style="min-width:0"><b>${esc(m.t)}</b><div class="note">${esc(m.sub)}</div><div class="bar ${m.done?'ok':''}" style="margin-top:6px"><i style="width:${Math.min(100,100*m.cur/m.goal)}%"></i></div></div><span class="xpw">${m.done?'+50 XP':Math.min(m.cur,m.goal)+(m.pct?'%':'')+' / '+m.goal+(m.pct?'%':'')}</span></div>`).join('')}</div></div>
    <div class="grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">
      <div class="panel row" style="gap:12px">${ring(td,S.goal,'Meta do dia')}<div class="stat"><span>Meta do dia</span><b>${td}/${S.goal}</b><div class="row" style="gap:6px"><button class="btn sm" data-goal="-5" aria-label="Diminuir meta">−5</button><button class="btn sm" data-goal="5" aria-label="Aumentar meta">+5</button></div></div></div>
      <div class="panel stat"><span>Sequência</span><b class="streak">${st} dia${st===1?'':'s'}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">Dias seguidos com pelo menos uma questão.</span></div>
      <div class="panel stat"><span>XP da semana</span><b>${wk}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">${lw?(wk>=lw?'Acima da semana passada ('+lw+')':'Faltam '+(lw-wk)+' para igualar a semana passada'):'Primeira semana registrada'}</span></div>
      <div class="panel stat"><span>Acerto em provas reais</span><b>${overall.n?overall.pct+'%':'–'}</b><span style="text-transform:none;letter-spacing:0;font-weight:400">${answered} resolvidas · ${S.sims.length} simulado${S.sims.length===1?'':'s'}</span></div>
    </div>
  </div>
  ${nxt?`<div class="panel row between"><div style="min-width:0"><h3>Próxima matéria do seu plano: ${esc(nxt.d)}</h3><p class="note" style="margin:4px 0 0">${esc(nxt.why)}</p></div><a class="btn pri" href="#questoes" data-focus="${esc(nxt.d)}" style="text-decoration:none">Treinar agora</a></div>`:''}
  <div class="panel"><div class="row between"><h2>Conquistas</h2><span class="note">${Object.keys(S.badges).length} de ${BADGES.length}</span></div><div class="badges" style="margin-top:12px">${BADGES.map(([k,n])=>`<div class="badge ${S.badges[k]?'on':''}"><div class="m">${k}</div>${n}</div>`).join('')}</div></div>
  <div class="panel"><h2>Origem das questões</h2><p class="note">${nReal} questões de ${realSrc.length} provas oficiais públicas (${porBanca.map(([b,n])=>`${n} ${b}`).join(', ')}), sempre com o gabarito definitivo da banca. Itens anulados aparecem marcados e não contam na nota. ${REAL.filter(q=>q.com).length} têm comentário escrito; nas demais, o tutor IA explica. Além delas, há ${IAQ.length} <b>questões inéditas escritas por IA</b> no estilo das bancas, separadas por um filtro próprio e fora das estatísticas. ${DATA.report?`Ficaram de fora ${Object.values(DATA.report.excluidas).reduce((a,b)=>a+b,0)} questões que dependiam de imagem, fórmula, sublinhado ou texto que não deu para conferir, ou que se repetiam em outro caderno.`:''}</p>
  <p class="note"><b>Vunesp:</b> 4 provas incluídas (TCE-SP Auditor de Controle Externo e Administração 2025, TJ-SP Contador 2025, Polícia Civil-SP Perito 2023). Os cadernos vêm do PCI Concursos, e o gabarito definitivo foi conferido em publicação oficial (Diário Oficial do TCE-SP, edital do TJSP e comunicado da Academia de Polícia). Outras provas Vunesp ficam de fora até aparecer o gabarito definitivo oficial.</p>
  ${TIPOS.filter(([k])=>k!=='ia').map(([k,nome])=>{const ss=realSrc.filter(s=>s.tipo===k).sort((a,b)=>b.ano-a.ano);return `<details style="margin-top:6px"><summary>${esc(nome)} <span class="note">· ${ss.length} prova${ss.length>1?'s':''} · ${Q.filter(q=>SRC[q.src].tipo===k).length} questões</span></summary><div class="tw"><table><thead><tr><th>Prova</th><th>Banca</th><th class="num">Questões</th><th>Fontes</th></tr></thead><tbody>${ss.map(s=>`<tr><td>${esc(s.orgao)} · <b>${s.ano}</b><br><span class="note">${esc(s.cargo)}</span>${s.origem?`<br><span class="note">${esc(s.origem)}</span>`:''}</td><td>${s.banca}</td><td class="num">${Q.filter(q=>q.src===s.id).length}</td><td><a href="${s.prova}" target="_blank" rel="noopener">prova</a> · <a href="${s.gabarito}" target="_blank" rel="noopener">gabarito</a>${s.ajuste?` · <a href="${s.ajuste}" target="_blank" rel="noopener">alterações (FCC)</a>`:''}</td></tr>`).join('')}</tbody></table></div></details>`}).join('')}</div>`;
};
V.painel.after=()=>{
  document.querySelectorAll('[data-goal]').forEach(b=>b.onclick=()=>{S.goal=Math.max(5,Math.min(200,S.goal+ +b.dataset.goal));persist();render()});
  document.querySelectorAll('[data-focus]').forEach(b=>b.onclick=()=>{qfSet({disc:b.dataset.focus||''})});
};

function filtered(){
  return Q.filter(q=>{
    const s=SRC[q.src];
    if(QF.origem==='real'&&q.ia) return false;
    if(QF.origem==='ia'&&!q.ia) return false;
    if(QF.src&&q.src!==QF.src) return false;
    if(QF.tipo&&s.tipo!==QF.tipo) return false;
    if(QF.orgao&&s.orgao_curto!==QF.orgao) return false;
    if(QF.banca&&s.banca!==QF.banca) return false;
    if(QF.periodo==='rec'&&!(s.ano>=2022)) return false;
    if(QF.periodo==='ant'&&!(s.ano<2022)) return false;
    if(QF.disc&&q.disc!==QF.disc) return false;
    if(QF.ass&&q.ass!==QF.ass) return false;
    if(QF.q&&!searchHit(q,QF.q)) return false;
    if(QF.status==='fav') return !!S.fav[q.id];
    if(QF.status==='nota') return !!S.notes[q.id];
    const a=S.ans[q.id];
    if(QF.status==='pend'&&a) return false;
    if(QF.status==='erradas'&&!(a&&!a.ok)) return false;
    if(QF.status==='certas'&&!(a&&a.ok)) return false;
    return true;
  });
}
V.questoes=()=>{
  const opt=(arr,cur)=>arr.map(([v,l])=>`<option value="${esc(v)}" ${v===cur?'selected':''}>${esc(l)}</option>`).join('');
  const srcs=Object.values(SRC).filter(s=>(!QF.tipo||s.tipo===QF.tipo)&&(QF.origem!=='real'||!s.ia)&&(QF.origem!=='ia'||s.ia));
  const nT=k=>Q.filter(q=>SRC[q.src].tipo===k).length;
  const orgs=[...new Set(srcs.filter(s=>!s.ia).map(s=>s.orgao_curto))].sort((a,b)=>a.localeCompare(b,'pt',{numeric:true}));
  const bancas=[...new Set(srcs.map(s=>s.banca))];
  const discs=[...new Set(Q.filter(q=>srcs.includes(SRC[q.src])).map(q=>q.disc))].sort((a,b)=>a.localeCompare(b,'pt'));
  return `<div><h1>Banco de questões</h1><p class="sub">Filtre pelo tipo de prova: o mesmo cargo cobrado por órgãos e anos diferentes fica junto. O ano aparece em cada questão e pode ser usado como filtro secundário.</p></div>
  <div class="panel" style="display:flex;flex-direction:column;gap:12px">
   <div class="row between"><div class="seg" role="group" aria-label="Origem das questões">${[['real','Provas reais'],['ia','Inéditas (IA)'],['','Todas']].map(([v,l])=>`<button data-org="${v}" class="${QF.origem===v?'on':''}">${l}</button>`).join('')}</div><span class="note" id="qcount"></span></div>
   <div class="grid g4">
    <label class="f" style="grid-column:span 2">Tipo de prova<select id="fTipo">${opt([['','Todos os tipos'],...TIPOS.filter(([k])=>QF.origem==='ia'?k==='ia':QF.origem==='real'?k!=='ia':true).map(([k,n])=>[k,n+' ('+nT(k)+')'])],QF.tipo)}</select></label>
    <label class="f">Banca<select id="fBanca">${opt([['','Todas'],...bancas.map(b=>[b,b])],QF.banca)}</select></label>
    <label class="f">Órgão<select id="fOrgao" ${QF.origem==='ia'?'disabled':''}>${opt([['','Todos'],...orgs.map(o=>[o,o])],QF.orgao)}</select></label>
    <label class="f" style="grid-column:span 2">Matéria<select id="fDisc">${opt([['','Todas'],...discs.map(d=>[d,d])],QF.disc)}</select></label>
    <label class="f">Período<select id="fPer">${opt([['','Todos os anos'],['rec','2022 em diante'],['ant','Até 2021']],QF.periodo)}</select></label>
    <label class="f">Mostrar<select id="fStatus">${opt([['pend','Não resolvidas'],['todas','Todas'],['erradas','Que errei'],['certas','Que acertei'],['fav','Favoritas ('+Object.keys(S.fav||{}).length+')'],['nota','Com anotação ('+Object.keys(S.notes||{}).length+')']],QF.status)}</select></label>
    ${QF.disc?`<label class="f" style="grid-column:span 2">Assunto<select id="fAss">${opt([['','Todos os assuntos'],...[...new Set(Q.filter(q=>q.disc===QF.disc&&q.ass).map(q=>q.ass))].sort((a,b)=>a.localeCompare(b,'pt')).map(a=>[a,a+' ('+Q.filter(q=>q.disc===QF.disc&&q.ass===a&&(QF.origem!=='real'||!q.ia)).length+')'])],QF.ass)}</select></label>`:''}
    <label class="f" style="grid-column:span ${QF.disc?2:4}">Buscar no enunciado<input id="fQ" type="search" value="${esc(QF.q)}" placeholder="ex.: crase, 8.112, licitação, prescrição" style="font:inherit;text-transform:none;letter-spacing:0;padding:7px 9px;border:1px solid var(--line2);border-radius:7px;background:var(--paper);color:var(--ink)"></label>
   </div>
   ${QF.src?`<div class="row"><span class="chip">Só a prova ${esc(srcLabel(SRC[QF.src]))}</span><button class="btn sm" id="fClrSrc">Ver o tipo inteiro</button></div>`:''}
  </div><div id="qslot"></div>`;
};
V.questoes.after=()=>{
  const map={fTipo:'tipo',fBanca:'banca',fOrgao:'orgao',fDisc:'disc',fStatus:'status',fPer:'periodo',fAss:'ass'};
  Object.keys(map).forEach(id=>{ const el=$('#'+id); if(el) el.onchange=e=>{ QF[map[id]]=e.target.value; if(id==='fTipo'){QF.orgao='';QF.banca='';QF.src=''} if(id==='fDisc') QF.ass=''; qIdx=0; render(); }; });
  const fq=$('#fQ'); let qt; fq.oninput=()=>{ clearTimeout(qt); qt=setTimeout(()=>{ QF.q=fq.value.trim(); qIdx=0; showQ(); },300); };
  document.querySelectorAll('[data-org]').forEach(b=>b.onclick=()=>{ QF.origem=b.dataset.org; QF.tipo='';QF.orgao='';QF.banca='';QF.src=''; qIdx=0; render(); });
  const c=$('#fClrSrc'); if(c) c.onclick=()=>{ if(QF.src&&!QF.tipo) QF.tipo=SRC[QF.src].tipo; QF.src=''; qIdx=0; render(); };
  showQ();
};
function showQ(){
  const list=filtered(), slot=$('#qslot'); if(!slot) return;
  if(!list.length){ const qc=$('#qcount'); if(qc) qc.textContent='0 questões neste recorte'; slot.innerHTML=`<div class="panel empty">Nenhuma questão com esses filtros. ${QF.status==='pend'?'Você resolveu tudo deste recorte! Troque “Mostrar” para “Que errei” e revise.':''}</div>`; return; }
  if(qIdx>=list.length) qIdx=0;
  const q=list[qIdx];
  const qc=$('#qcount'); if(qc){ const yrs=[...new Set(list.filter(x=>!x.ia).map(x=>SRC[x.src].ano))].sort(); qc.textContent=`${list.length} questões neste recorte · ${new Set(list.map(x=>x.src)).size} prova${new Set(list.map(x=>x.src)).size>1?'s':''}${yrs.length?' · '+(yrs.length>1?yrs[0]+'–'+yrs[yrs.length-1]:yrs[0]):''}`; }
  slot.replaceChildren(questionCard(q,{ctx:`${qIdx+1} de ${list.length} neste filtro.`,onNext:()=>{ if(QF.status!=='pend') qIdx++; showQ(); window.scrollTo({top:0}) }}));
}

V.revisao=()=>{
  const due=dueQs(), errs=Object.entries(S.ans).filter(([id,a])=>!a.ok&&QBY[id]).map(([id])=>id);
  return `<div><h1>Revisão</h1><p class="sub">Revisão espaçada: cada item volta em 1, 3, 7, 15, 30 e 60 dias se você acertar, e no dia seguinte se errar.</p></div>
  <div class="grid g2"><div class="panel stat"><span>Para revisar hoje</span><b>${due.length}</b></div><div class="panel stat"><span>Caderno de erros</span><b>${errs.length}</b></div></div>
  <div class="row"><button class="btn pri" id="rvDue" ${due.length?'':'disabled'}>Revisar os de hoje</button><button class="btn" id="rvErr" ${errs.length?'':'disabled'}>Refazer caderno de erros</button></div>
  <div id="rvslot">${due.length||errs.length?'':'<div class="panel empty">Nada para revisar ainda. Resolva questões e elas aparecem aqui no dia certo.</div>'}</div>
  ${errs.length?`<div class="panel"><h3>Caderno de erros</h3><div class="tw" style="margin-top:8px"><table><thead><tr><th>Item</th><th>Matéria</th><th>Prova</th><th>Próxima revisão</th></tr></thead><tbody>${errs.map(id=>{const q=QBY[id];return `<tr><td class="num">${q.n}</td><td>${esc(q.disc)}</td><td>${esc(srcLabel(SRC[q.src]))}</td><td>${S.srs[id]?.due||'-'}</td></tr>`}).join('')}</tbody></table></div></div>`:''}`;
};
V.revisao.after=()=>{
  const run=(ids,label)=>{ let i=0; const next=()=>{ const slot=$('#rvslot'); if(!slot) return; if(i>=ids.length){slot.innerHTML='<div class="panel empty">Revisão concluída. Volte amanhã para a próxima rodada.</div>';gain(0,'Revisão concluída');return} slot.replaceChildren(questionCard(QBY[ids[i]],{ctx:`${label}: ${i+1} de ${ids.length}.`,onNext:()=>{i++;next();window.scrollTo({top:0})}})) }; next(); };
  const d=$('#rvDue'); if(d) d.onclick=()=>run(dueQs(),'Revisão');
  const e=$('#rvErr'); if(e) e.onclick=()=>run(Object.entries(S.ans).filter(([id,a])=>!a.ok&&QBY[id]).map(([id])=>id),'Caderno de erros');
};

/* Simulados */
let SIM=null;
V.simulado=()=>{
  if(SIM&&!SIM.done) return simRun();
  if(SIM&&SIM.done) return simResult();
  return `<div><h1>Simulados</h1><p class="sub">Monte um simulado do seu jeito ou faça uma prova inteira, com tempo e folha de respostas. A nota segue a regra da banca.</p></div>
  ${customSimHTML()}
  ${TIPOS.map(([k,nome])=>{const ss=Object.values(SRC).filter(s=>s.tipo===k).sort((a,b)=>b.ano-a.ano||a.orgao_curto.localeCompare(b.orgao_curto,'pt',{numeric:true}));return `<div class="panel"><div class="tipohead"><h2>${esc(nome)}</h2><span class="note">${ss.length} prova${ss.length>1?'s':''}${k==='ia'?' · treino extra, fora das estatísticas':''}</span></div>${ss.map(s=>{const n=Q.filter(q=>q.src===s.id).length;const mins=s.formato==='CE'?Math.round(n*2.2):Math.round(n*3.4);const best=S.sims.filter(x=>x.src===s.id).sort((a,b)=>b.pct-a.pct)[0];
    return `<div class="simrow"><div style="min-width:0"><div class="row" style="gap:8px"><b>${esc(s.ia?s.cargo:(s.orgao_curto||s.orgao)+' · '+s.ano)}</b><span class="chip ${s.ia?'ia':''}">${s.banca} · ${s.formato==='CE'?'Certo ou Errado':'A–E'}</span>${s.antiga?'<span class="chip warn">lei da época</span>':''}</div><div class="note">${s.ia?'Questões inéditas (IA)':esc(s.cargo)} · ${n} ${s.formato==='CE'?'itens':'questões'} · ${mins} min${best?` · melhor resultado <b>${best.pct}%</b>`:''}</div></div><button class="btn ${s.ia?'':'pri'} sm" data-sim="${s.id}" data-min="${mins}">Começar</button></div>`}).join('')}</div>`}).join('')}
  <div class="panel"><h3>Como a nota é calculada</h3><p class="note">Cebraspe: na maioria dos editais, cada item errado anula um certo, e o item em branco vale zero. Por isso o simulado mostra a nota líquida (certos menos errados) e ensina quando vale deixar em branco. FGV e FCC: contam só os acertos, então nunca deixe em branco. Confira sempre a regra do edital do seu concurso.</p></div>
  ${S.sims.length?`<div class="panel"><h3>Histórico</h3><div class="tw"><table><thead><tr><th>Data</th><th>Prova</th><th class="num">Resultado</th></tr></thead><tbody>${S.sims.slice().reverse().map(x=>`<tr><td>${x.d}</td><td>${x.label?esc(x.label):SRC[x.src]?esc(srcLabel(SRC[x.src]))+' – '+esc(SRC[x.src].cargo):'Simulado'}</td><td class="num">${x.pct}% ${x.liq!=null?'· líquida '+x.liq:''}</td></tr>`).join('')}</tbody></table></div></div>`:''}`;
};
V.simulado.after=()=>{
  document.querySelectorAll('[data-sim]').forEach(b=>b.onclick=()=>{ const s=SRC[b.dataset.sim]; SIM={src:b.dataset.sim,ids:Q.filter(q=>q.src===b.dataset.sim).map(q=>q.id),resp:{},i:0,end:Date.now()+b.dataset.min*60000,done:false,title:(s.ia?s.cargo:s.orgao+' '+s.ano),sub:s.cargo+' · '+s.banca,ce:s.formato==='CE'}; render(); window.scrollTo({top:0}); });
  if(!SIM) wireCustomSim();
  if(SIM&&!SIM.done) simWire();
  if(SIM&&SIM.done){ const b=$('#simBack'); if(b) b.onclick=()=>{SIM=null;render()} }
};
let simTick;
function simRun(){
  const q=QBY[SIM.ids[SIM.i]];
  const prev=SIM.i>0?QBY[SIM.ids[SIM.i-1]]:null;
  return `<div class="row between"><div><h1>${esc(SIM.title)}</h1><p class="sub">${esc(SIM.sub)}</p></div><div class="timer" id="simTimer">--:--</div></div>
  <section class="panel" style="display:flex;flex-direction:column;gap:14px">${metaHTML(q)}${q.text&&(!prev||prev.text!==q.text)?supportHTML(q.text):q.text?`<details><summary>Ver texto de apoio</summary>${supportHTML(q.text)}</details>`:''}${q.cmd?`<div class="cmd">${esc(q.cmd)}</div>`:''}<div class="stem">${esc(q.stem)}</div>
  ${q.fmt==='CE'?`<div class="ce">${['C','E'].map(c=>`<button class="opt ${SIM.resp[q.id]===c?'sel':''}" data-r="${c}"><span class="bub">${c}</span>${c==='C'?'Certo':'Errado'}</button>`).join('')}</div><button class="btn sm" data-r="" style="align-self:flex-start">Deixar em branco</button>`
   :`<div class="opts">${q.opts.map((o,i)=>{const L='ABCDE'[i];return `<button class="opt ${SIM.resp[q.id]===L?'sel':''}" data-r="${L}"><span class="bub">${L}</span><span>${esc(o)}</span></button>`}).join('')}</div>`}
  <div class="row between"><button class="btn" id="sPrev" ${SIM.i?'':'disabled'}>Anterior</button><span class="note">${SIM.i+1} de ${SIM.ids.length}</span><button class="btn pri" id="sNext">${SIM.i===SIM.ids.length-1?'Revisar e entregar':'Próxima'}</button></div></section>
  <div class="panel"><h3>Folha de respostas</h3><div class="sheet" style="margin-top:10px">${SIM.ids.map((id,i)=>`<button data-go="${i}" class="${SIM.resp[id]?'done':''} ${i===SIM.i?'cur':''}" aria-label="Ir para ${QBY[id].n}">${QBY[id].n}${SIM.resp[id]?'·'+SIM.resp[id]:''}</button>`).join('')}</div>
  <div class="row" style="margin-top:12px"><button class="btn pri" id="sFinish">Entregar prova</button><button class="btn" id="sQuit">Sair sem salvar</button></div></div>`;
}
function simWire(){
  document.querySelectorAll('[data-r]').forEach(b=>b.onclick=()=>{ const id=SIM.ids[SIM.i]; if(b.dataset.r) SIM.resp[id]=b.dataset.r; else delete SIM.resp[id]; if(SIM.i<SIM.ids.length-1) SIM.i++; render(); });
  document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{SIM.i=+b.dataset.go;render()});
  $('#sPrev').onclick=()=>{SIM.i--;render()};
  $('#sNext').onclick=()=>{ if(SIM.i<SIM.ids.length-1){SIM.i++;render()} else document.querySelector('.sheet').scrollIntoView({behavior:'smooth'}) };
  $('#sFinish').onclick=finishSim; $('#sQuit').onclick=()=>{SIM=null;render()};
  clearInterval(simTick);
  const tick=()=>{ const el=$('#simTimer'); if(!el||!SIM||SIM.done){clearInterval(simTick);return} const ms=SIM.end-Date.now(); if(ms<=0){finishSim();return} const m=Math.floor(ms/60000),s=Math.floor(ms%60000/1000); el.textContent=String(m).padStart(2,'0')+':'+String(s).padStart(2,'0'); el.style.color=ms<300000?'var(--bad)':''; };
  tick(); simTick=setInterval(tick,1000);
}
function finishSim(){
  clearInterval(simTick);
  let c=0,e=0,b=0; const byD={};
  SIM.ids.forEach(id=>{ const q=QBY[id]; if(q.anulada) return; const r=SIM.resp[id]; byD[q.disc]=byD[q.disc]||{c:0,e:0,b:0};
    if(!r){b++;byD[q.disc].b++;return}
    const ok=r===q.ans; ok?(c++,byD[q.disc].c++):(e++,byD[q.disc].e++);
    const a=S.ans[q.id]||{n:0,hits:0,hist:[]}; a.n++; if(ok)a.hits++; a.ok=ok; a.last=r; a.d=today(); a.hist.push([today(),ok?1:0]); S.ans[q.id]=a; schedule(S.srs,q.id,ok);
  });
  const valid=c+e+b, pct=valid?Math.round(100*c/valid):0, liq=SIM.ce?c-e:null;
  SIM.done=true; SIM.res={c,e,b,pct,liq,byD,valid};
  S.sims.push({src:SIM.src,d:today(),pct,liq,label:SIM.src==='custom'?SIM.title:undefined}); activity(c+e); gain(50+c*2,'Simulado entregue: +'+(50+c*2)+' XP'); persist(); render();
}
function simResult(){
  const r=SIM.res;
  return `<div><h1>Resultado do simulado</h1><p class="sub">${esc(SIM.title)} · ${esc(SIM.sub)}</p></div>
  <div class="grid g4"><div class="panel stat"><span>Acertos</span><b style="color:var(--ok)">${r.c}</b></div><div class="panel stat"><span>Erros</span><b style="color:var(--bad)">${r.e}</b></div><div class="panel stat"><span>Em branco</span><b>${r.b}</b></div><div class="panel stat"><span>${r.liq!=null?'Nota líquida (C − E)':'Aproveitamento'}</span><b>${r.liq!=null?r.liq+' / '+r.valid:r.pct+'%'}</b></div></div>
  ${r.liq!=null?`<div class="panel note">No Cebraspe, ${r.e} erro${r.e===1?'':'s'} anularam ${r.e} acerto${r.e===1?'':'s'}. Se você tivesse deixado em branco os itens em que estava em dúvida, a nota líquida poderia subir. Treine marcar só quando tiver segurança.</div>`:''}
  <div class="panel"><h3>Por matéria</h3><div class="tw"><table><thead><tr><th>Matéria</th><th class="num">Certos</th><th class="num">Errados</th><th class="num">Branco</th><th style="width:30%">Aproveitamento</th></tr></thead><tbody>${Object.entries(r.byD).map(([d,x])=>{const t=x.c+x.e+x.b,p=t?Math.round(100*x.c/t):0;return `<tr><td>${esc(d)}</td><td class="num">${x.c}</td><td class="num">${x.e}</td><td class="num">${x.b}</td><td><div class="bar ${p>=70?'ok':p>=50?'warn':'bad'}"><i style="width:${p}%"></i></div></td></tr>`}).join('')}</tbody></table></div></div>
  <div class="row"><a class="btn pri" href="#revisao" style="text-decoration:none">Ver comentários no caderno de erros</a><button class="btn" id="simBack">Voltar aos simulados</button></div>`;
}

/* Flashcards */
const CARDS=[
 ['Prazo de prescrição da ação disciplinar (Lei 8.112): advertência, suspensão e demissão?','180 dias; 2 anos; 5 anos. Conta da data em que o fato se tornou conhecido (art. 142).'],
 ['Lei 9.784: o que NÃO pode ser delegado?','Atos de caráter normativo, decisão de recursos administrativos e matérias de competência exclusiva (art. 13).'],
 ['Recurso contra indeferimento de suspeição (Lei 9.784) tem efeito suspensivo?','Não. Cabe recurso sem efeito suspensivo (art. 21).'],
 ['Impedimento e suspeição na Lei 9.784 alcançam parentes até qual grau?','Até o 3º grau (arts. 18 e 20). Primo é 4º grau: não alcança.'],
 ['Servidor federal pode ser sócio de empresa privada?','Pode ser acionista, cotista ou comanditário. Não pode gerenciar ou administrar nem exercer o comércio (art. 117, X).'],
 ['Improbidade por violação a princípios (art. 11) depois da Lei 14.230/2021: exige o quê?','Dolo com fim de obter proveito ou benefício indevido. O rol do art. 11 passou a ser taxativo.'],
 ['Lei Anticorrupção: fusão, cisão ou incorporação extinguem a responsabilidade da empresa?','Não. A responsabilidade subsiste (Lei 12.846, art. 4º).'],
 ['Qual pena a Comissão de Ética (Decreto 1.171) pode aplicar?','Somente a censura, por parecer assinado por todos os integrantes.'],
 ['Poder de polícia: quais fases podem ser delegadas a estatal (STF, Tema 532)?','Consentimento, fiscalização e sanção, por lei, a estatal de capital majoritariamente público em regime não concorrencial. A ordem de polícia é indelegável.'],
 ['Registro de preços (Lei 14.133): modalidades e critérios?','Concorrência ou pregão; menor preço ou maior desconto.'],
 ['Credenciamento x pré-qualificação (Lei 14.133)','Credenciamento: chamamento para credenciar todos os aptos. Pré-qualificação: procedimento prévio para analisar habilitação ou objetos.'],
 ['Matriz de riscos é obrigatória quando?','Nas contratações integradas e semi-integradas (e nas obras e serviços de grande vulto) — art. 22, § 3º.'],
 ['LAI: o cidadão precisa justificar o pedido de informação?','Não. São vedadas exigências sobre os motivos (art. 10, § 3º).'],
 ['LGPD: dado anonimizado é dado pessoal?','Não, salvo se a anonimização puder ser revertida (art. 12).'],
 ['Fundamentos da República (CF, art. 1º) — mnemônico','SO-CI-DI-VA-PLU: soberania, cidadania, dignidade, valores sociais do trabalho e da livre iniciativa, pluralismo político.'],
 ['Projeto de lei de iniciativa do STF ou tribunais superiores começa em qual Casa?','Na Câmara dos Deputados (CF, art. 64).'],
 ['Competência remanescente (residual) na Federação é de quem?','Dos Estados (CF, art. 25, § 1º).'],
 ['Liberdade de profissão (art. 5º, XIII) é norma de eficácia…','Contida: aplicação imediata, mas a lei pode restringir.'],
 ['Renúncia à nacionalidade brasileira impede readquiri-la?','Não, desde a EC 131/2023 (art. 12, § 5º).'],
 ['Quem julga as revisões criminais e rescisórias de julgados do TRF?','O próprio TRF (CF, art. 108, I, “b”).'],
 ['Gás canalizado: competência de qual ente?','Dos Estados (CF, art. 25, § 2º).'],
 ['Teto remuneratório alcança estatais quando?','Quando recebem recursos do ente para pessoal ou custeio em geral (CF, art. 37, § 9º).'],
 ['Níveis da cultura organizacional (Schein), do mais visível ao mais profundo','Artefatos, valores declarados e pressupostos básicos.'],
 ['Racionalidade limitada (Simon): o decisor busca a solução…','Satisfatória, e não a ótima.'],
 ['Projeto x operação','Projeto é temporário e tem resultado único; operação é contínua e repetitiva.'],
 ['Ponto de pedido: fórmula','PP = consumo médio × tempo de reposição + estoque de segurança.'],
 ['Curva ABC: o que é a classe A?','Poucos itens de alto valor e controle rigoroso. A classe C reúne muitos itens de baixo valor.'],
 ['Inventário geral x rotativo','Geral: anual, com paralisação. Rotativo: ao longo do ano, sem parar o setor.'],
 ['Funções do Estado (Musgrave)','Alocativa, distributiva e estabilizadora.'],
 ['Resultado primário x nominal','Primário exclui juros; nominal inclui juros.'],
 ['Créditos extraordinários servem para quê?','Despesas imprevisíveis e urgentes: guerra, comoção interna ou calamidade pública.'],
 ['PPA (CF, art. 165, § 1º) abrange quais despesas?','Despesas de capital, as delas decorrentes e as de programas de duração continuada.'],
 ['Tributos sobre consumo são progressivos ou regressivos?','Regressivos: pesam mais na renda dos mais pobres.'],
 ['Falácia da afirmação do consequente','Se P então Q; Q; logo P. É inválida.'],
 ['Negação de “Todos têm mais de 25 anos”','Pelo menos um tem 25 anos ou menos.'],
 ['Equivalente de “Se P, então Q” (contrapositiva)','Se não Q, então não P.'],
 ['Intervenção na concessão (Lei 8.987): prazos','Procedimento instaurado em 30 dias e concluído em até 180 dias.'],
 ['Etapas da Análise de Impacto Regulatório (resumo)','Problema, atores e base legal, objetivos, alternativas, impactos, escolha, implementação e monitoramento.'],
];
let FC=null;
V.flashcards=()=>{
  const due=CARDS.map((c,i)=>i).filter(i=>!S.cards[i]||S.cards[i].due<=today());
  if(!FC) FC={queue:due,i:0,flip:false};
  const i=FC.queue[FC.i];
  const learned=Object.values(S.cards).filter(c=>c.step>=2).length;
  return `<div><h1>Flashcards</h1><p class="sub">Fatos que as bancas mais cobram nestas provas. Vire a carta, diga se lembrou e o sistema agenda a próxima revisão.</p></div>
  <div class="grid g3"><div class="panel stat"><span>Para hoje</span><b>${FC.queue.length-FC.i}</b></div><div class="panel stat"><span>Dominados</span><b>${learned}/${CARDS.length}</b></div><div class="panel stat"><span>Total</span><b>${CARDS.length}</b></div></div>
  ${i==null?'<div class="panel empty">Nenhum cartão para hoje. Volte amanhã.</div>':`
  <div class="panel card3d"><div>${esc(CARDS[i][0])}</div>${FC.flip?`<div class="back">${esc(CARDS[i][1])}</div>`:''}</div>
  <div class="row" style="justify-content:center">${FC.flip?`<button class="btn" data-fc="0">Não lembrei</button><button class="btn pri" data-fc="1">Lembrei</button>`:`<button class="btn pri" id="fcFlip">Mostrar resposta</button>`}</div>`}`;
};
V.flashcards.after=()=>{
  const f=$('#fcFlip'); if(f) f.onclick=()=>{FC.flip=true;render()};
  document.querySelectorAll('[data-fc]').forEach(b=>b.onclick=()=>{ const i=FC.queue[FC.i], ok=b.dataset.fc==='1'; schedule(S.cards,i,ok); if(!ok) FC.queue.push(i); FC.i++; FC.flip=false; activity(); gain(ok?5:2); persist(); render(); });
};

/* Estatísticas */
V.estatisticas=()=>{
  const rows=DISCS.map(d=>({d,...discStats(d),tot:REAL.filter(q=>q.disc===d&&!q.anulada).length})).filter(r=>r.tot).sort((a,b)=>b.n-a.n||b.tot-a.tot);
  const tipoRows=TIPOS.filter(([k])=>k!=='ia').map(([k,nome])=>({nome,...statsWhere(q=>!q.ia&&SRC[q.src].tipo===k),tot:REAL.filter(q=>SRC[q.src].tipo===k).length})), iaS=statsWhere(q=>q.ia);
  const days=[...Array(14)].map((_,i)=>addDays(today(),i-13)); const mx=Math.max(5,...days.map(d=>S.days[d]||0));
  const W=560,H=150,bw=W/14;
  const bancas=[...new Set(Object.values(SRC).filter(s=>!s.ia).map(s=>s.banca))];
  return `<div><h1>Desempenho</h1><p class="sub">Seu acerto por tipo de prova, banca e matéria. Só entram questões de provas reais; as inéditas (IA) aparecem à parte.</p></div>
  <div class="panel"><h3>Atividade nos últimos 14 dias</h3><div class="tw"><svg class="chart" viewBox="0 0 ${W} ${H+24}" style="width:100%;min-width:420px;max-width:${W}px" role="img" aria-label="Itens estudados por dia">
   <line x1="0" x2="${W}" y1="${H}" y2="${H}"/>${days.map((d,i)=>{const v=S.days[d]||0,h=v/mx*(H-20);return `<rect class="b" x="${i*bw+6}" y="${H-h}" width="${bw-12}" height="${h}" rx="3"/>${v?`<text x="${i*bw+bw/2}" y="${H-h-4}" text-anchor="middle">${v}</text>`:''}<text x="${i*bw+bw/2}" y="${H+15}" text-anchor="middle">${d.slice(8)}/${d.slice(5,7)}</text>`}).join('')}</svg></div></div>
  <div class="panel"><h3>Por tipo de prova</h3><div class="tw" style="margin-top:6px"><table><thead><tr><th>Tipo</th><th class="num">Resolvidas</th><th class="num">Acerto</th><th style="width:30%">Desempenho</th></tr></thead><tbody>${tipoRows.map(r=>`<tr><td>${esc(r.nome)}</td><td class="num">${r.n}/${r.tot}</td><td class="num">${r.n?r.pct+'%':'–'}</td><td><div class="bar ${!r.n?'':r.pct>=70?'ok':r.pct>=50?'warn':'bad'}"><i style="width:${r.n?r.pct:0}%"></i></div></td></tr>`).join('')}</tbody></table></div>
  <p class="note" style="margin-bottom:0">Inéditas (IA): ${iaS.n?`${iaS.pct}% de acerto em ${iaS.n} resolvidas`:'nenhuma resolvida ainda'}. Não somam ao seu acerto em provas reais.</p></div>
  <div class="panel"><h3>Por banca</h3><div class="grid g4" style="margin-top:10px">${bancas.map(b=>{const r=discStats('',b);return `<div class="stat"><span>${b}</span><b>${r.n?r.pct+'%':'–'}</b><span style="text-transform:none;letter-spacing:0">${r.h} de ${r.n} resolvidas</span></div>`}).join('')}</div></div>
  <div class="panel"><h3>Por matéria</h3><div class="tw"><table><thead><tr><th>Matéria</th><th class="num">Resolvidas</th><th class="num">Acerto</th><th style="width:34%">Desempenho</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.d)}</td><td class="num">${r.n}/${r.tot}</td><td class="num">${r.n?r.pct+'%':'–'}</td><td><div class="bar ${!r.n?'':r.pct>=70?'ok':r.pct>=50?'warn':'bad'}"><i style="width:${r.n?r.pct:0}%"></i></div></td></tr>`).join('')}</tbody></table></div>
  <p class="note">Verde a partir de 70%, que é a faixa em que costuma estar a nota de corte das provas de analista.</p></div>
  <div class="panel row between"><span class="note">Quer recomeçar do zero? Isso apaga seu progresso neste navegador e na sua conta.</span><button class="btn sm" id="reset">Apagar progresso</button></div>`;
};
V.estatisticas.after=()=>{ const b=$('#reset'); b.onclick=()=>{ if(b.dataset.c){ S=BLANK(); persist(); toast('Progresso apagado'); render(); } else { b.dataset.c=1; b.textContent='Clique de novo para confirmar'; } } };

/* Concursos */
const CONC=[
 {c:'Analista Judiciário (TRFs, TRTs, TREs)',area:'Tribunais',sal:[13,15],bancas:'Cebraspe (TRF6 2024, TSE Unificado 2024), FGV, FCC',freq:'Alta: vários tribunais por ano',mat:'Português, Constitucional, Administrativo, legislação do órgão e, na área administrativa, AFO, Administração e Gestão de Materiais',rec:true,prova:'aj_adm'},
 {c:'Analista do MPU',area:'Ministério Público',sal:[13,15],bancas:'FGV (2025), Cebraspe (2018)',freq:'Irregular',mat:'Português, Sustentabilidade, Direitos Humanos, Administração Pública, legislação do MPU e específicas',rec:true,prova:'mpu'},
 {c:'Analista de Planejamento e Orçamento (APO)',area:'Gestão federal',sal:[20,22],bancas:'CNU, aplicado pela Cesgranrio',freq:'Pelo CNU',mat:'AFO, Economia, Administração Pública, Constitucional',rec:true,prova:'cnu_gestao'},
 {c:'Especialista em Políticas Públicas e Gestão Governamental (EPPGG)',area:'Gestão federal',sal:[20,22],bancas:'CNU, aplicado pela Cesgranrio',freq:'Pelo CNU',mat:'Políticas públicas, Administração Pública, Economia, Constitucional',rec:true,prova:'cnu_gestao'},
 {c:'Especialista em Regulação (agências)',area:'Agências reguladoras',sal:[16,19],bancas:'Federais: Cebraspe ou CNU; estaduais: FGV (AGENERSA 2023)',freq:'Média',mat:'Regulação, Economia, Administrativo, Constitucional e a área técnica da agência',rec:true,prova:'regulacao'},
 {c:'Analista do Banco Central',area:'Controle e finanças',sal:[20,21],bancas:'Cebraspe (2024)',freq:'Baixa',mat:'Economia, Finanças, Contabilidade, Estatística, TI',rec:false},
 {c:'Auditor Federal de Controle Externo (TCU)',area:'Controle',sal:[22,26],bancas:'Varia (confira o último edital)',freq:'Baixa',mat:'Controle externo, AFO, Auditoria, Administrativo, Constitucional',rec:false},
 {c:'Auditor-Fiscal da Receita Federal',area:'Fiscal',sal:[21,23],bancas:'FGV (2022)',freq:'Baixa',mat:'Tributário, Contabilidade, Auditoria, Legislação tributária',rec:false},
 {c:'Analista Tributário da Receita Federal',area:'Fiscal',sal:[11,13],bancas:'FGV (2022)',freq:'Baixa',mat:'Tributário, Contabilidade, Legislação aduaneira',rec:false},
 {c:'Analista Legislativo (Câmara e Senado)',area:'Legislativo',sal:[20,30],bancas:'Varia (FGV, Cebraspe)',freq:'Baixa',mat:'Processo legislativo, Constitucional, Administrativo, área específica',rec:false},
];
let CF={min:8,soRec:false};
V.concursos=()=>{
  const list=CONC.filter(x=>x.sal[1]>=CF.min&&(!CF.soRec||x.rec));
  return `<div><h1>Concursos acima de R$ 8 mil</h1><p class="sub">Painel para escolher o alvo de longo prazo. Para os editais publicados agora, veja a aba <a href="#editais">Editais</a>. Os valores são faixas aproximadas de remuneração inicial: confira sempre o último edital antes de decidir.</p></div>
  <div class="panel row" style="gap:20px"><label class="f" style="flex:1;min-width:200px"><span>Remuneração mínima: R$ <span id="minv">${CF.min}</span> mil</span><input id="cmin" type="range" min="8" max="20" step="1" value="${CF.min}"></label><label class="row" style="gap:6px"><input type="checkbox" id="crec" ${CF.soRec?'checked':''}> Só os recomendados para você</label></div>
  <div class="grid g2">${list.map(x=>`<div class="panel" style="display:flex;flex-direction:column;gap:8px"><div class="row between"><span class="chip ghost">${esc(x.area)}</span>${x.rec?'<span class="chip ok">Recomendado para você</span>':''}</div><h3>${esc(x.c)}</h3><div class="stat"><span>Remuneração inicial aprox.</span><b style="font-size:20px">R$ ${x.sal[0]}–${x.sal[1]} mil</b></div><p class="note" style="margin:0"><b>Bancas recentes:</b> ${esc(x.bancas)}<br><b>Frequência:</b> ${esc(x.freq)}<br><b>Matérias-chave:</b> ${esc(x.mat)}</p>${x.prova?`<a class="btn sm" href="#questoes" data-src="${x.prova}" style="align-self:flex-start;text-decoration:none">Treinar com provas deste tipo</a>`:''}</div>`).join('')||'<div class="panel empty">Nenhum cargo nesta faixa.</div>'}</div>
  <p class="note">Recomendação baseada no seu perfil (Engenharia de Produção, pós em BI, meta acima de R$ 10 mil): tribunais e MPU como porta de entrada; APO, EPPGG e agências reguladoras como alvo principal, porque valorizam planejamento, orçamento e análise de dados.</p>`;
};
V.concursos.after=()=>{
  $('#cmin').oninput=e=>{CF.min=+e.target.value;$('#minv').textContent=CF.min}; $('#cmin').onchange=()=>render();
  $('#crec').onchange=e=>{CF.soRec=e.target.checked;render()};
  document.querySelectorAll('[data-src]').forEach(b=>b.onclick=()=>{qfSet({tipo:b.dataset.src})});
};


let EF={min:8,abertos:true};
const brl=v=>v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
const isoBR=s=>s.slice(8,10)+'/'+s.slice(5,7)+'/'+s.slice(0,4);
function edStatus(e){ const d=today(); if(d<e.ini) return ['warn','Abre em '+isoBR(e.ini)]; if(d>e.fim) return ['ghost','Inscrições encerradas']; const n=Math.round((new Date(e.fim+'T12:00:00')-new Date(d+'T12:00:00'))/864e5); return [n<=3?'bad':'ok', n===0?'Último dia de inscrição':'Inscrições abertas · '+(n===1?'falta 1 dia':'faltam '+n+' dias')]; }
V.editais=()=>{
  const list=EDITAIS.filter(e=>e.sal>=EF.min*1000&&(!EF.abertos||today()<=e.fim)).sort((a,b)=>a.fim.localeCompare(b.fim));
  return `<div><h1>Editais abertos</h1><p class="sub">Concursos com edital publicado e remuneração inicial a partir de R$ ${EF.min} mil. Cada dado foi conferido no edital ou na página oficial da banca em ${EDITAIS_DATA}. Antes de pagar a inscrição, confira sempre a página oficial, porque prazos podem ser prorrogados ou retificados.</p></div>
  <div class="panel row" style="gap:20px"><label class="f" style="flex:1;min-width:200px"><span>Remuneração mínima: R$ <span id="emv">${EF.min}</span> mil</span><input id="emin" type="range" min="8" max="30" step="1" value="${EF.min}"></label><label class="row" style="gap:6px"><input type="checkbox" id="eab" ${EF.abertos?'checked':''}> Só com inscrição aberta ou a abrir</label></div>
  ${list.map(e=>{const [k,st]=edStatus(e);return `<div class="panel" style="display:flex;flex-direction:column;gap:8px"><div class="row between"><div class="row" style="gap:8px"><h2>${esc(e.o)}</h2><span class="chip">${esc(e.b)}</span></div><span class="chip ${k}">${esc(st)}</span></div>
   <p style="margin:0">${esc(e.c)}</p>
   <div class="grid g4"><div class="stat"><span>Remuneração inicial</span><b style="font-size:18px">${esc(e.salT)}</b></div><div class="stat"><span>Vagas</span><b style="font-size:15px;font-family:var(--f-read);font-weight:500;letter-spacing:0">${esc(e.v)}</b></div><div class="stat"><span>Inscrições</span><b style="font-size:15px">${isoBR(e.ini)} a ${isoBR(e.fim)}</b></div><div class="stat"><span>Prova</span><b style="font-size:15px;font-family:var(--f-read);font-weight:500;letter-spacing:0">${esc(e.prova)}</b></div></div>
   <p class="note" style="margin:0">${esc(e.nota)}</p>
   <div class="row between"><span class="note">Fonte: ${esc(e.fonte)}</span><div class="row" style="gap:6px">${e.tipo?`<a class="btn sm" href="#questoes" data-et="${e.tipo}" style="text-decoration:none">Treinar com provas deste tipo</a>`:''}<a class="btn pri sm" href="${e.url}" target="_blank" rel="noopener" style="text-decoration:none">Página oficial</a></div></div></div>`}).join('')||'<div class="panel empty">Nenhum edital nesta faixa.</div>'}
  <p class="note">Esta lista só traz concursos com edital oficial publicado. Concursos apenas previstos ou autorizados não entram aqui. A lista foi montada em ${EDITAIS_DATA} e não se atualiza sozinha: peça uma nova conferência quando quiser.</p>`;
};
V.editais.after=()=>{
  $('#emin').oninput=e=>{EF.min=+e.target.value;$('#emv').textContent=EF.min}; $('#emin').onchange=()=>render();
  $('#eab').onchange=e=>{EF.abertos=e.target.checked;render()};
  document.querySelectorAll('[data-et]').forEach(b=>b.onclick=()=>qfSet({tipo:b.dataset.et}));
};

/* Bancas */
const BANCAS=[
 {b:'Cebraspe',f:'Certo ou Errado, em blocos de itens ligados a um comando',reg:'Na maioria dos editais, cada item errado anula um certo (nota líquida). Deixar em branco não desconta.',estilo:['Troca uma palavra da lei para tornar o item errado (“exceto” vira “inclusive”, “2 anos” vira “5 anos”).','Generalizações (“sempre”, “somente”, “necessariamente”) são suspeitas, mas não são erro automático.','Em português, cobra reescrita de trechos: verifique correção e manutenção do sentido ao mesmo tempo.','Cobra jurisprudência recente do STF e do STJ e alterações legislativas novas.'],dica:'Treine com nota líquida. Se a sua taxa de acerto em uma matéria estiver abaixo de 60%, deixar em branco nos itens de dúvida costuma render mais.',on:[]},
 {b:'FGV',f:'Múltipla escolha com 5 alternativas (A a E)',reg:'Conta apenas os acertos. Não há desconto por erro.',estilo:['Enunciados longos com casos práticos (“Maria, servidora do Estado Alfa…”).','Português com frases curtas e citações, cobrando lógica do texto, ambiguidade e estilo.','Direito com muita jurisprudência e temas de repercussão geral.','Raciocínio lógico com contas rápidas e lógica proposicional.'],dica:'Elimine alternativas: em casos práticos, ache primeiro o instituto jurídico do caso e só então leia as opções.',on:[]},
 {b:'Cesgranrio (CNU)',f:'Múltipla escolha com 5 alternativas',reg:'Conta os acertos. No CNU, provas por bloco temático, com conhecimentos gerais comuns e específicos do bloco.',estilo:['Questões mais diretas, com cobrança literal de conceitos.','Conhecimentos gerais com políticas públicas, desafios do Estado e diversidade.','Específicas por bloco, alinhadas aos cargos (APO e EPPGG estão no bloco de gestão).'],dica:'Estude pelo edital do bloco e resolva as provas do CNU 2024 e 2025 na íntegra. Aqui você já tem questões do Bloco 6 (Regulação) e do Bloco 7 (Gestão Governamental, onde estão APO/EPPGG-like).',on:[]},
 {b:'FCC',f:'Múltipla escolha com 5 alternativas',reg:'Conta os acertos. Não há desconto por erro.',estilo:['Muito apegada à letra da lei: troca prazos, números e palavras do artigo nas alternativas erradas.','Português com gramática clássica (crase, regência, concordância, pontuação) sobre textos jornalísticos.','Comandos curtos (“É correto afirmar…”, “NÃO é…”): leia o comando antes das alternativas.','Nos TRTs, cobra Direito e Processo do Trabalho com a letra da CLT.'],dica:'Lei seca e mais lei seca. As provas FCC daqui são de 2018 e 2019: confira mudanças posteriores na lei (Reforma da Previdência, Lei 14.133 e Lei 14.230).',on:[]},
 {b:'Vunesp',f:'Múltipla escolha com 5 alternativas',reg:'Conta os acertos.',estilo:['Forte nos tribunais de São Paulo (TJSP) e em prefeituras.','Português e interpretação com peso grande; direito cobrado de forma direta.'],dica:'Questões em breve: só vou incluir quando encontrar o gabarito definitivo oficial publicado pela banca.',on:[]},
];
function bancaStats(b){
  const qs=REAL.filter(q=>SRC[q.src].banca===b); if(!qs.length) return '<p class="note" style="margin:0">Ainda sem provas desta banca no banco de questões.</p>';
  const valid=qs.filter(q=>!q.anulada), an=qs.length-valid.length, ce=valid.filter(q=>q.fmt==='CE'), mc=valid.filter(q=>q.fmt==='MC');
  const dc={}; qs.forEach(q=>dc[q.disc]=(dc[q.disc]||0)+1); const top=Object.entries(dc).sort((a,c)=>c[1]-a[1]).slice(0,7), mx=top[0][1];
  const words=Math.round(qs.reduce((t,q)=>t+(q.stem+' '+(q.opts||[]).join(' ')).split(/\s+/).length,0)/qs.length);
  const provas=new Set(qs.map(q=>q.src)).size;
  let ans='';
  if(ce.length){ const c=ce.filter(q=>q.ans==='C').length; const pc=Math.round(100*c/ce.length); ans+=`<div><h3>Certo ou Errado</h3><div class="bar ok" style="margin-top:8px" role="img" aria-label="${pc}% certo"><i style="width:${pc}%"></i></div><p class="note" style="margin:6px 0 0">${pc}% dos itens são Certos e ${100-pc}% Errados (${ce.length} itens). Não chute sempre o mesmo lado: o equilíbrio é quase meio a meio.</p></div>`; }
  if(mc.length){ const L='ABCDE'.split('').map(l=>[l,mc.filter(q=>q.ans===l).length]); const m2=Math.max(...L.map(x=>x[1])); ans+=`<div><h3>Letra do gabarito</h3><div class="letters" style="margin-top:8px">${L.map(([l,n])=>`<div><span>${Math.round(100*n/mc.length)}%</span><i style="height:${Math.max(4,60*n/m2)}px"></i><b>${l}</b></div>`).join('')}</div><p class="note" style="margin:6px 0 0">Distribuição das respostas em ${mc.length} questões. Nenhuma letra domina, então "chutar sempre C" não funciona.</p></div>`; }
  return `<div class="panel" style="background:var(--bg);box-shadow:none;display:flex;flex-direction:column;gap:14px"><div class="row between"><h3>Raio-X nas questões deste banco</h3><span class="note">${qs.length} questões de ${provas} prova${provas>1?'s':''} · ${an} anulada${an===1?'':'s'} (${(100*an/qs.length).toFixed(1)}%) · enunciado médio de ${words} palavras</span></div>
   <div class="grid g2"><div><h3>Matérias que mais aparecem</h3><div class="bars" style="margin-top:8px">${top.map(([d,n])=>`<div class="l"><span title="${esc(d)}">${esc(d)}</span><div class="bar"><i style="width:${100*n/mx}%"></i></div><span>${Math.round(100*n/qs.length)}%</span></div>`).join('')}</div></div><div style="display:flex;flex-direction:column;gap:14px">${ans}</div></div>
   <p class="note" style="margin:0">Calculado só sobre as provas que estão aqui, não sobre toda a história da banca. As matérias das questões novas foram classificadas automaticamente.</p></div>`;
}
V.bancas=()=>`<div><h1>Perfil das bancas</h1><p class="sub">Como cada banca pensa, com um raio-X estatístico calculado sobre as provas reais deste banco.</p></div>
  ${BANCAS.map(x=>`<div class="panel" style="display:flex;flex-direction:column;gap:10px"><div class="row between"><h2>${x.b}</h2><span class="chip">${(n=>n?n+' questões na plataforma':'Questões em breve')(REAL.filter(q=>SRC[q.src].banca===x.b.split(' ')[0]).length)}</span></div>
  <div class="grid g2"><div><h3>Formato</h3><p class="note">${esc(x.f)}</p><h3>Pontuação</h3><p class="note">${esc(x.reg)}</p></div><div><h3>Estilo de cobrança</h3><ul class="note" style="padding-left:18px;margin:6px 0">${x.estilo.map(e=>`<li>${esc(e)}</li>`).join('')}</ul></div></div>
  ${bancaStats(x.b.split(' ')[0])}
  <p style="margin:0"><b>Estratégia:</b> ${esc(x.dica)}</p></div>`).join('')}
  <p class="note">Perfis montados a partir das provas públicas e da experiência geral com as bancas. Confira sempre a regra de pontuação no edital.</p>`;

/* Aulas */
const AULAS={
 'Língua Portuguesa':{q:['interpretação de texto Cebraspe','reescrita de frases Cebraspe','crase','concordância verbal'],leis:[]},
 'Raciocínio Lógico e Matemática':{q:['lógica proposicional equivalências','falácias argumentação Cebraspe','negação de proposições'],leis:[]},
 'Direito Administrativo':{q:['Lei 8.112 completa','Lei 9.784 processo administrativo','Lei 14.133 licitações','poder de polícia STF tema 532','LAI e LGPD'],leis:[['Lei 8.112/1990','leis/l8112cons.htm'],['Lei 9.784/1999','leis/l9784.htm'],['Lei 14.133/2021','_ato2019-2022/2021/lei/l14133.htm'],['LAI','_ato2011-2014/2011/lei/l12527.htm'],['LGPD','_ato2015-2018/2018/lei/l13709.htm']]},
 'Direito Constitucional':{q:['direitos fundamentais','organização do Estado competências','Poder Judiciário constituição','eficácia das normas constitucionais'],leis:[['Constituição Federal','constituicao/constituicao.htm']]},
 'Ética e Integridade':{q:['Lei de improbidade 14.230 alterações','Lei anticorrupção 12.846','Código de ética Decreto 1.171'],leis:[['Lei 8.429/1992','leis/l8429.htm'],['Lei 12.846/2013','_ato2011-2014/2013/lei/l12846.htm'],['Decreto 1.171/1994','decreto/d1171.htm']]},
 'AFO e Orçamento Público':{q:['AFO orçamento público PPA LDO LOA','princípios orçamentários','créditos adicionais'],leis:[['Lei 4.320/1964','leis/l4320.htm'],['LRF (LC 101/2000)','leis/lcp/lcp101.htm']]},
 'Administração Geral e Pública':{q:['cultura organizacional Schein','processo decisório Simon','gestão de projetos PMBOK'],leis:[]},
 'Gestão de Materiais e Logística':{q:['administração de materiais curva ABC','gestão de estoques ponto de pedido'],leis:[]},
 'Economia e Regulação':{q:['funções do Estado Musgrave','falhas de mercado','agências reguladoras regulação econômica','análise de impacto regulatório','concessões Lei 8.987'],leis:[['Lei 8.987/1995','leis/l8987cons.htm'],['Lei 11.445/2007 (saneamento)','_ato2007-2010/2007/lei/l11445.htm']]},
 'Direitos Humanos e Inclusão':{q:['Declaração Universal dos Direitos Humanos','Agenda 2030 ODS','Estatuto da Pessoa com Deficiência'],leis:[['Lei 13.146/2015','_ato2015-2018/2015/lei/l13146.htm']]},
 'Políticas Públicas':{q:['ciclo de políticas públicas','tipologia de Lowi políticas públicas','avaliação de políticas públicas'],leis:[]},
 'Tecnologia da Informação e Dados':{q:['business intelligence data warehouse','CRISP-DM','SQL para concursos','big data Hadoop'],leis:[]},
 'Estatística':{q:['estatística para concursos inferência','distribuição normal','amostragem estatística concurso'],leis:[]},
 'Contabilidade':{q:['contabilidade pública MCASP','PCASP','balanço patrimonial setor público'],leis:[]},
 'Direito Processual e Civil':{q:['processo civil CPC 2015 concurso','recursos no CPC'],leis:[['CPC (Lei 13.105/2015)','_ato2015-2018/2015/lei/l13105.htm']]},
 'Direito do Trabalho e Processual do Trabalho':{q:['direito do trabalho para tribunais','processo do trabalho recursos','reforma trabalhista Lei 13.467'],leis:[['CLT (Decreto-Lei 5.452/1943)','decreto-lei/del5452.htm']]},
 'Direito Penal e Processual Penal':{q:['crimes contra a administração pública','inquérito policial','prisão e liberdade provisória'],leis:[['Código Penal','decreto-lei/del2848compilado.htm'],['Código de Processo Penal','decreto-lei/del3689.htm']]},
 'Direito Previdenciário':{q:['regime geral de previdência social','reforma da previdência EC 103/2019','benefícios previdenciários'],leis:[['Lei 8.213/1991','leis/l8213cons.htm']]},
 'Gestão de Pessoas':{q:['gestão por competências','avaliação de desempenho','liderança e motivação'],leis:[]},
};
let AULA_OPEN='';
const cap=s=>s.charAt(0).toUpperCase()+s.slice(1);
function vidRow(topic){
  const v=VIDS[topic]; if(!v||!v.length) return `<div class="simrow"><div><b>${esc(cap(topic))}</b></div><a class="btn sm" href="${yt(topic)}" target="_blank" rel="noopener">Buscar no YouTube</a></div>`;
  const a=v[0], b=v[1], seen=(S.vid||{})[a.id]||(b&&(S.vid||{})[b.id]);
  return `<div class="simrow"><div style="min-width:0;display:flex;flex-direction:column;gap:3px"><span class="stat"><span>${esc(cap(topic))}</span></span>
    <a href="${ytw(a.id)}" target="_blank" rel="noopener" style="font-weight:600;text-decoration:none;color:var(--ink)">${esc(a.t)}</a>
    <span class="note">${esc(a.c)}${a.d?' · '+a.d:''}${b?` · reserva: <a href="${ytw(b.id)}" target="_blank" rel="noopener">${esc(b.t.length>60?b.t.slice(0,58)+'…':b.t)}</a> (${esc(b.c)}${b.d?', '+b.d:''})`:''}</span></div>
    <div class="row" style="gap:6px;justify-content:flex-end"><button class="btn pri sm" data-play="${a.id}">Assistir</button><button class="btn sm" data-seen="${a.id}" aria-pressed="${seen?'true':'false'}">${seen?'✓ Assistida':'Marcar assistida'}</button></div></div>`;
}
V.aulas=()=>{
  const all=Object.values(AULAS).flatMap(x=>x.q), done=all.filter(tp=>(VIDS[tp]||[]).some(v=>(S.vid||{})[v.id])).length;
  return `<div><h1>Aulas gratuitas</h1><p class="sub">Uma aula escolhida para cada assunto, de professores de cursinhos conhecidos, com um vídeo reserva. Os vídeos tocam aqui mesmo; o título abre no YouTube. Marque o que já assistiu e depois resolva as questões da matéria.</p></div>
  <div class="grid g3"><div class="panel stat"><span>Aulas assistidas</span><b>${done}/${all.length}</b><div class="bar" style="margin-top:6px"><i style="width:${Math.round(100*done/all.length)}%"></i></div></div>
  <div class="panel" style="grid-column:span 2;display:flex;flex-direction:column;gap:6px;justify-content:center"><h3>Cursos gratuitos da ENAP</h3><p class="note" style="margin:0">Administração pública, orçamento, licitações e ética, com certificado do governo federal.</p><a class="btn sm" href="https://www.escolavirtual.gov.br/catalogo" target="_blank" rel="noopener" style="text-decoration:none;align-self:flex-start">Abrir catálogo</a></div></div>
  ${Object.entries(AULAS).map(([d,x])=>{const n=REAL.filter(q=>q.disc===d).length, dd=x.q.filter(tp=>(VIDS[tp]||[]).some(v=>(S.vid||{})[v.id])).length;return `<details class="panel" data-dd="${esc(d)}" ${AULA_OPEN===d?'open':''}><summary class="row between" style="list-style:none"><span style="display:flex;flex-direction:column;gap:2px"><h3>${esc(d)}</h3><span class="note">${x.q.length} aula${x.q.length>1?'s':''} · ${dd} assistida${dd===1?'':'s'} · ${n} questões reais</span></span><span class="chip ghost">abrir</span></summary>
   <div style="margin-top:10px">${x.q.map(vidRow).join('')}</div>
   ${x.leis.length?`<div style="margin-top:10px"><div class="note">Lei seca oficial (Planalto)</div><div class="links" style="margin-top:4px">${x.leis.map(([l,u])=>`<a href="https://www.planalto.gov.br/ccivil_03/${u}" target="_blank" rel="noopener">${esc(l)}</a>`).join('')}</div></div>`:''}
   ${n?`<a class="btn sm" href="#questoes" data-d="${esc(d)}" style="margin-top:12px;display:inline-block;text-decoration:none">Resolver questões de ${esc(d)}</a>`:''}</details>`}).join('')}
  <p class="note">Cada vídeo foi conferido no YouTube em novembro de 2026 (existe e está público). Escolhi pelo professor, pela aderência ao assunto e pela atualização: em leis que mudaram (licitações, improbidade, previdência) priorizei aulas posteriores à mudança. Se um vídeo sair do ar, use a reserva.</p>`;
};
V.aulas.after=()=>{
  document.querySelectorAll('[data-d]').forEach(b=>b.onclick=()=>{qfSet({disc:b.dataset.d,origem:''})});
  document.querySelectorAll('details[data-dd]').forEach(el=>el.addEventListener('toggle',()=>{ if(el.open) AULA_OPEN=el.dataset.dd; }));
  document.querySelectorAll('[data-play]').forEach(b=>b.onclick=()=>{ const row=b.closest('.simrow'); const nx=row.nextElementSibling; if(nx&&nx.classList.contains('ytbox')){nx.remove();b.textContent='Assistir';return} const box=document.createElement('div'); box.className='ytbox'; box.style.cssText='position:relative;width:100%;max-width:100%;aspect-ratio:16/9;margin:6px 0 12px'; box.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+encodeURIComponent(b.dataset.play)+'?rel=0" title="Aula" style="position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:8px" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>'; row.after(box); b.textContent='Fechar'; });
  document.querySelectorAll('[data-seen]').forEach(b=>b.onclick=()=>{ S.vid=S.vid||{}; const id=b.dataset.seen; if(S.vid[id]) delete S.vid[id]; else { S.vid[id]=today(); activity(); gain(5,'Aula marcada como assistida · +5 XP'); } persist(); AULA_OPEN=b.closest('details').dataset.dd; render(); });
};

/* Plano */
const ALVOS={
 tribunal:{n:'Analista Judiciário (tribunais)',w:[['Língua Portuguesa',3],['Direito Constitucional',3],['Direito Administrativo',3],['AFO e Orçamento Público',2],['Administração Geral e Pública',2],['Raciocínio Lógico e Matemática',1],['Ética e Integridade',1],['Gestão de Materiais e Logística',1]]},
 gestao:{n:'APO e EPPGG (CNU)',w:[['AFO e Orçamento Público',3],['Economia e Regulação',3],['Políticas Públicas',2],['Administração Geral e Pública',2],['Direito Constitucional',2],['Direito Administrativo',2],['Língua Portuguesa',2],['Raciocínio Lógico e Matemática',1]]},
 agencia:{n:'Agências reguladoras',w:[['Economia e Regulação',4],['Direito Administrativo',3],['Direito Constitucional',2],['Língua Portuguesa',2],['Raciocínio Lógico e Matemática',1],['Ética e Integridade',1]]},
};
function adapt(d,w){ const st=discStats(d); let f=1, why='Peso do edital; ainda sem dados suficientes, então vale o peso padrão.';
  if(st.n>=6){ if(st.pct<50){f=1.6;why='Seu acerto está em '+st.pct+'%: o plano aumentou o tempo desta matéria.'} else if(st.pct<70){f=1.25;why='Acerto de '+st.pct+'%, abaixo da meta de 70%: tempo um pouco maior.'} else if(st.pct>=85&&st.n>=15){f=.75;why='Acerto de '+st.pct+'%: a matéria está madura, o plano reduziu o tempo.'} else why='Acerto de '+st.pct+'%, dentro da meta: mantém o peso.'; }
  return {d,w,f,adj:w*f,st,why}; }
function planRows(){ const A=ALVOS[S.plan.alvo]||ALVOS.tribunal; return A.w.map(([d,w])=>adapt(d,w)).map(r=>({...r,need:r.adj*(r.st.n?(1-r.st.pct/100)+0.3:1.3)/(1+(dayRec().disc[r.d]||0)/8)})).sort((a,b)=>b.need-a.need); }
V.plano=()=>{
  const A=ALVOS[S.plan.alvo]||ALVOS.tribunal, H=S.plan.horas;
  const study=H*0.75, rev=H*0.25, R0=A.w.map(([d,w])=>adapt(d,w)), tot=R0.reduce((s,x)=>s+x.adj,0);
  const rows=R0.map(r=>{ const h=study*r.adj/tot; return {...r,h,blocks:Math.max(1,Math.round(h*60/50))}; });
  return `<div><h1>Plano de estudos</h1><p class="sub">Ciclo de estudos semanal com pesos do edital, blocos de 50 minutos e 25% do tempo para revisão. Os pesos se ajustam sozinhos ao seu desempenho.</p></div>
  <div class="panel grid g2"><label class="f">Alvo<select id="pAlvo">${Object.entries(ALVOS).map(([k,x])=>`<option value="${k}" ${k===S.plan.alvo?'selected':''}>${x.n}</option>`).join('')}</select></label>
  <label class="f">Horas por semana<input type="number" id="pHoras" min="3" max="60" value="${H}"></label></div>
  <div class="panel"><div class="row between"><h3>Seu ciclo semanal</h3><span class="note">${(study).toFixed(1)} h de teoria e questões + ${rev.toFixed(1)} h de revisão</span></div>
   <div class="tw" style="margin-top:8px"><table class="plan"><thead><tr><th>Matéria</th><th class="num">Horas/semana</th><th class="num">Blocos de 50 min</th><th>Seu acerto</th><th>Ajuste automático</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.d)}</td><td class="num">${r.h.toFixed(1)}</td><td class="num">${r.blocks}</td><td>${r.st.n?r.st.pct+'% ('+r.st.n+')':'<span class="note">sem dados</span>'}</td><td>${r.f>1?'<span class="chip bad">+'+Math.round((r.f-1)*100)+'%</span>':r.f<1?'<span class="chip ok">'+Math.round((r.f-1)*100)+'%</span>':'<span class="chip ghost">padrão</span>'}</td></tr>`).join('')}<tr><td><b>Revisão espaçada + flashcards</b></td><td class="num">${rev.toFixed(1)}</td><td class="num">${Math.max(1,Math.round(rev*60/50))}</td><td></td></tr></tbody></table></div></div>
  <div class="panel"><h3>Como usar o ciclo</h3><ol class="note" style="padding-left:18px;margin:8px 0 0;display:flex;flex-direction:column;gap:4px">
   <li>Siga a lista de cima para baixo. Ao terminar a última matéria, recomece o ciclo, sem se prender a dias da semana.</li>
   <li>Em cada bloco: 20 min de teoria (aula ou PDF), 25 min de questões da matéria aqui e 5 min anotando os erros.</li>
   <li>Todo dia, antes de começar, faça a fila de revisão e os flashcards do dia (10 a 15 min).</li>
   <li>O plano é adaptativo: com 6 ou mais questões numa matéria, ele aumenta o tempo onde seu acerto está abaixo de 70% e reduz onde passa de 85%.</li>
   <li>A cada 4 semanas, faça um simulado completo para medir a evolução.</li></ol></div>`;
};
V.plano.after=()=>{ $('#pAlvo').onchange=e=>{S.plan.alvo=e.target.value;persist();render()}; $('#pHoras').onchange=e=>{S.plan.horas=Math.max(3,Math.min(60,+e.target.value||15));persist();render()}; };


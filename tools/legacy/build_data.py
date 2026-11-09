import json, re, sys
sys.path.insert(0, '/tmp/claude-0/-home-user/478c6bdf-f475-5683-bd52-c80df6bd2f12/scratchpad/tools')
from comments import CE, MC
D='/tmp/claude-0/-home-user/478c6bdf-f475-5683-bd52-c80df6bd2f12/scratchpad/dl/'
P='https://www.planalto.gov.br/ccivil_03/'
CEB_TOP=[(1,14,'Língua Portuguesa','Interpretação e gramática',None),
 (15,18,'Direito Administrativo','Lei 8.112/1990 e Lei 9.784/1999',None),
 (19,22,'Ética e Integridade','Improbidade, Anticorrupção e Código de Ética',None),
 (23,30,'Raciocínio Lógico','Argumentação e falácias',None),
 (31,35,'Direitos Humanos','Direitos fundamentais, DUDH e Agenda 2030',None),
 (36,40,'Direitos da Pessoa com Deficiência','Estatuto da PcD e acessibilidade',None),
 (41,50,'Regimento Interno (TRF6)','Regimento Interno do TRF da 6ª Região',None),
 (51,54,'Direito Administrativo','Licitações (Lei 14.133/2021)',None),
 (55,58,'Direito Administrativo','Organização, poderes e agentes',None),
 (59,62,'Direito Administrativo','LAI e LGPD',None),
 (63,74,'Direito Constitucional','Constituição Federal',None),
 (75,86,'Administração Geral','Gestão, decisão, processos e projetos',None),
 (87,98,'Administração de Materiais','Estoques, compras e patrimônio',None),
 (99,110,'AFO','Orçamento público',None),
 (111,120,'Economia do Setor Público','Finanças públicas',None)]
FGV_TOP=[(1,10,'Língua Portuguesa','Interpretação e estilo'),(11,20,'Raciocínio Lógico','Lógica e matemática'),
 (21,25,'Direito Administrativo','Atos, poder de polícia, licitações'),(26,30,'Direito Constitucional','Constituição Federal'),
 (31,35,'Regulação','Concessões, saneamento e agências'),(36,40,'Ética e Integridade','Processo, improbidade e disciplina'),
 (41,46,'Economia e Regulação','Regulação econômica e AIR')]
LAW={15:'leis/l9784.htm',16:'leis/l8112cons.htm',17:'leis/l9784.htm',18:'leis/l8112cons.htm',19:'leis/l8429.htm',20:'_ato2011-2014/2013/lei/l12846.htm',21:'decreto/d1171.htm',22:'leis/l8429.htm',36:'_ato2015-2018/2015/lei/l13146.htm',37:'_ato2015-2018/2015/lei/l13146.htm',38:'leis/l10048.htm',39:'leis/l10098.htm',40:'_ato2015-2018/2015/lei/l13146.htm',
 51:'_ato2019-2022/2021/lei/l14133.htm',52:'_ato2019-2022/2021/lei/l14133.htm',53:'_ato2019-2022/2021/lei/l14133.htm',54:'_ato2019-2022/2021/lei/l14133.htm',56:'_ato2004-2006/2005/lei/l11107.htm',59:'_ato2015-2018/2018/lei/l13709.htm',60:'_ato2015-2018/2018/lei/l13709.htm',61:'_ato2011-2014/2011/lei/l12527.htm',62:'_ato2011-2014/2011/lei/l12527.htm',103:'leis/lcp/lcp101.htm',105:'leis/lcp/lcp101.htm',109:'leis/l4320.htm'}
for n in range(63,75): LAW[n]='constituicao/constituicao.htm'
for n in (104,106): LAW[n]='constituicao/constituicao.htm'
FLAW={21:'constituicao/constituicao.htm',25:'_ato2019-2022/2021/lei/l14133.htm',26:'constituicao/constituicao.htm',27:'constituicao/constituicao.htm',28:'constituicao/constituicao.htm',29:'constituicao/constituicao.htm',31:'leis/l8987cons.htm',34:'_ato2007-2010/2007/lei/l11445.htm',36:'leis/l9784.htm',37:'leis/l8429.htm',39:'leis/l8112cons.htm'}
def top(tab,n):
    for t in tab:
        if t[0]<=n<=t[1]: return t[2],t[3]
from cleanfn import clean
srcs={
 'trf6cg':{'id':'trf6cg','banca':'Cebraspe','orgao':'TRF da 6ª Região','ano':2025,'cargo':'Analista Judiciário (Conhecimentos Gerais)','formato':'CE',
   'prova':'https://cdn.cebraspe.org.br/concursos/TRF6_24/arquivos/034_TRF6_CG1_01.PDF','gabarito':'https://cdn.cebraspe.org.br/concursos/TRF6_24/arquivos/Gab_Definitivo_034_TRF6_CG1_01.PDF'},
 'trf6aj':{'id':'trf6aj','banca':'Cebraspe','orgao':'TRF da 6ª Região','ano':2025,'cargo':'Analista Judiciário – Área Administrativa','formato':'CE',
   'prova':'https://cdn.cebraspe.org.br/concursos/TRF6_24/arquivos/034_TRF6_001_01.PDF','gabarito':'https://cdn.cebraspe.org.br/concursos/TRF6_24/arquivos/Gab_Definitivo_034_TRF6_001_01.PDF'},
 'agenersa':{'id':'agenersa','banca':'FGV','orgao':'AGENERSA (agência reguladora do RJ)','ano':2023,'cargo':'Especialista em Regulação','formato':'MC',
   'prova':'https://conhecimento.fgv.br/sites/default/files/concursos/cns002-especialista-em-regulacaocns002-tipo-1.pdf','gabarito':'https://conhecimento.fgv.br/sites/default/files/concursos/agenersa-gabaritos-definitivos.pdf'}}
just='https://cdn.cebraspe.org.br/concursos/TRF6_24/arquivos/TRF6_24_JUSTIFICATIVAS_DE_ALTERAES_DE_GABARITO.PDF'
qs=[]; texts={}
def ctxclean(c):
    c=c.split('rascunho.')[-1]
    for k in ['De acordo com o Plano']:
        if k in c and 'mando que' in c: c=c[c.index(k):]
    c=re.sub(r'^.*?OS ESPECÍFICOS --\s*','',c,flags=re.S)
    # split support text from command: command starts at last paragraph containing 'julgue'
    paras=[p.strip() for p in re.split(r'\n\s*\n',c) if p.strip()]
    return paras
for f,sid in (('cg1.json','trf6cg'),('e001.json','trf6aj')):
    for it in json.load(open(D+f)):
        n=it['n']; paras=ctxclean(it['ctx'])
        cmd=re.sub(r'\s+',' ',paras[-1]) if paras else ''
        txt=None
        if len(paras)>1:
            body='\n\n'.join(paras[:-1]); body=re.sub(r'\n[ \t]{4,}','\n\n',body); body=re.sub(r'(?<!\n)\n(?!\n)',' ',body); body=re.sub(r'[ \t]+',' ',body).strip()
            key=sid+'-t'+str(len(texts)); 
            found=[k for k,v in texts.items() if v==body]
            if found: key=found[0]
            else: texts[key]=body
            txt=key
        d,a=top(CEB_TOP,n)
        q={'id':f'{sid}-{n}','src':sid,'n':n,'fmt':'CE','disc':d,'tema':a,'cmd':cmd,'text':txt,'stem':it['text'],
           'ans':None if it['gab']=='X' else it['gab'],'anulada':it['gab']=='X','com':CE[n]}
        if n in LAW: q['lei']=P+LAW[n]
        if q['anulada']: q['just']=just
        qs.append(q)
for it in json.load(open(D+'fgv.json')):
    n=it['n']
    if n>46 or n==15: continue
    d,a=top(FGV_TOP,n)
    q={'id':f'agenersa-{n}','src':'agenersa','n':n,'fmt':'MC','disc':d,'tema':a,'stem':clean(it['stem']),'opts':[clean(it['opts'][k]) for k in 'ABCDE'],
       'ans':it['gab'],'anulada':False,'com':MC[n]}
    if n in FLAW: q['lei']=P+FLAW[n]
    qs.append(q)
# fix texts paragraph joins: simple whitespace normalize

json.dump({'sources':srcs,'texts':texts,'questions':qs},open(D+'data.json','w'),ensure_ascii=False)
print(len(qs), sum(q['anulada'] for q in qs)); 
for k,v in texts.items(): print(k, v[:150],'…',v[-160:])
cmds=set(q['cmd'] for q in qs if q['fmt']=='CE'); print(len(cmds)); [print(' -',c[:120]) for c in cmds]

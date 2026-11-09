import json, sys, re
S='/tmp/claude-0/-home-user/478c6bdf-f475-5683-bd52-c80df6bd2f12/scratchpad/'
sys.path.insert(0, S+'tools'); import ia_questions as IA
d=json.load(open(S+'dl/data2.json')); r=json.load(open(S+'dl/report.json')); d['report']={'excluidas':r['excluidas']}
# questões inéditas (IA): fonte própria por banca, marcadas com ia=True
base={'orgao':'Inédita (IA)','orgao_curto':'Inéditas (IA)','ano':2026,'tipo':'ia','tipo_nome':'Inéditas (IA) no estilo das bancas','ia':True,'prova':None,'gabarito':None}
for sid,banca,fmt,cargo in [('ia_cebraspe','Cebraspe','CE','Itens inéditos no estilo Cebraspe'),('ia_fcc','FCC','MC','Questões inéditas no estilo FCC'),('ia_fgv','FGV','MC','Casos práticos inéditos no estilo FGV')]:
    d['sources'][sid]=dict(base,id=sid,banca=banca,formato=fmt,cargo=cargo)
n=0
for i,(disc,tema,stem,ans,com) in enumerate(IA.CE,1):
    d['questions'].append({'id':f'ia_cebraspe-{i}','src':'ia_cebraspe','n':i,'fmt':'CE','disc':disc,'tema':tema,'cmd':None,'text':None,'stem':stem,'ans':ans,'anulada':False,'com':com,'ia':True})
for sid,L in [('ia_fcc',IA.FCC),('ia_fgv',IA.FGV)]:
    for i,(disc,tema,stem,opts,ans,com) in enumerate(L,1):
        k='ABCDE'.index(ans)
        if sid=='ia_fgv':  # espalha a letra do gabarito de forma determinística
            tgt=(i*3)%5; rot=(k-tgt)%5; opts=opts[rot:]+opts[:rot]; ans='ABCDE'[tgt]; com='Gabarito '+ans+com[10:]
        d['questions'].append({'id':f'{sid}-{i}','src':sid,'n':i,'fmt':'MC','disc':disc,'tema':tema,'cmd':None,'text':None,'stem':stem,'opts':opts,'ans':ans,'anulada':False,'com':com,'ia':True})
for q in d['questions']:
    if q.get('ia'): assert q['com'][9]==q['ans']
t=open(S+'app/template.html').read().replace('/*DATA*/',json.dumps(d,ensure_ascii=False).replace('</','<\\/')).replace('/*VIDS*/{}',json.dumps(json.load(open(S+'yt/verified.json')),ensure_ascii=False).replace('</','<\\/'))
open(S+'out/banca-aberta.html','w').write(t); print(len(t), len(d['questions']))

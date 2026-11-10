import sys, re, subprocess, json
pdf, gabtxt, out, first_page = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
gab = gabtxt.split(',')
def text(p, x, w):
    return subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-layout','-x',str(x),'-y','0','-W',str(w),'-H','842',pdf,'-'],capture_output=True,text=True).stdout
npages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
chunks=[]
for p in range(first_page,npages+1):
    for x in (0,297):
        ls=[l for l in text(p,x,299).split('\n')[2:] if l.strip() and not re.search(r'Tipo Branca|^\s*Especialista em Regulação\s*$|FGV CONHECIMENTO|AGÊNCIA REGULADORA',l)]
        if ls:
            base=min(len(l)-len(l.lstrip()) for l in ls); chunks.append([(len(l)-len(l.lstrip())-base, l.strip()) for l in ls])
qs=[]; cur=None; subj=None; opt=None; lasthdr=False
for ch in chunks:
  for ind,s in ch:
    if s.startswith('Módulo'): continue
    if re.fullmatch(r'\d{1,2}', s) and int(s)==(qs[-1]['n']+1 if qs else 1):
        cur={'n':int(s),'subj':subj,'stem':[],'opts':{}}; qs.append(cur); opt=None; lasthdr=False; continue
    mo=re.match(r'^\(([A-E])\)\s*(.*)', s)
    if cur and mo: opt=mo.group(1); cur['opts'][opt]=mo.group(2); continue
    if cur and opt and ind>=2: cur['opts'][opt]+=' '+s; continue
    if (cur is None) or (opt=='E'):
        subj = (subj+' '+s) if lasthdr else s; lasthdr=True; cur=None; opt=None; continue
    cur['stem'].append(s)
for q in qs:
    q['stem']='\n'.join(q['stem']); q['gab']=gab[q['n']-1]
json.dump(qs,open(out,'w'),ensure_ascii=False,indent=1)
print(len(qs), sorted(set(q['subj'] for q in qs)))

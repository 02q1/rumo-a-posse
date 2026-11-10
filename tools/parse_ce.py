import sys, re, subprocess, json
pdf, gab = sys.argv[1], sys.argv[2]
def text(p, x, w):
    return subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-layout','-x',str(x),'-y','0','-W',str(w),'-H','842',pdf,'-'],capture_output=True,text=True).stdout
npages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
lines=[]
for p in range(1,npages+1):
    for x,w in ((0,298),(297,298)):
        lines += text(p,x,w).split('\n')
# gabarito
g = subprocess.run(['pdftotext','-layout',gab,'-'],capture_output=True,text=True).stdout.split('\n')
ans={}
for i,l in enumerate(g):
    if l.strip().startswith('Item'):
        nums=l.split()[1:]; vals=g[i+1].split()[1:] if g[i+1].strip().startswith('Gabarito') else None
        if vals:
            for n,v in zip(nums,vals):
                if n!='0': ans[int(n)]=v
items=[]; ctx=[]; cur=None
skip=re.compile(r'CEBRASPE –|Espaço livre|^\s*--|^\s*•|^\s*$')
for l in lines:
    if re.search(r'CEBRASPE –|Espaço livre|-- ', l): 
        continue
    m=re.match(r'^\s{0,3}(\d{1,3})\s+(\S.*)$', l)
    if m and int(m.group(1)) in ans and (not items or int(m.group(1))==items[-1]['n']+1 or not cur):
        cur={'n':int(m.group(1)),'text':m.group(2).strip(),'ctx':'\n'.join(ctx).strip()}
        items.append(cur); continue
    if cur is not None and (l.startswith('   ') ) and l.strip():
        cur['text']+=' '+l.strip(); continue
    if not l.strip():
        if ctx and ctx[-1]!='': ctx.append('')
        continue
    if cur is not None:
        ctx=[]; cur=None
    ctx.append(l.rstrip())
for it in items:
    it['text']=re.sub(r'\s+',' ',it['text']); it['gab']=ans.get(it['n'])
json.dump(items,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)
print(len(items), [it['n'] for it in items])
# inherit ctx
last=''
for it in items:
    if it['ctx']: last=it['ctx']
    else: it['ctx']=last
json.dump(items,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)

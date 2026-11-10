import re
def clean(s):
    s=re.sub('[-]','•',s)
    ls=s.split('\n'); out=[ls[0]]
    for l in ls[1:]:
        if re.match(r'^(•|[IVX]+\.|\(\s*\)|\d+\.|“)',l) or re.search(r'[.:?”)]$',out[-1]): out.append(l)
        else: out[-1]+=' '+l
    return '\n'.join(out)

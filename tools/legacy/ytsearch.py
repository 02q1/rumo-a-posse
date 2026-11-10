import sys, json, re, urllib.parse, subprocess
q=sys.argv[1]
html=subprocess.run(['curl','-s','-m','20','-H','Accept-Language: pt-BR','https://www.youtube.com/results?search_query='+urllib.parse.quote(q)],capture_output=True,text=True).stdout
m=re.search(r'var ytInitialData = (\{.*?\});</script>',html,re.S)
if not m: print('NODATA'); sys.exit()
d=json.loads(m.group(1)); out=[]
def walk(o):
    if isinstance(o,dict):
        if 'videoRenderer' in o:
            v=o['videoRenderer']
            out.append((v.get('videoId'),''.join(r.get('text','') for r in v.get('title',{}).get('runs',[])),''.join(r.get('text','') for r in v.get('ownerText',{}).get('runs',[])),v.get('lengthText',{}).get('simpleText',''),v.get('viewCountText',{}).get('simpleText',''),v.get('publishedTimeText',{}).get('simpleText','')))
        for x in o.values(): walk(x)
    elif isinstance(o,list):
        for x in o: walk(x)
walk(d)
for r in out[:int(sys.argv[2]) if len(sys.argv)>2 else 8]: print(' | '.join(r))

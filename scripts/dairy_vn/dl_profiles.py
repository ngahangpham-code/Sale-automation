import sys,re,json,glob
rows=[]
for f in sorted(glob.glob(sys.argv[1]+'/dl_*.html')):
    h=open(f,encoding='utf-8').read()
    # decode " style escapes into a JSON-parseable string
    for m in re.finditer(r'(\[\{\\u0022sku\\u0022.*?\}\]\}\])',h):
        raw=m.group(1)
        try:
            s=json.loads('"'+raw.replace('"','\\"')+'"')  # unescape layer 1
            data=json.loads(s)
        except Exception as e:
            print('ERR',f,e,file=sys.stderr); continue
        for v in data:
            for p in v.get('profiles') or []:
                rows.append((f.split('dl_')[-1][:-5],v.get('title'),p['description'],p['url']))
for r in dict.fromkeys(rows): print('\t'.join(r))

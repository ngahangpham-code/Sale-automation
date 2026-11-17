# usage: page_ing.py cache_dir out.tsv url...  -> url, title, ingredient text (from page text)
import sys,re,subprocess,hashlib,os
from bs4 import BeautifulSoup
D,out=sys.argv[1],sys.argv[2]
with open(out,'w',encoding='utf-8') as o:
  for url in sys.argv[3:]:
    f=os.path.join(D,hashlib.md5(url.encode()).hexdigest()+'.html')
    if not os.path.exists(f): subprocess.run(['curl','-sSL','-m','30','-o',f,url])
    s=BeautifulSoup(open(f,encoding='utf-8',errors='ignore').read(),'lxml')
    for t in s(['script','style','noscript']): t.decompose()
    title=(s.find('h1') or s.title).get_text(' ',strip=True)
    t=re.sub(r'\s+',' ',s.get_text(' ',strip=True))
    ing=''
    for m in re.finditer(r'Thành phần(?! dinh dưỡng)',t):
        seg=t[m.end():m.end()+4000]
        e=re.search(r'Thời hạn sử dụng|Hạn sử dụng|Công dụng|Bảo quản|Đối tượng',seg)
        seg=seg[:e.start()] if e else seg[:1500]
        parts=re.split(r'\d[\d.,]*\s+(?:\(\d+%\)\s*)?\d[\d.,]*\s',seg)
        cand=parts[-1].strip(' :-')
        if len(cand)>25 and ',' in cand: ing=cand; break
    o.write(f'{url}\t{title}\t{ing}\n')

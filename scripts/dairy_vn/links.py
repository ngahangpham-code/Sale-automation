import sys,re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
html=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
s=BeautifulSoup(html,'lxml')
seen=set()
for a in s.find_all('a',href=True):
    u=urljoin(sys.argv[2],a['href'])
    if u not in seen and re.search(sys.argv[3],u,re.I): seen.add(u); print(u,'|',a.get_text(' ',strip=True)[:60])

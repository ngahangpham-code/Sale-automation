# usage: nut.py cache out.tsv urls... -> url, title, meta desc, key actives found in FIRST nutrition table
import sys,re,subprocess,hashlib,os
from bs4 import BeautifulSoup
KEYS=[("IgG / sữa non (colostrum)",r"IgG|sữa non|colostrum"),("2'-FL (HMO)",r"2'\s*-?\s*F|Fucosyllactose|HMO"),("FOS",r"\bFOS\b"),("GOS",r"\bGOS\b"),("Inulin",r"Inulin"),("DHA",r"\bDHA\b"),("ARA",r"\bARA\b"),("Lactoferrin",r"Lactoferrin"),("MCT",r"\bMCT\b"),("Vitamin K2",r"K2"),("Lysine",r"Lysin"),("Choline",r"Cholin"),("Taurine",r"Taurin"),("Lutein",r"Lutein"),("Nucleotides",r"Nucleotid"),("L-carnitine",r"carnitin"),("Inositol",r"Inositol"),("Probiotic/lợi khuẩn",r"Probiotic|Bifido|Lactobacillus|lợi khuẩn|BB-12|men sống"),("Postbiotic",r"Postbiotic"),("Whey/WPC",r"whey|WPC"),("Đạm sữa A2",r"\bA2\b"),("MFGM",r"MFGM"),("Sphingomyelin",r"Sphingomyelin"),("HMB",r"\bHMB\b"),("Collagen",r"Collagen"),("Arginine",r"Arginin"),("Glucosamine",r"Glucosamin"),("Isomaltulose/Palatinose",r"Isomaltulose|Palatinose"),("Crom",r"Crom|Chromium"),("Omega 3/ALA",r"Omega\s*3|ALA\b|Alpha Linolenic"),("Beta-glucan",r"glucan"),("Chất xơ",r"Chất xơ"),("Canxi",r"Canxi|Calci"),("Vitamin D3",r"D3"),("Glutamine",r"Glutamin"),("Leucine",r"Leucin"),("Sữa non/IgA",r"IgA")]
D,out=sys.argv[1],sys.argv[2]
with open(out,'w',encoding='utf-8') as o:
  for url in sys.argv[3:]:
    f=os.path.join(D,hashlib.md5(url.encode()).hexdigest()+'.html')
    if not os.path.exists(f): subprocess.run(['curl','-sSL','-m','30','-o',f,url])
    s=BeautifulSoup(open(f,encoding='utf-8',errors='ignore').read(),'lxml')
    for t in s(['script','style','noscript','header','footer','nav']): t.decompose()
    h1=s.find('h1'); title=(h1 or s.title).get_text(' ',strip=True) if (h1 or s.title) else ''
    md=s.find('meta',attrs={'name':'description'}) or s.find('meta',attrs={'property':'og:description'})
    md=(md.get('content') or '') if md else ''
    t=re.sub(r'\s+',' ',s.get_text(' ',strip=True))
    m=re.search(r'Thành phần[^.]{0,40}?(Đơn vị|Trong 100)',t)
    tab=t[m.start():m.start()+2500] if m else ''
    found=[k for k,rx in KEYS if re.search(rx,tab,re.I)]
    o.write('\t'.join([url,re.sub(r'\s+',' ',title),re.sub(r'\s+',' ',md)[:400],', '.join(found)])+'\n')

# usage: sm.py sitemap_url [maxdepth] -> prints all page URLs (recurses sitemap indexes, handles .gz)
import sys,re,subprocess,gzip
def get(u):
    b=subprocess.run(['curl','-sSL','-m','60',u],capture_output=True).stdout
    if b[:2]==b'\x1f\x8b': b=gzip.decompress(b)
    return b.decode('utf-8','ignore')
def walk(u,d):
    x=get(u); locs=[l.strip() for l in re.findall(r'<loc>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</loc>',x,re.S)]
    if '<sitemapindex' in x and d>0:
        for l in locs: walk(l,d-1)
    else:
        for l in locs: print(l)
walk(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 2)

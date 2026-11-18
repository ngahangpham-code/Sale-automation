# usage: ph.py cache out.tsv urls... -> url, title, ingredients, origin, manufacturer, brand
import sys,re,subprocess,hashlib,os
from bs4 import BeautifulSoup
D,out=sys.argv[1],sys.argv[2]
with open(out,'w',encoding='utf-8') as o:
  for url in sys.argv[3:]:
    f=os.path.join(D,hashlib.md5(url.encode()).hexdigest()+'.html')
    if not os.path.exists(f): subprocess.run(['curl','-sSL','-m','40','-o',f,url])
    s=BeautifulSoup(open(f,encoding='utf-8',errors='ignore').read(),'lxml')
    for t in s(['script','style','noscript']): t.decompose()
    h1=s.find('h1'); title=h1.get_text(' ',strip=True) if h1 else ''
    t=re.sub(r'\s+',' ',s.get_text(' ',strip=True))
    ing=''
    m0=re.search(r'Thành phần\s*:\s*(.{20,4000}?)(?=\s(?:Công dụng|Chỉ định|Cách [Ss]ử [Dd]ụng|Cách dùng|Lưu ý|Hướng dẫn|Đối tượng|Bảo quản|Giao hàng|Mô tả|Thành phần dinh dưỡng|Giá trị dinh dưỡng|Tác dụng))',t)
    m=re.search(r'Mô tả sản phẩm Thành phần (.{0,3000}?)(?= Chỉ định | Công dụng | Cách sử dụng | Cách dùng )',t)
    if m0: ing=m0.group(1).strip()
    elif m:
        ing=m.group(1)
        if title and ing.startswith(title): ing=ing[len(title):]
        ing=re.sub(r'^\s*(Thông tin thành phần|Thành phần)?\s*:?\s*','',ing).strip()
    def grab(k):
        m=re.search(k+r':\s*(.{1,120}?)(?=\s(?:Nơi sản xuất|Tên Nhà sản xuất|Công ty chịu|Công ty phân phối|Xem thêm|Xuất xứ)|$)',t)
        return m.group(1).strip() if m else ''
    o.write('\t'.join([url,title,ing,grab('Nơi sản xuất'),grab('Tên Nhà sản xuất'),grab('Xuất xứ thương hiệu')])+'\n')

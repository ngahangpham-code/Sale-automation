# usage: rt.py source_name cache_dir url_list out.tsv
# -> source, url, title, made_in, manufacturer, brand, ingredient_text, format
import sys,re,os,hashlib
from bs4 import BeautifulSoup
src,D,lst,out=sys.argv[1:5]
END=r'(?=\s(?:Hướng dẫn sử dụng|Hướng dẫn bảo quản|Cách sử dụng|Cách dùng|Công dụng|Đối tượng sử dụng|Bảo quản|Lưu ý|Chỉ định|Thông tin dinh dưỡng|Giá trị dinh dưỡng|Thành phần dinh dưỡng|Hạn sử dụng|Xuất xứ|Thương hiệu|Quy cách|Vận chuyển|Sản phẩm liên quan|Đánh giá))'
def f(rx,t,n=120):
    m=re.search(rx+r'\s*:?\s*(.{1,%d}?)(?=\s(?:Sản xuất tại|Trọng lượng|Độ tuổi|Nhà sản xuất|Cảnh báo|Xuất xứ|Thương hiệu|Quy cách|Hạn sử dụng|Thể tích|Dung tích|Mã sản phẩm|SKU)|$)'%n,t)
    return m.group(1).strip(' :') if m else ''
with open(out,'w',encoding='utf-8') as o:
  for url in open(lst,encoding='utf-8').read().split():
    p=os.path.join(D,hashlib.md5(url.encode()).hexdigest()+'.html')
    if not os.path.exists(p): continue
    s=BeautifulSoup(open(p,encoding='utf-8',errors='ignore').read(),'lxml')
    for x in s(['script','style','noscript']): x.decompose()
    h1=s.find('h1'); title=re.sub(r'\s+',' ',h1.get_text(' ',strip=True)) if h1 else ''
    t=re.sub(r'\s+',' ',s.get_text(' ',strip=True))
    ing,fmt='',''
    m=re.search(r'THÀNH PHẦN & DINH DƯỠNG \+?\s*(.{10,3000}?)(?=\s(?:Hướng dẫn sử dụng|Hướng dẫn bảo quản|Vận chuyển))',t)
    if m: ing,fmt=m.group(1),'grouped'
    else:
        for rx in [r'Thành phần(?: nguyên liệu| cấu tạo)?\s*:\s*(.{15,3000}?)'+END, r'Thành phần(?! dinh dưỡng)(?: nguyên liệu| cấu tạo)?\s+(.{15,3000}?)'+END]:
            m=re.search(rx,t)
            if m and ',' in m.group(1): ing,fmt=m.group(1),'label'; break
    made=f(r'Sản xuất tại',t,40) or f(r'Nơi sản xuất',t,40) or f(r'Xuất xứ(?: thương hiệu)?',t,40)
    mfr=f(r'Nhà sản xuất',t,150)
    brand=f(r'Thương hiệu',t,40)
    o.write('\t'.join(x.replace('\t',' ') for x in [src,url,title,made,mfr,brand,ing.strip(),fmt])+'\n')

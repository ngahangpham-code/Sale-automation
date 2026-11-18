# Build products.json from scraped/OCR data
import re,json,glob,difflib,os,sys
S=sys.argv[1]; os.chdir(S)
FIX={'chât':'chất','ôn định':'ổn định','ồn định':'ổn định','thực phâm':'thực phẩm','dâu cá':'dầu cá','dâu thực vật':'dầu thực vật',
 'gẦY':'gầy','gẦy':'gầy','tông hợp':'tổng hợp','fiuctose':'fructose','460()':'460(i)','452()':'452(i)','4520))':'452(i))','4520)':'452(i)',
 '14442':'1442','Bó,':'B6,','BI,':'B1,','BI)':'B1)','điêu chỉnh':'điều chỉnh','giông':'giống','chính độ':'chỉnh độ','axít':'axit','| ':'','ỗn định':'ổn định','đường sugar 6, 8%)':'đường (6,8%)','thực phẩn':'thực phẩm','(#71)':'(471)',' wege,':',',' lodized salt':'','Bó)':'B6)','Bó và':'B6 và','befa':'beta','đùng':'dùng','muỗi I-Št':'muối I-ốt',' ƒiesh milk':'',') ƒermented yoghurt':'',' pomegranafe juice':'','đường sugar,':'đường,',' (Iricalcium phosphare)':')','hướng đương':'hướng dương','Omega 6⁄ containing Omega 3, Qmega 6':'Omega 6, Omega 3','axit folie':'axit folic',' (wafer, milk powđers)':'','_ ':'','- buttermilk':'buttermilk'}
def clean_dl(t):
    t=re.split(r'\.\s+(?=[A-Z][a-z]+[\s,])',t)[0]            # drop trailing English sentence
    t=re.split(r'\s\S{1,4}:\s*[a-z]+ [a-z]+',t)[0]          # drop "ân: milk powder..." tails
    t=re.sub(r'(?<=[^\s\d])\s*[/!]\s*[^,()]*?(?=\s*[,()]|$)','',t)   # drop "/ english" glosses (OCR may read / as !)
    t=re.sub(r'\)\s*\((?![^()]*\d)(?![^()]*[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ])[^()]*\)',')',t)  # drop English duplicate (...)
    for a,b in FIX.items(): t=t.replace(a,b)
    t=re.sub(r'\s+',' ',t).strip(' .;')
    return t
rows=[]
# ---- Dutch Lady / FrieslandCampina (OCR of declaration PDFs)
seen=set()
for i,line in enumerate(open('dl_profiles.tsv',encoding='utf-8'),1):
    slug,title,desc,url=line.rstrip('\n').split('\t')
    if re.search(r'CẬP NHẬT|CÔNG VĂN|HÔ',desc,re.I) or url in seen: continue
    seen.add(url)
    ing=''
    p=f'pdf/dl_{i}.ocr.txt'
    if os.path.exists(p):
        ing=os.popen(f'python3 -I code/extract.py {p}').read().strip()
    brand='Dutch Lady (Cô Gái Hà Lan)'
    if 'fristi' in slug: brand='Fristi'
    elif 'yomost' in slug: brand='Yomost'
    elif 'hoan-hao' in slug: brand='Hoàn Hảo'
    elif 'truong-sinh' in slug: brand='Trường Sinh'
    cat=('Sữa đặc / kem đặc' if 'kem-dac' in slug else 'Sữa bột' if 'nguyen-kem' in slug else
         'Sữa chua uống / thức uống lên men' if ('yomost' in slug or 'fristi' in slug) else 'Sữa nước (UHT)')
    name=title.strip()
    variant=re.sub(r'^(HỒ SƠ|BẢN)( TỰ)? (CÔNG BỐ|CÔNG BỐ HỢP QUY) SẢN PHẨM\s*','',desc,flags=re.I).strip()
    rows.append(dict(company='FrieslandCampina Việt Nam',brand=brand,cat=cat,product=f'{name} — {variant}' if variant and variant.upper()!=name.upper() else name,
        dtype='Danh sách nguyên liệu (hồ sơ công bố)' if ing else 'Có hồ sơ công bố – chưa trích được',
        ing=clean_dl(ing) if ing else '',src=url,decl=url,
        note='Trích bằng OCR từ bản scan hồ sơ công bố – có thể còn lỗi chính tả nhỏ, nên đối chiếu file gốc.' if ing else 'Mở file PDF gốc để xem thành phần.'))
# ---- Hanoimilk (product pages, text)
decl=[l.rstrip('\n').split('\t') for l in open('hn_list.tsv',encoding='utf-8')]
def norm(s): return re.sub(r'\s+',' ',re.sub(r'THÔNG TIN CÔNG BỐ SẢN PHẨM:|THỰC PHẨM BỔ SUNG|\d+\s*ML|TUDD|THỨC UỐNG DINH DƯỠNG','',s.upper())).strip()
seen=set()
for line in open('hn_ing.tsv',encoding='utf-8'):
    url,title,ing=line.rstrip('\n').split('\t')
    if title in seen: continue
    seen.add(title)
    if 'Thành phần:' in ing: ing=ing.split('Thành phần:')[-1]
    m=re.search(r'\b(Nước|Sữa tươi|Sữa bò tươi)\b',ing)
    if m: ing=ing[m.start():]
    ing=ing.strip(' -:.')
    best=max(decl,key=lambda d: difflib.SequenceMatcher(None,norm(d[1]),norm(title)).ratio())
    r=difflib.SequenceMatcher(None,norm(best[1]),norm(title)).ratio()
    cat='Sữa nước (UHT)' if 'TIỆT TRÙNG' in title.upper() else 'Sữa uống dinh dưỡng pha sẵn' if 'IZZI' in title.upper() or 'DINH DƯỠNG' in title.upper() else 'Thức uống sữa'
    if 'TUDD' in title.upper() or 'THỨC UỐNG' in title.upper(): cat='Thức uống sữa (trái cây/thạch/cacao)'
    rows.append(dict(company='CTCP Sữa Hà Nội (Hanoimilk)',brand='IZZI' if 'IZZI' in title.upper() else 'Hanoimilk',cat=cat,product=title,
        dtype='Danh sách nguyên liệu (trang sản phẩm)',ing=ing,src=url,decl=best[2] if r>0.55 else 'https://hanoimilk.com/blogs/tong-hop-thong-tin-cong-bo-san-pham',
        note='Hồ sơ công bố đăng dạng file Google Drive trong bài viết.'))
# Hanoimilk yogurts: declarations on Google Drive, OCR
man=json.load(open('hn_manual.json',encoding='utf-8'))
drive=dict(l.rstrip('\n').split('\t') for l in open('hn_drive.tsv',encoding='utf-8') if '\t' in l)
for c,t,u in decl:
    if c in('sua-chua-an','sua-chua-uong-1'):
        b=u.rsplit('/',1)[1]; ing=man.get(b,'')
        if not ing and os.path.exists(f'hnpdf/{b}.ocr.txt'): ing=os.popen(f'python3 -I code/extract.py hnpdf/{b}.ocr.txt').read().strip()
        ing=clean_dl(ing) if ing else ''
        for a,z in {'tỉnh luyện':'tinh luyện','tỉnh khiết':'tinh khiết','Streptococus kc':'Streptococcus','Streptococus':'Streptococcus','Strepfococcus':'Streptococcus','bulparicus':'bulgaricus','phẩm mẫu':'phẩm màu','(NS ':'(INS ','vitamin (A, €)':'vitamin (A, C)','chất ồn':'chất ổn','chất ôn':'chất ổn','chất ỗn':'chất ổn'}.items(): ing=ing.replace(a,z)
        rows.append(dict(company='CTCP Sữa Hà Nội (Hanoimilk)',brand='Yotuti' if 'YOTUTI' in t else 'Hanoimilk',cat='Sữa chua ăn' if c=='sua-chua-an' else 'Sữa chua uống',
          product=t.replace('THÔNG TIN CÔNG BỐ SẢN PHẨM:','').strip(),dtype='Danh sách nguyên liệu (hồ sơ công bố)' if ing else 'Có hồ sơ công bố – chưa trích được',ing=ing,src=u,
          decl=f'https://drive.google.com/file/d/{drive[b]}/view' if drive.get(b) else u,note='Trích bằng OCR từ hồ sơ công bố (file Google Drive) – nên đối chiếu file gốc.'))
# ---- Pharmacity: VN-made products with full ingredient lists
CO={'Công ty Cổ phần Sữa Việt Nam':'CTCP Sữa Việt Nam (Vinamilk)','CÔNG TY TNHH NESTLÉ VIỆT NAM':'Công ty TNHH Nestlé Việt Nam','Công Ty Cổ Phần Sữa Vitadairy Việt Nam':'CTCP VitaDairy Việt Nam','Nhà máy Vitadairy Bình Dương':'CTCP VitaDairy Việt Nam'}
seen=set()
for l in open('ph.tsv',encoding='utf-8'):
    url,title,ing,org,mfr,bo=l.rstrip('\n').split('\t')
    comp=CO.get(mfr) if org.startswith('Việt Nam') else None
    if 'TH True Milk' in title: comp='CTCP Sữa TH (TH Group)'
    if not comp or not ing or title in seen or ing.startswith('Sữa ColosBaby Gold chứa'): continue
    seen.add(title)
    ing=re.sub(r'\s*Quy cách\s*:.*$','',ing).strip()
    ing=re.sub(r'^TH True Milk Sữa Tươi TT ít đường\s*','',ing)
    brand=next((b for b in ['Optimum Gold','Sure Prevent','Sure Diecerna','MILO','ColosBaby','FOHEPTA','TH true MILK'] if b.lower() in title.lower()),'')
    cat='Sữa bột trẻ em' if ('cho trẻ' in title or 'Cho Trẻ' in title) else 'Dinh dưỡng y học / người lớn' if 'Sữa bột' in title else 'Sữa nước / thức uống sữa'
    rows.append(dict(company=comp,brand=brand,cat=cat,product=title,dtype='Danh sách nguyên liệu (nhà bán lẻ Pharmacity)',ing=ing,src=url,decl='',
        note=('Pharmacity ghi nơi sản xuất: Việt Nam. ' if org else '')+('Danh sách bị cắt ngắn trên trang (kết thúc bằng "...").' if ing.endswith('...') else '')))
# ---- other retailer / association sources found via web search
for c,b,cat,pr,dt,ing,src,note in json.load(open('extra.json',encoding='utf-8')):
    rows.append(dict(company=c,brand=b,cat=cat,product=pr,dtype=dt,ing=ing,src=src,decl='',note=note))
# ---- Nutifood & Vitadairy (nutrition-table actives)
def nut(file,company,brandf,catf):
    out=[]
    for line in open(file,encoding='utf-8'):
        url,title,md,act=line.rstrip('\n').split('\t')
        if not title or title.startswith('Nutifood - Giải Pháp'): continue
        out.append(dict(company=company,brand=brandf(title,url),cat=catf(title,url),product=re.sub(r'\s+',' ',title),
            dtype='Hoạt chất nổi bật (theo bảng dinh dưỡng)' if act else 'Trang sản phẩm không công bố thành phần',
            ing=act,src=url,decl='',note='Website chỉ đăng bảng giá trị dinh dưỡng, không đăng danh sách nguyên liệu đầy đủ; cột thành phần liệt kê hoạt chất/vi chất có trong bảng.'))
    return out
def nb(t,u):
    for k,v in [('grow','GrowPLUS+'),('nuvi','NuVi'),('varna','Värna'),('nutimilk','NutiMilk'),('new-zealand','NutiMilk')]:
        if k in u: return v
    return 'Nutifood'
def nc(t,u):
    if 'ngu-coc' in u: return 'Ngũ cốc dinh dưỡng'
    if 'sua-chua' in u or 'len-men' in u: return 'Sữa chua / sữa lên men'
    if 'varna' in u or 'complete' in u: return 'Sữa bột người lớn'
    if 'grow-plus' in u or 'nuvi-grow' in u: return 'Sữa bột / pha sẵn trẻ em'
    if 'creamer' in u: return 'Sữa đặc / creamer pha chế'
    return 'Sữa nước / thức uống sữa'
rows+=nut('nuti.tsv','Nutifood (CTCP Thực phẩm Dinh dưỡng Nutifood Bình Dương)',nb,nc)
def vb(t,u):
    for k,v in [('colosbaby','ColosBaby'),('oggi','Oggi'),('calosure','CaloSure'),('colos','Colos'),('calokid','Calokid'),('vitagrow','Vitagrow'),('nepro','Nepro'),('gluvita','Gluvita'),('fohepta','Fohepta'),('colosigg','ColosIgG 24h')]:
        if k in u: return v
    return 'VitaDairy'
def vc(t,u):
    if 'nguoi-lon' in u: return 'Dinh dưỡng y học / người lớn'
    if 'cho-me' in u: return 'Sữa bột bà mẹ'
    if 'sua-uong' in u or '237ml' in u or 'trai-cay' in u: return 'Sữa uống pha sẵn'
    if 'mien-dich-dung-kem' in u: return 'Bột sữa non bổ sung'
    return 'Sữa bột trẻ em'
rows+=nut('vd2.tsv','CTCP VitaDairy Việt Nam',vb,vc)
# ---- companies without accessible data: brand-level rows
blocked=[
 ('CTCP Sữa Việt Nam (Vinamilk)','Vinamilk 100% Sữa tươi, Green Farm, Organic Gold','Sữa nước (UHT, thanh trùng)'),
 ('CTCP Sữa Việt Nam (Vinamilk)','Ông Thọ, Ngôi Sao Phương Nam','Sữa đặc / kem đặc'),
 ('CTCP Sữa Việt Nam (Vinamilk)','Susu, Probi, Vinamilk Yogurt','Sữa chua ăn / sữa chua uống / lên men'),
 ('CTCP Sữa Việt Nam (Vinamilk)','Optimum, Dielac, Yoko, Sure Prevent','Sữa bột trẻ em / người lớn'),
 ('CTCP Giống bò sữa Mộc Châu (Mộc Châu Milk – thuộc Vinamilk/GTNfoods)','Mộc Châu Milk, Yo-Pro, Mộc Châu Creamery','Sữa tươi thanh/tiệt trùng, sữa chua'),
 ('CTCP Sữa TH (TH Group)','TH true MILK, TH true YOGURT, TH true OAT, TH true NUT','Sữa tươi, sữa chua, sữa hạt'),
 ('Dalatmilk (thuộc TH Group)','Dalatmilk, Dalatmilk Cool C','Sữa tươi thanh/tiệt trùng, thức uống sữa chua lên men'),
 ('CTCP Sữa Quốc tế LOF (tên cũ IDP)','Kun, LOF Ba Vì, LiF (Love\'in Farm), Malto','Sữa tươi, sữa chua, thức uống sữa trẻ em'),
 ('Công ty TNHH Nestlé Việt Nam','MILO (RTD UHT), Nestlé','Thức uống lúa mạch – sữa UHT'),
 ('CTCP Nutricare','Metacare, Glucare Gold, Nutricare Gold, Smarta IQ, Care 100','Sữa bột / dinh dưỡng y học, sữa nước'),
]
for c,b,cat in blocked:
    rows.append(dict(company=c,brand=b,cat=cat,product='(Các SKU khác của nhóm thương hiệu – chưa lấy được thành phần)',dtype='Chưa truy cập được website',ing='',src='',decl='',note='Website chặn truy cập tự động từ môi trường cloud – cần mở trên máy của bạn.'))
# Vinamilk partial from web search
rows.append(dict(company='CTCP Sữa Việt Nam (Vinamilk)',brand='Vinamilk',cat='Sữa nước (UHT)',product='Sữa tươi tiệt trùng giảm béo hương chuối',dtype='Danh sách nguyên liệu (trích một phần, qua kết quả tìm kiếm)',
    ing='Sữa tươi tách béo (95,9%), đường, nước chuối ép cô đặc (10 g/l), … (chưa đầy đủ)',src='https://www.vinamilk.com.vn/cong-bo-san-pham/',decl='https://www.vinamilk.com.vn/cong-bo-san-pham/',
    note='Dòng này lấy từ đoạn trích trong kết quả tìm kiếm, mình chưa mở được file PDF gốc – cần đối chiếu.'))
json.dump(rows,open('products.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(rows)); print(Counter(r['company'] for r in rows)); print(Counter(r['dtype'] for r in rows))

# Merge official + retailer records, normalise ingredients, flag accuracy issues -> records.json
import json,re,sys,unicodedata,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__)))
import norm
S=sys.argv[1]; os.chdir(S)
OLDC={'CTCP Sữa Việt Nam (Vinamilk)':'Vinamilk','FrieslandCampina Việt Nam':'FrieslandCampina VN','CTCP Sữa TH (TH Group)':'TH Group',
 'Nutifood (CTCP Thực phẩm Dinh dưỡng Nutifood Bình Dương)':'Nutifood','CTCP VitaDairy Việt Nam':'VitaDairy','CTCP Sữa Hà Nội (Hanoimilk)':'Hanoimilk',
 'CTCP Giống bò sữa Mộc Châu (Mộc Châu Milk – thuộc Vinamilk/GTNfoods)':'Mộc Châu Milk','CTCP Sữa Quốc tế LOF (tên cũ IDP)':'LOF (IDP)',
 'Công ty TNHH Nestlé Việt Nam':'Nestlé VN','CTCP Nutricare':'Nutricare','Dalatmilk (thuộc TH Group)':'Dalatmilk'}
SRCNAME={'thegioisua':'Thế Giới Sữa (thegioisua.com)','kfm':'Kingfoodmart','scby':'Sữa Cho Bé Yêu (suachobeyeu.vn)','medigo':'Medigo','vda':'Hiệp hội Sữa VN (vda.org.vn)'}
MARKETING=re.compile(r'\b(nên|lý tưởng|giúp|lợi ích|mã vạch|hỗ trợ|bạn có thể|mẹ nên|chúng tôi|công thức sữa|bao gồm:)',re.I)
DAIRY=re.compile(r'sữa|milk|yogurt|váng|phô mai|\bbơ\b|milo|kem đặc|creamer|probi|susu|kun|izzi|nuvi|fristi|yomost|growplus|colos|metacare|glucare|v[aä]rna|optimum|dielac|sure',re.I)
DOMESTIC={'Vinamilk','Mộc Châu Milk','TH Group','Dalatmilk','Hanoimilk','LOF (IDP)','Nutifood','VitaDairy','Nutricare','FrieslandCampina VN'}
def cat_of(t):
    t=t.lower()
    for k,v in [('sữa chua uống','Sữa chua uống'),('scu','Sữa chua uống'),('sữa chua','Sữa chua ăn'),('sca','Sữa chua ăn'),('váng sữa','Váng sữa'),('phô mai','Phô mai'),('bơ','Bơ'),('kem đặc','Sữa đặc / kem đặc'),('sữa đặc','Sữa đặc / kem đặc'),('creamer','Sữa đặc / kem đặc'),
                ('pha sẵn','Sữa bột pha sẵn'),('sbps','Sữa bột pha sẵn'),('sddps','Sữa bột pha sẵn'),('sữa bột','Sữa bột'),('spdd','Sữa bột'),('sb ','Sữa bột'),('lon','Sữa bột'),('ngũ cốc','Ngũ cốc'),('bột ăn dặm','Bột ăn dặm'),
                ('thạch','Thức uống sữa có thạch'),('lúa mạch','Thức uống lúa mạch / cacao'),('milo','Thức uống lúa mạch / cacao'),('trái cây','Thức uống sữa trái cây'),('lên men','Sữa lên men'),('hạt','Sữa hạt'),('yến mạch','Sữa hạt / ngũ cốc'),
                ('thanh trùng','Sữa thanh trùng'),('tiệt trùng','Sữa tiệt trùng (UHT)'),('sữa tươi','Sữa tiệt trùng (UHT)'),('sữa','Sữa nước / thức uống sữa')]:
        if k in t: return v
    return 'Khác'
def skukey(c,title):
    t=unicodedata.normalize('NFD',title.lower()).replace('đ','d')
    t=''.join(ch for ch in t if unicodedata.category(ch)!='Mn')
    t=re.sub(r'\d+([.,]\d+)?\s?(ml|l|g|gr|gram|kg|hop|chai|tui|loc|thung|hu|goi|lon|vien)\b',' ',t)
    t=re.sub(r'\b(combo|thung|loc|hop|chai|tui|bich|hu|lon|goi|x\d+|\d+x|tba|tbs|ht|h|l|s|vn|moi|new|chinh hang|mua|tang|qua)\b',' ',t)
    t=re.sub(r'[^a-z0-9+ ]',' ',t)
    stop={'sua','bot','dinh','duong','san','pham','cho','tre','tu','thang','tuoi','nam','be','co','va','vi','huong','thuc','uong','cong','thuc','loai','dang','spdd','spddct','sb','sddps','sbps','tt','st','sttc','sttct','stc','stlm','scu','sca','nhan','hieu','danh','nguoi','lon','tren','duoi','the','tich'}
    toks=sorted(set(w for w in t.split() if w not in stop and not (w.isdigit() and len(w)>2)))
    return c+'|'+' '.join(toks)
recs=[]
def add(**r):
    r['ings']=norm.ingredients(r['ing']) if r['ing'] else []
    recs.append(r)
# ---- previous dataset (official sites, OCR, Pharmacity, search summaries)
for x in json.load(open('products.json',encoding='utf-8')):
    if x['dtype'].startswith('Chưa truy cập') or x['product'].startswith('(Các SKU'): continue
    c=OLDC[x['company']]; d=x['dtype']
    if 'hồ sơ công bố' in d: rel,st='A','Hồ sơ công bố (PDF, OCR)'
    elif 'trang sản phẩm' in d: rel,st='A','Website hãng'
    elif 'Hoạt chất' in d or 'không công bố' in d: rel,st='C','Website hãng – chỉ bảng dinh dưỡng'
    elif 'Pharmacity' in d: rel,st='B','Nhà bán lẻ (Pharmacity)'
    else: rel,st='D','Tóm tắt qua kết quả tìm kiếm'
    notes=[]
    if 'OCR' in x['note']: notes.append('Đọc bằng OCR từ bản scan – có thể sai chính tả nhỏ ở mã INS.')
    if rel=='C': notes.append('Chỉ có hoạt chất trong bảng dinh dưỡng, không phải danh sách nguyên liệu: thiếu nền sữa, dầu, phụ gia.')
    if rel=='D': notes.append('Chưa mở trực tiếp được trang nguồn – thông tin qua đoạn tóm tắt của công cụ tìm kiếm. '+x['note'])
    if x['ing'].rstrip().endswith(('...','…')): notes.append('Danh sách bị cắt ngắn trên trang nguồn.')
    if 'rút gọn' in d or 'tóm tắt' in d: notes.append('Danh sách rút gọn, thiếu % và mã phụ gia.')
    if rel=='B' and x['note'] and 'cắt ngắn' not in x['note']: pass
    src=x['src'] if x['src']!='—' else ''
    add(customer=c,product=x['product'],cat=x['cat'],source=st,rel=rel,ing=x['ing'] if x['ing']!='—' else '',url=src,made='Việt Nam',notes=notes)
# ---- retailer scrapes
for name in ['thegioisua','kfm','scby','medigo','vda']:
    fn={'thegioisua':'rt/tgs.tsv'}.get(name,f'rt/{name}.tsv')
    if not os.path.exists(fn): continue
    for l in open(fn,encoding='utf-8'):
        p=l.rstrip('\n').split('\t')
        if len(p)<8: continue
        _,url,title,made,mfr,brand,ing,fmt=p
        if not ing or not title: continue
        if MARKETING.search(ing) or ing.count(',')<3: continue              # marketing copy or too short to be a label
        if not DAIRY.search(title) or re.search(r'kitkat|chunky|kẹo|bánh|nuggets|ngũ cốc ăn sáng|bột ăn dặm|ridielac|bao cao su|xịt|viên uống',title,re.I): continue
        if made and not re.search(r'việt nam',made,re.I): continue            # imported: not made by a VN factory
        c=norm.customer(mfr,title,brand,url)
        if not c: continue
        if not made and not (c in DOMESTIC or (c=='Nestlé VN' and re.search('milo',title,re.I))): continue  # mixed import/local brands need explicit VN origin
        notes=[]
        rel='B'
        if fmt=='grouped':
            rel='C'; notes.append('Nhà bán lẻ tự phân nhóm lại (khoáng/vitamin/chất béo/đường…), không giữ thứ tự nhãn, không có % và hiếm khi có mã phụ gia – dùng để biết CÓ/KHÔNG có nguyên liệu, không dùng để biết tỷ lệ.')
        if ing.rstrip().endswith(('...','…',',')): notes.append('Danh sách bị cắt ngắn trên trang nguồn.')
        if not made: notes.append('Trang không ghi nơi sản xuất – khách hàng suy ra từ thương hiệu.')
        if fmt=='label' and not re.search(r'\d',ing): notes.append('Không có % hay mã INS – có thể là danh sách rút gọn.')
        add(customer=c,product=title,cat=cat_of(title),source='Nhà bán lẻ – '+SRCNAME[name],rel=rel,ing=ing,url=url,made=made or '(không ghi)',notes=notes)
# ---- SKU grouping + cross-source conflict notes
groups={}
for i,r in enumerate(recs):
    r['key']=skukey(r['customer'],r['product']); groups.setdefault(r['key'],[]).append(i)
gid=0
for k,idx in groups.items():
    gid+=1
    for i in idx: recs[i]['sku_id']=f'SKU{gid:04d}'
    full=[i for i in idx if recs[i]['rel'] in('A','B') and recs[i]['ings'] and not any('cắt ngắn' in n for n in recs[i]['notes'])]
    if len(full)>=2:
        sets={i:set(recs[i]['ings']) for i in full}
        for i in full:
            for j in full:
                if i==j: continue
                miss=sorted(sets[j]-sets[i]-{'Premix vitamin','Premix khoáng','Hương liệu','Dầu thực vật (không ghi rõ)','Sữa bột (không ghi rõ loại)'})
                if miss:
                    recs[i]['notes'].append(f"Nguồn khác ({recs[j]['source']}) ghi thêm: "+', '.join(miss[:6])+(' …' if len(miss)>6 else '')+' → các nguồn KHÔNG THỐNG NHẤT (có thể khác phiên bản công thức hoặc nhà bán lẻ chép nhầm nhãn); ưu tiên nguồn có độ tin cậy cao hơn.')
                    break
json.dump(recs,open('records.json','w',encoding='utf-8'),ensure_ascii=False)
from collections import Counter
print(len(recs),'records',len(groups),'SKU groups')
print(Counter(r['customer'] for r in recs))
print(Counter(r['rel'] for r in recs))

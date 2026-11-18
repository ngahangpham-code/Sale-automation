# records.json -> opportunity workbook
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__)); import norm
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import ColorScaleRule,FormulaRule
recs=json.load(open(sys.argv[1],encoding='utf-8')); OUT=sys.argv[2]
F='Arial'; BF=Font(name=F,size=10); BB=Font(name=F,size=10,bold=True); LINK=Font(name=F,size=10,color='0563C1',underline='single')
HF=Font(name=F,bold=True,color='FFFFFF',size=10); HFILL=PatternFill('solid',fgColor='1F4E79')
YEL=PatternFill('solid',fgColor='FFFF00'); INP=Font(name=F,size=10,color='0000FF',bold=True)
WR=Alignment(wrap_text=True,vertical='top'); thin=Side(style='thin',color='BFBFBF'); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)
RELFILL={'A':'C6EFCE','B':'E2EFDA','C':'FFF2CC','D':'FCE4D6'}
RELTXT={'A':'A – Hồ sơ công bố / website hãng','B':'B – Nhà bán lẻ ghi nguyên văn nhãn','C':'C – Nhà bán lẻ phân nhóm lại / chỉ bảng dinh dưỡng','D':'D – Tóm tắt qua công cụ tìm kiếm'}
CUSTS=['Vinamilk','FrieslandCampina VN','TH Group','Nutifood','VitaDairy','Nutricare','Mộc Châu Milk','LOF (IDP)','Hanoimilk','Nestlé VN','Dalatmilk','Abbott VN','Morinaga VN']
CUSTS=[c for c in CUSTS if any(r['customer']==c for r in recs)]
def title(ws,t,sub):
    ws['A1']=t; ws['A1'].font=Font(name=F,bold=True,size=13,color='1F4E79')
    ws['A2']=sub; ws['A2'].font=Font(name=F,italic=True,size=9)
def hdr(ws,r,cols,widths):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        x=ws.cell(r,i,c); x.font=HF; x.fill=HFILL; x.alignment=Alignment(wrap_text=True,vertical='center'); x.border=BOX
        ws.column_dimensions[L(i)].width=w
    ws.row_dimensions[r].height=32
def put(ws,r,vals,font=BF):
    for j,v in enumerate(vals,1):
        c=ws.cell(r,j,v); c.font=font; c.alignment=WR; c.border=BOX
    return r
wb=Workbook()
# ======== 1 Hướng dẫn
ws=wb.active; ws.title='Hướng dẫn'
txt=[('TÌM NGUYÊN LIỆU CHƯA BÁN CHO CÁC NHÀ SẢN XUẤT SỮA TẠI VIỆT NAM',Font(name=F,bold=True,size=14,color='1F4E79')),
('Lập ngày 18/11/2026 · Dữ liệu thành phần công khai trên website hãng, hồ sơ công bố và các nhà bán lẻ',Font(name=F,italic=True,size=10)),('',BF),
('CÁCH DÙNG (3 bước)',Font(name=F,bold=True,size=11)),
('1. Sheet "Danh mục nguyên liệu": ở cột G (nền vàng), chọn "Có" cho nguyên liệu bạn đang có hàng để bán.',BF),
('2. Sheet "Cơ hội bán hàng": ở cột J (nền vàng), chọn "Có" cho cặp khách hàng – nguyên liệu mà bạn ĐÃ bán.',BF),
('3. Lọc cột K "Trạng thái":',BF),
('   • "① CƠ HỘI – khách đang dùng, bạn có hàng, chưa bán": ưu tiên chào hàng ngay (bạn có hàng, khách đang mua của nhà cung cấp khác).',BF),
('   • "② Đề xuất mới – khách chưa dùng, đối thủ của khách đã dùng": giới thiệu như một ý tưởng phát triển sản phẩm (đối thủ cạnh tranh của khách đang dùng).',BF),
('   • "③ Khách dùng – bạn chưa có hàng": gợi ý mở rộng danh mục sản phẩm của bạn.',BF),
('   • "Đang bán": đã có giao dịch.',BF),
('   Sheet "Tổng hợp khách hàng" tự đếm số cơ hội ① và ② cho từng khách.',BF),('',BF),
('ĐỘ TIN CẬY NGUỒN (cột "Độ tin cậy")',Font(name=F,bold=True,size=11))]
r=1
for t,f in txt:
    c=ws.cell(r,1,t); c.font=f; c.alignment=WR; r+=1
for k in 'ABCD':
    c=ws.cell(r,1,RELTXT[k]+{'A':' – chính xác nhất (có %, mã INS, đúng thứ tự nhãn).','B':' – thường đúng, nhưng có thể là nhãn cũ hoặc bị cắt ngắn.','C':' – chỉ đáng tin ở mức CÓ/KHÔNG có nguyên liệu; không có %, thiếu phụ gia.','D':' – cần kiểm chứng; chỉ dùng để tham khảo hướng tiếp cận.'}[k])
    c.font=BF; c.fill=PatternFill('solid',fgColor=RELFILL[k]); c.alignment=WR; r+=1
r+=1
for t in ['LƯU Ý ĐỘ CHÍNH XÁC',
 '• Mỗi dòng ở sheet "Sản phẩm & nguồn" có cột "Ghi chú độ chính xác": danh sách bị cắt, nhà bán lẻ tự phân nhóm, OCR, không ghi nơi sản xuất, và các trường hợp NGUỒN KHÔNG THỐNG NHẤT (cùng SKU nhưng hai nguồn ghi khác nhau – thường do đổi công thức).',
 '• Chỉ giữ hàng ghi "Sản xuất tại Việt Nam" (hoặc thương hiệu nội địa không ghi nơi sản xuất). Hàng nhập khẩu nguyên lon (VD: Abbott Similac, Ensure) bị loại vì không mua nguyên liệu tại nhà máy VN.',
 '• Số "SKU" là số sản phẩm khác nhau sau khi gộp cùng sản phẩm ở nhiều nguồn/quy cách; việc gộp dựa trên tên nên có thể còn trùng hoặc gộp nhầm.',
 '• Nguyên liệu "không ghi rõ" (VD: dầu thực vật, sữa bột) nghĩa là nhãn không nói loại cụ thể – đây cũng là cơ hội để hỏi khách đang dùng loại nào.',
 '• Website Vinamilk, TH, Nestlé, Dalatmilk, Nutricare chặn truy cập tự động – dữ liệu các hãng này chủ yếu đến từ nhà bán lẻ.',
 '• Mã phụ gia (INS) được nhận diện tự động; hãy mở link nguồn để kiểm tra trước khi gửi cho khách.']:
    c=ws.cell(r,1,t); c.font=BB if t.isupper() else BF; c.alignment=WR; r+=1
ws.column_dimensions['A'].width=140
# ======== data prep
skus={}   # (customer, sku_id) -> dict(name, rel, ings{name:bestrel})
order='ABCD'
for x in recs:
    k=(x['customer'],x['sku_id'])
    d=skus.setdefault(k,{'name':x['product'],'rel':x['rel'],'ings':{}})
    if order.index(x['rel'])<order.index(d['rel']): d['rel']=x['rel']; d['name']=x['product']
    for n in x['ings']:
        if n not in d['ings'] or order.index(x['rel'])<order.index(d['ings'][n]): d['ings'][n]=x['rel']
pair={}  # (cust,ing) -> [count, bestrel, examples]
for (c,sid),d in skus.items():
    for n,rl in d['ings'].items():
        p=pair.setdefault((c,n),[0,'D',[]]); p[0]+=1
        if order.index(rl)<order.index(p[1]): p[1]=rl
        if len(p[2])<3: p[2].append(d['name'])
# ======== 6 Chi tiết (long table used by formulas)
wd=wb.create_sheet('Chi tiết SKU-nguyên liệu')
title(wd,'CHI TIẾT: MỖI DÒNG = 1 SKU × 1 NGUYÊN LIỆU','Bảng nguồn cho các công thức đếm. Không cần sửa.')
hdr(wd,3,['Khách hàng','Mã SKU','Sản phẩm','Nhóm nguyên liệu','Nguyên liệu','Độ tin cậy'],[18,10,60,22,40,10])
r=4
for (c,sid),d in sorted(skus.items()):
    for n in sorted(d['ings'],key=norm.ORDER.index):
        for j,v in enumerate([c,sid,d['name'],norm.GROUP[n],n,d['ings'][n]],1): wd.cell(r,j,v).font=BF
        r+=1
DL=r-1; wd.auto_filter.ref=f'A3:F{DL}'; wd.freeze_panes='A4'
CT="'Chi tiết SKU-nguyên liệu'"
# ======== 3 Danh mục nguyên liệu
wm=wb.create_sheet('Danh mục nguyên liệu',1)
title(wm,'DANH MỤC NGUYÊN LIỆU (CHUẨN HÓA)','Cột G (nền vàng): chọn "Có" nếu bạn có hàng để bán. Cột E–F tự đếm từ dữ liệu.')
hdr(wm,3,['STT','Nhóm','Nguyên liệu (chuẩn hóa)','Tên tiếng Anh / thương mại','Số khách đang dùng','Số SKU đang dùng','Bạn có bán? (Có/Không)','Ghi chú của bạn'],[6,24,44,34,12,12,14,40])
dv=DataValidation(type='list',formula1='"Có,Không"',allow_blank=True); wm.add_data_validation(dv)
for i,n in enumerate(norm.ORDER,1):
    rr=i+3
    put(wm,rr,[i,norm.GROUP[n],n,norm.EN[n],
        f'=SUMPRODUCT(--(\'Cơ hội bán hàng\'!$C$4:$C$5000=C{rr}),--(\'Cơ hội bán hàng\'!$E$4:$E$5000>0))',
        f'=COUNTIF({CT}!$E$4:$E${DL},C{rr})',None,None])
    g=wm.cell(rr,7); g.fill=YEL; g.font=INP; dv.add(g)
ML=len(norm.ORDER)+3; wm.freeze_panes='D4'; wm.auto_filter.ref=f'A3:H{ML}'
wm.conditional_formatting.add(f'E4:F{ML}',ColorScaleRule(start_type='num',start_value=0,start_color='FFFFFF',end_type='max',end_color='5B9BD5'))
# ======== 4 Cơ hội bán hàng
wo=wb.create_sheet('Cơ hội bán hàng',1)
title(wo,'CƠ HỘI BÁN HÀNG THEO KHÁCH HÀNG × NGUYÊN LIỆU','Cột J (nền vàng): chọn "Có" nếu đã bán nguyên liệu này cho khách. Lọc cột K để xem cơ hội. Cột E, I, K tự tính.')
hdr(wo,3,['Khách hàng','Nhóm','Nguyên liệu','Tên tiếng Anh','Số SKU khách đang dùng','Số khách khác đang dùng','Độ tin cậy cao nhất','Ví dụ SKU (tối đa 3)','Bạn có bán?','Đã bán cho khách này? (Có/Không)','Trạng thái','Ghi chú độ chính xác'],[18,20,38,28,11,11,11,60,10,14,40,46])
dv2=DataValidation(type='list',formula1='"Có,Không"',allow_blank=True); wo.add_data_validation(dv2)
r=4
for c in CUSTS:
    for n in norm.ORDER:
        p=pair.get((c,n))
        others=sum(1 for c2 in CUSTS if c2!=c and (c2,n) in pair)
        if not p and others==0: continue
        note=''
        if p and p[1]=='C': note='Chỉ thấy ở nguồn độ tin cậy C – kiểm tra lại nhãn.'
        if p and p[1]=='D': note='Chỉ thấy qua kết quả tìm kiếm – cần kiểm chứng.'
        if p and 'không ghi rõ' in n: note=(note+' ' if note else '')+'Nhãn không ghi loại cụ thể – hỏi khách đang dùng loại nào.'
        if not p: note='Chưa thấy trong dữ liệu công khai của khách (có thể khách có dùng nhưng nguồn không ghi).'
        vals=[c,norm.GROUP[n],n,norm.EN[n],f'=COUNTIFS({CT}!$A$4:$A${DL},A{r},{CT}!$E$4:$E${DL},C{r})',
              f'=SUMPRODUCT(--($C$4:$C$5000=C{r}),--($A$4:$A$5000<>A{r}),--($E$4:$E$5000>0))',
              p[1] if p else '—','; '.join(p[2]) if p else '',
              f"=IFERROR(INDEX('Danh mục nguyên liệu'!$G$4:$G${ML},MATCH(C{r},'Danh mục nguyên liệu'!$C$4:$C${ML},0)),\"\")",None,
              f'=IF(E{r}>0,IF(J{r}="Có","Đang bán",IF(I{r}="Có","① CƠ HỘI – khách đang dùng, bạn có hàng, chưa bán","③ Khách dùng – bạn chưa có hàng")),IF(AND(I{r}="Có",F{r}>0),"② Đề xuất mới – khách chưa dùng, đối thủ đã dùng",""))',note]
        put(wo,r,vals)
        if p: wo.cell(r,7).fill=PatternFill('solid',fgColor=RELFILL[p[1]])
        j=wo.cell(r,10); j.fill=YEL; j.font=INP; dv2.add(j)
        r+=1
OL=r-1; wo.freeze_panes='D4'; wo.auto_filter.ref=f'A3:L{OL}'
for t,col in [('①','F8CBAD'),('②','FFE699'),('Đang bán','C6EFCE')]:
    wo.conditional_formatting.add(f'K4:K{OL}',FormulaRule(formula=[f'ISNUMBER(SEARCH("{t}",K4))'],fill=PatternFill('solid',fgColor=col)))
# fix SUMPRODUCT ranges to real size
for row in wo.iter_rows(min_row=4,max_row=OL,min_col=6,max_col=6):
    for c in row: c.value=c.value.replace('5000',str(OL))
for row in wm.iter_rows(min_row=4,max_row=ML,min_col=5,max_col=5):
    for c in row: c.value=c.value.replace('5000',str(OL))
# ======== 2 Tổng hợp khách hàng
wt=wb.create_sheet('Tổng hợp khách hàng',1)
title(wt,'TỔNG HỢP THEO KHÁCH HÀNG','Tự tính. Cột G–H cập nhật khi bạn điền "Có" ở Danh mục nguyên liệu và Cơ hội bán hàng.')
hdr(wt,3,['Khách hàng','Số SKU có dữ liệu','SKU độ tin cậy A/B','SKU chỉ C/D','Số nguyên liệu khác nhau đang dùng','Đang bán','① Cơ hội (có hàng, chưa bán)','② Đề xuất mới','③ Khách dùng – bạn chưa có hàng','Nguồn dữ liệu chính'],[20,12,12,12,14,10,14,12,14,60])
srcs={}
for x in recs: srcs.setdefault(x['customer'],set()).add(x['source'])
CO="'Cơ hội bán hàng'"
for i,c in enumerate(CUSTS):
    rr=i+4; ab=sum(1 for (cc,s),d in skus.items() if cc==c and d['rel'] in 'AB'); cd=sum(1 for (cc,s),d in skus.items() if cc==c and d['rel'] in 'CD')
    put(wt,rr,[c,ab+cd,ab,cd,f'=COUNTIFS({CO}!$A$4:$A${OL},A{rr},{CO}!$E$4:$E${OL},">0")',
        f'=COUNTIFS({CO}!$A$4:$A${OL},A{rr},{CO}!$K$4:$K${OL},"Đang bán")',
        f'=COUNTIFS({CO}!$A$4:$A${OL},A{rr},{CO}!$K$4:$K${OL},"①*")',
        f'=COUNTIFS({CO}!$A$4:$A${OL},A{rr},{CO}!$K$4:$K${OL},"②*")',
        f'=COUNTIFS({CO}!$A$4:$A${OL},A{rr},{CO}!$K$4:$K${OL},"③*")','; '.join(sorted(srcs.get(c,[])))])
TR=len(CUSTS)+4; put(wt,TR,['TỔNG']+[f'=SUM({L(j)}4:{L(j)}{TR-1})' for j in range(2,10)]+[''],BB)
wt.freeze_panes='B4'
# ======== 5 Ma trận
wx=wb.create_sheet('Ma trận nguyên liệu')
title(wx,'MA TRẬN: SỐ SKU DÙNG NGUYÊN LIỆU, THEO KHÁCH HÀNG','Ô trống = chưa thấy trong dữ liệu công khai. Tự tính từ sheet Chi tiết.')
hdr(wx,3,['Nhóm','Nguyên liệu']+CUSTS+['Số khách'],[20,38]+[10]*len(CUSTS)+[9])
for i,n in enumerate(norm.ORDER):
    rr=i+4; wx.cell(rr,1,norm.GROUP[n]).font=BF; wx.cell(rr,2,n).font=BF
    for j,c in enumerate(CUSTS,3):
        x=wx.cell(rr,j,f'=COUNTIFS({CT}!$A$4:$A${DL},{L(j)}$3,{CT}!$E$4:$E${DL},$B{rr})'); x.font=BF; x.number_format='0;-0;""'
    k=len(CUSTS)+3; x=wx.cell(rr,k,f'=COUNTIF(C{rr}:{L(k-1)}{rr},">0")'); x.font=BB
    for j in range(1,k+1): wx.cell(rr,j).border=BOX
XL=len(norm.ORDER)+3
wx.conditional_formatting.add(f'C4:{L(len(CUSTS)+2)}{XL}',ColorScaleRule(start_type='num',start_value=0,start_color='FFFFFF',end_type='max',end_color='5B9BD5'))
wx.freeze_panes='C4'
# ======== 7 Sản phẩm & nguồn
wp=wb.create_sheet('Sản phẩm & nguồn')
title(wp,'SẢN PHẨM & NGUỒN (MỖI DÒNG = 1 TRANG NGUỒN)','Thành phần chép nguyên văn từ nguồn. Cùng "Mã SKU" = cùng sản phẩm ở nhiều nguồn/quy cách.')
hdr(wp,3,['Khách hàng','Mã SKU','Sản phẩm','Ngành hàng','Nguồn','Độ tin cậy','Nơi sản xuất','Thành phần (nguyên văn từ nguồn)','Nguyên liệu nhận diện được','Ghi chú độ chính xác','Link nguồn'],[16,9,48,20,26,9,12,80,50,50,30])
r=4
for x in sorted(recs,key=lambda x:(CUSTS.index(x['customer']),x['sku_id'],'ABCD'.index(x['rel']))):
    put(wp,r,[x['customer'],x['sku_id'],x['product'],x['cat'],x['source'],x['rel'],x['made'],x['ing'] or '—','; '.join(x['ings']),' '.join(x['notes']),x['url'] or '—'])
    wp.cell(r,6).fill=PatternFill('solid',fgColor=RELFILL[x['rel']])
    if x['url']: wp.cell(r,11).hyperlink=x['url']; wp.cell(r,11).font=LINK
    if 'KHÔNG THỐNG NHẤT' in ' '.join(x['notes']): wp.cell(r,10).fill=PatternFill('solid',fgColor='F8CBAD')
    r+=1
wp.freeze_panes='D4'; wp.auto_filter.ref=f'A3:K{r-1}'
# ======== 8 Nguồn dữ liệu
wn=wb.create_sheet('Nguồn dữ liệu')
title(wn,'CÁC NGUỒN ĐÃ THỬ','Nguồn nào bị chặn thì ghi rõ để bạn tự mở trên máy nếu cần.')
hdr(wn,3,['Nguồn','Loại','Độ tin cậy','Kết quả','Ghi chú'],[34,22,10,16,80])
from collections import Counter
cnt=Counter(x['source'] for x in recs)
rows=[('dutchlady.com.vn – hồ sơ công bố PDF','Website hãng','A','Đã dùng','FrieslandCampina: hồ sơ cho từng SKU, đọc bằng OCR.'),
('hanoimilk.com + Google Drive','Website hãng','A','Đã dùng','Thành phần trên trang sản phẩm + hồ sơ công bố sữa chua.'),
('nutifood.com.vn, vitadairy.vn','Website hãng','C','Một phần','Chỉ có bảng dinh dưỡng, không có danh sách nguyên liệu.'),
('vinamilk.com.vn, thmilk.vn, nestle.com.vn, dalatmilk.vn, nutricare.com.vn, mocchaumilk.com','Website hãng','—','Bị chặn','Chặn truy cập tự động (403 / kiểm tra chống bot / ngắt kết nối). Vinamilk có kho bản tự công bố: vinamilk.com.vn/cong-bo-san-pham – nên mở trên máy của bạn.'),
('lof.vn','Website hãng','—','Không có dữ liệu','Chỉ giới thiệu thương hiệu.'),
('Pharmacity','Nhà bán lẻ','B','Đã dùng','Có nơi sản xuất + thành phần; ít SKU sữa nội địa.'),
('Thế Giới Sữa (thegioisua.com)','Nhà bán lẻ chuyên sữa','C','Đã dùng','Nhiều SKU nhất; thành phần được nhà bán lẻ phân nhóm lại, không có %.'),
('Kingfoodmart','Siêu thị','B','Đã dùng','Thành phần nguyên văn; không ghi nhà sản xuất.'),
('Sữa Cho Bé Yêu (suachobeyeu.vn)','Nhà bán lẻ chuyên sữa','B','Đã dùng',''),
('Medigo','Nhà thuốc online','B','Đã dùng','Chủ yếu sữa bột / dinh dưỡng y học.'),
('LOTTE Mart, Thế Giới Sữa, KidsPlaza… (qua tìm kiếm)','Tìm kiếm web','D','Đã dùng','Đoạn tóm tắt của công cụ tìm kiếm – cần kiểm chứng.'),
('Long Châu, Con Cưng, Bách Hóa Xanh','Nhà bán lẻ','—','Bị chặn','Chặn truy cập tự động.'),
('KidsPlaza, LOTTE Mart (truy cập trực tiếp)','Nhà bán lẻ','—','Chưa dùng','Sitemap không liệt kê sản phẩm / trang tải bằng JavaScript.'),
('Cổng dịch vụ công ATTP (Cục ATTP)','Cơ quan nhà nước','A','Chưa dùng','Hồ sơ tự công bố có thể tra cứu thủ công trên cổng của Cục ATTP / Sở Y tế tỉnh – nguồn chính xác nhất nếu cần đối chiếu SKU cụ thể.')]
for i,row in enumerate(rows,4): put(wn,i,list(row))
for w in wb.worksheets: w.sheet_view.zoomScale=90
wb.save(OUT); print('saved',OUT,'detail rows',DL-3,'opp rows',OL-3,'skus',len(skus))

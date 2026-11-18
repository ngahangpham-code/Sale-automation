import json,sys
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table,TableStyleInfo
rows=json.load(open(sys.argv[1],encoding='utf-8')); OUT=sys.argv[2]
F='Arial'; HF=Font(name=F,bold=True,color='FFFFFF',size=10); HFILL=PatternFill('solid',fgColor='1F4E79')
BF=Font(name=F,size=10); LINK=Font(name=F,size=10,color='0563C1',underline='single')
WR=Alignment(wrap_text=True,vertical='top'); thin=Side(style='thin',color='BFBFBF'); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)
STATUS_FILL={'Danh sách nguyên liệu':'E2EFDA','Hoạt chất nổi bật':'FFF2CC','Có hồ sơ':'FCE4D6','Chưa truy cập':'EDEDED','Trang sản phẩm không':'EDEDED'}
def hdr(ws,r,cols,widths):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        x=ws.cell(r,i,c); x.font=HF; x.fill=HFILL; x.alignment=Alignment(wrap_text=True,vertical='center'); x.border=BOX
        ws.column_dimensions[get_column_letter(i)].width=w
wb=Workbook()
# ---------------- Sheet 1: Tổng quan
ws=wb.active; ws.title='Tổng quan'
P='Sản phẩm - Thành phần'
lines=[('BÁO CÁO NHÀ SẢN XUẤT SỮA TẠI VIỆT NAM – SẢN PHẨM & THÀNH PHẦN NGUYÊN LIỆU',Font(name=F,bold=True,size=14,color='1F4E79')),
('Ngày lập: 17/11/2026 · Cập nhật: 18/11/2026 · Dành cho: Technical Sales – Dairy & Nutrition',Font(name=F,italic=True,size=10)),
('',BF),
('PHẠM VI',Font(name=F,bold=True,size=11)),
('• 11 doanh nghiệp sản xuất sữa / dinh dưỡng từ sữa có nhà máy tại Việt Nam (không gồm sữa đậu nành như Vinasoy và hàng nhập khẩu nguyên chiếc).',BF),
('• Với mỗi sản phẩm: tên, ngành hàng, thành phần nguyên liệu theo công bố trên website chính thức và link tới hồ sơ công bố sản phẩm.',BF),
('',BF),
('CÁCH ĐỌC CỘT "LOẠI DỮ LIỆU" (sheet Sản phẩm - Thành phần)',Font(name=F,bold=True,size=11)),
('Danh sách nguyên liệu (hồ sơ công bố) – trích từ Bản tự công bố sản phẩm (PDF scan, đọc bằng OCR). Nên đối chiếu file gốc trước khi dùng cho tài liệu chính thức.','E2EFDA'),
('Danh sách nguyên liệu (trang sản phẩm) – chép từ mục Thành phần trên trang sản phẩm của hãng.','E2EFDA'),
('Danh sách nguyên liệu (nhà bán lẻ …) – lấy từ trang nhà bán lẻ (Pharmacity, LOTTE Mart, Thế Giới Sữa…) hoặc Hiệp hội Sữa VN khi website hãng chặn truy cập. Độ tin cậy thấp hơn hồ sơ công bố – nên đối chiếu nhãn.','E2EFDA'),
('Hoạt chất nổi bật (theo bảng dinh dưỡng) – hãng chỉ đăng bảng giá trị dinh dưỡng; cột thành phần liệt kê hoạt chất/vi chất có trong bảng (không phải danh sách nguyên liệu đầy đủ).','FFF2CC'),
('Có hồ sơ công bố – chưa trích được – có link hồ sơ, cần mở file để xem thành phần.','FCE4D6'),
('Chưa truy cập được website – website chặn truy cập tự động từ máy chủ cloud; mới có danh mục thương hiệu.','EDEDED'),
('',BF),
('TÓM TẮT SỐ LIỆU (tự tính từ dữ liệu)',Font(name=F,bold=True,size=11)),
]
r=1
for t,f in lines:
    c=ws.cell(r,1,t)
    if isinstance(f,str): c.font=BF; c.fill=PatternFill('solid',fgColor=f)
    else: c.font=f
    c.alignment=Alignment(wrap_text=True,vertical='top'); r+=1
stats=[('Số doanh nghiệp',f"=COUNT('Nhà sản xuất'!A4:A200)"),
('Tổng số dòng sản phẩm',f"=COUNTA('{P}'!E4:E1000)"),
('…trong đó có danh sách nguyên liệu',f"=COUNTIF('{P}'!F4:F1000,\"Danh sách nguyên liệu*\")"),
('…trong đó chỉ có hoạt chất nổi bật',f"=COUNTIF('{P}'!F4:F1000,\"Hoạt chất nổi bật*\")"),
('…trong đó chưa có thành phần',f"=B{r+1}-B{r+2}-B{r+3}")]
for k,v in stats:
    ws.cell(r,1,k).font=BF; c=ws.cell(r,2,v); c.font=Font(name=F,bold=True,size=10); r+=1
r+=1
ws.cell(r,1,'HẠN CHẾ & BƯỚC TIẾP THEO').font=Font(name=F,bold=True,size=11); r+=1
for t in ['• Website Vinamilk, TH true MILK, Mộc Châu Milk, Nestlé, Dalatmilk, LOF (Kun) và Nutricare chặn truy cập tự động (lỗi 403 / kiểm tra chống bot). Với các hãng này, thành phần các SKU chủ lực được lấy từ nhà bán lẻ (Pharmacity, LOTTE Mart…), và các SKU còn lại được gom thành dòng "Các SKU khác … chưa lấy được". Vinamilk có kho "Bản tự công bố sản phẩm" tại vinamilk.com.vn/cong-bo-san-pham, mở trên máy của bạn để bổ sung.',
          '• Nutifood và VitaDairy chỉ công bố bảng dinh dưỡng trên website; một số SKU VitaDairy có thêm danh sách nguyên liệu từ Pharmacity.',
          '• Dữ liệu OCR có thể còn sai chính tả nhỏ (VD: mã phụ gia INS). Kiểm tra lại với file PDF gốc (link cột H) trước khi trích dẫn cho khách hàng.',
          '• Thông tin nhà máy/sở hữu ở sheet "Nhà sản xuất" lấy từ báo chí và website công ty; nên xác minh lại khi dùng.']:
    c=ws.cell(r,1,t); c.font=BF; c.alignment=Alignment(wrap_text=True,vertical='top'); r+=1
ws.column_dimensions['A'].width=120; ws.column_dimensions['B'].width=12
# ---------------- Sheet 3 first (data) so formulas reference it
wp=wb.create_sheet(P)
wp['A1']='SẢN PHẨM & THÀNH PHẦN NGUYÊN LIỆU THEO CÔNG BỐ CỦA NHÀ SẢN XUẤT'; wp['A1'].font=Font(name=F,bold=True,size=13,color='1F4E79')
wp['A2']='Dùng bộ lọc ở dòng tiêu đề để lọc theo công ty / ngành hàng / loại dữ liệu. Màu nền cột F = mức độ đầy đủ của dữ liệu (xem sheet Tổng quan).'; wp['A2'].font=Font(name=F,italic=True,size=9)
cols=['STT','Công ty','Thương hiệu','Ngành hàng','Sản phẩm','Loại dữ liệu','Thành phần nguyên liệu / hoạt chất (theo công bố)','Nguồn (trang/hồ sơ)','Hồ sơ công bố sản phẩm','Ghi chú']
hdr(wp,3,cols,[6,30,18,24,42,26,90,30,30,40])
order={'CTCP Sữa Việt Nam (Vinamilk)':0,'FrieslandCampina Việt Nam':1,'CTCP Sữa TH (TH Group)':2,'Nutifood (CTCP Thực phẩm Dinh dưỡng Nutifood Bình Dương)':3}
rows.sort(key=lambda x:(order.get(x['company'],9),x['company'],x['brand'],x['product']))
for i,x in enumerate(rows,1):
    rr=i+3
    vals=[i,x['company'],x['brand'],x['cat'],x['product'],x['dtype'],x['ing'] or '—',x['src'],x['decl'],x['note']]
    for j,v in enumerate(vals,1):
        c=wp.cell(rr,j,v); c.font=BF; c.alignment=WR; c.border=BOX
    for j in (8,9):
        c=wp.cell(rr,j)
        if c.value: c.hyperlink=c.value; c.font=LINK
        else: c.value='—'
    for k,col in STATUS_FILL.items():
        if x['dtype'].startswith(k): wp.cell(rr,6).fill=PatternFill('solid',fgColor=col)
last=len(rows)+3
wp.freeze_panes='F4'; wp.auto_filter.ref=f'A3:J{last}'
# ---------------- Sheet 2: Nhà sản xuất
wc=wb.create_sheet('Nhà sản xuất',1)
wc['A1']='DANH SÁCH NHÀ SẢN XUẤT SỮA TẠI VIỆT NAM'; wc['A1'].font=Font(name=F,bold=True,size=13,color='1F4E79')
wc['A2']='Cột H–I tự đếm từ sheet "Sản phẩm - Thành phần". Thông tin nhà máy/sở hữu lấy từ báo chí và website công ty – nên xác minh lại.'; wc['A2'].font=Font(name=F,italic=True,size=9)
cc=['STT','Công ty','Thương hiệu chính','Ngành hàng chính','Nhà máy / vùng nguyên liệu (thông tin công khai)','Website chính thức','Trạng thái dữ liệu website','Số dòng SP trong báo cáo','Số dòng có DS nguyên liệu','Nguồn tham khảo']
hdr(wc,3,cc,[6,34,34,30,40,28,34,12,12,45])
comp=[
('CTCP Sữa Việt Nam (Vinamilk)','Vinamilk, Ông Thọ, Ngôi Sao Phương Nam, Susu, Probi, Optimum, Dielac, Yoko, Green Farm','Sữa nước, sữa chua, sữa đặc, sữa bột, dinh dưỡng','Nhiều nhà máy & trang trại trong nước; công ty mẹ của Mộc Châu Milk (qua GTNfoods)','https://www.vinamilk.com.vn','Website chặn bot (403); bổ sung 7 SKU từ Pharmacity/nhà bán lẻ; có kho bản tự công bố tại /cong-bo-san-pham','https://www.vinamilk.com.vn/cong-bo-san-pham/'),
('FrieslandCampina Việt Nam','Dutch Lady (Cô Gái Hà Lan), Fristi, Yomost, Hoàn Hảo, Trường Sinh','Sữa nước, sữa chua uống, sữa đặc/kem đặc, sữa bột','Theo báo chí: nhà máy tại Bình Dương và Hà Nam (cần xác minh)','https://www.dutchlady.com.vn','Đầy đủ: có hồ sơ công bố PDF cho từng SKU','https://www.dutchlady.com.vn/san-pham/sua-tuoi-dutch-lady'),
('CTCP Sữa TH (TH Group)','TH true MILK, TH true YOGURT, TH true OAT, TH true NUT','Sữa tươi, sữa chua, sữa hạt','Trang trại & nhà máy tại Nghĩa Đàn, Nghệ An','https://www.thmilk.vn','Website chặn bot; bổ sung 2 SKU từ Pharmacity/nhà bán lẻ','https://lsvn.vn/giai-phap-dinh-duong-tien-phong-cho-tung-nhom-tuoi-tu-th-true-milk1665051137-a124862.html'),
('Nutifood (CTCP Thực phẩm Dinh dưỡng Nutifood Bình Dương)','GrowPLUS+, NuVi, Värna, NutiMilk, Famna','Sữa bột trẻ em/người lớn, sữa nước, sữa chua, ngũ cốc','Website ghi GrowPLUS+ sản xuất tại Singapore; trang trại NutiMilk trong nước','https://nutifood.com.vn','Một phần: chỉ có bảng dinh dưỡng','https://nutifood.com.vn/en/brands/growplus'),
('CTCP VitaDairy Việt Nam','ColosBaby, Oggi, CaloSure, Calokid, Colos, Vitagrow, Nepro, Gluvita, Fohepta','Sữa bột trẻ em (sữa non), dinh dưỡng y học, sữa pha sẵn','Chưa xác minh','https://vitadairy.vn','Một phần: bảng dinh dưỡng trên website + 3 SKU có DS nguyên liệu từ Pharmacity','https://vitadairy.vn/san-pham.html'),
('CTCP Sữa Hà Nội (Hanoimilk)','IZZI, Yotuti, Hanoimilk','Sữa tiệt trùng, sữa uống dinh dưỡng, sữa chua, thức uống sữa trái cây/thạch','Hà Nội','https://hanoimilk.com','Đầy đủ: thành phần trên trang SP + 8 hồ sơ công bố sữa chua (Google Drive, OCR)','https://hanoimilk.com/blogs/tong-hop-thong-tin-cong-bo-san-pham'),
('CTCP Giống bò sữa Mộc Châu (Mộc Châu Milk – thuộc Vinamilk/GTNfoods)','Mộc Châu Milk, Yo-Pro, Mộc Châu Creamery','Sữa tươi thanh/tiệt trùng, sữa chua','Mộc Châu, Sơn La','https://www.mocchaumilk.com','Website không kết nối được; bổ sung 3 SKU từ nhà bán lẻ / Hiệp hội Sữa VN','https://tuoitre.vn/moc-chau-milk-ra-mat-sua-tuoi-bich-giay-moi-tron-dinh-duong-them-tiet-kiem-2020100610253834.htm'),
('CTCP Sữa Quốc tế LOF (tên cũ IDP)','Kun, LOF Ba Vì, LiF (Love\'in Farm), Malto','Sữa tươi, sữa chua, thức uống sữa trẻ em','3 nhà máy: Chương Mỹ, Ba Vì (Hà Nội) và Củ Chi (TP.HCM)','https://lof.vn','Website chỉ giới thiệu thương hiệu; bổ sung 2 SKU Kun từ nhà bán lẻ','https://tuoitre.vn/sua-lof-ba-vi-trinh-lang-dien-mao-moi-huong-vi-khong-doi-20220924135303665.htm'),
('Công ty TNHH Nestlé Việt Nam','MILO (uống liền), Nestlé','Thức uống lúa mạch – sữa UHT','Nhà máy Bình An (Đồng Nai) và Bông Sen (Hưng Yên) sản xuất MILO','https://www.nestle.com.vn','Website chặn bot (403); MILO hộp 180ml lấy từ Pharmacity (SX tại VN)','https://www.brandsvietnam.com/12578-Nestle-khai-truong-nha-may-san-xuat-MILO-o-Hung-Yen'),
('CTCP Nutricare','Metacare, Glucare Gold, Nutricare Gold, Smarta IQ, Care 100','Sữa bột, dinh dưỡng y học, sữa nước','Nhà máy sữa bột (2010, mở rộng 2017) và nhà máy sữa nước (2019); địa điểm cần xác minh','https://nutricare.com.vn','Website chặn bot (403); bổ sung 3 SKU từ nhà bán lẻ (danh sách rút gọn)','https://nutricare.com.vn/en/?p=22813'),
('Dalatmilk (thuộc TH Group)','Dalatmilk, Dalatmilk Cool C','Sữa tươi thanh/tiệt trùng, sữa chua, thức uống sữa chua lên men','Trang trại & nhà máy tại Đơn Dương, Lâm Đồng','https://dalatmilk.vn','Website chặn bot (403); bổ sung 1 SKU từ nhà bán lẻ','https://tienphong.vn/thuc-uong-sua-chua-len-men-dau-dalatmilk-cool-c-vua-ra-mat-co-gi-dac-biet-post1853851.tpo'),
]
for i,(n,b,cat,fac,web,st,src) in enumerate(comp,1):
    rr=i+3
    vals=[i,n,b,cat,fac,web,st,f"=COUNTIF('{P}'!$B$4:$B${last},B{rr})",f"=COUNTIFS('{P}'!$B$4:$B${last},B{rr},'{P}'!$F$4:$F${last},\"Danh sách nguyên liệu*\")",src]
    for j,v in enumerate(vals,1):
        c=wc.cell(rr,j,v); c.font=BF; c.alignment=WR; c.border=BOX
    for j in (6,10): c=wc.cell(rr,j); c.hyperlink=c.value; c.font=LINK
tr=len(comp)+4
wc.cell(tr,2,'TỔNG').font=Font(name=F,bold=True,size=10)
for j in (8,9):
    L=get_column_letter(j); c=wc.cell(tr,j,f'=SUM({L}4:{L}{tr-1})'); c.font=Font(name=F,bold=True,size=10); c.border=BOX
wc.freeze_panes='C4'
# ---------------- Sheet 4: Ma trận nguyên liệu
wm=wb.create_sheet('Ma trận nguyên liệu')
wm['A1']='MA TRẬN NGUYÊN LIỆU: SỐ SẢN PHẨM CÓ CHỨA TỪ KHÓA, THEO CÔNG TY'; wm['A1'].font=Font(name=F,bold=True,size=13,color='1F4E79')
wm['A2']='Đếm số dòng ở sheet "Sản phẩm - Thành phần" có cột G chứa từ khóa ở cột B (không phân biệt hoa thường). Sửa/thêm từ khóa ở cột B (ô nền vàng) để tự tính lại.'; wm['A2'].font=Font(name=F,italic=True,size=9)
mcomp=[c[0] for c in comp]
short=['Vinamilk','FrieslandCampina','TH','Nutifood','VitaDairy','Hanoimilk','Mộc Châu','LOF','Nestlé','Nutricare','Dalatmilk']
hdr(wm,3,['Nhóm','Nguyên liệu / hoạt chất (từ khóa)']+short+['Tổng'],[20,30]+[11]*len(short)+[9])
for j,n in enumerate(mcomp,3):
    c=wm.cell(4,j,n); c.font=Font(name=F,size=8,color='808080'); c.alignment=WR
wm.cell(4,1,'(tên công ty đầy đủ dùng cho công thức →)').font=Font(name=F,size=8,italic=True,color='808080')
keys=[('Nền sữa','sữa tươi'),('Nền sữa','sữa gầy'),('Nền sữa','nguyên kem'),('Nền sữa','whey'),('Nền sữa','buttermilk'),('Nền sữa','chất béo sữa'),('Nền sữa','sữa chua lên men'),('Nền sữa','lactose'),('Nền sữa','lactoza'),('Nền sữa','caseinat'),('Đạm thực vật','đậu nành'),
('Carbohydrate','đường'),('Carbohydrate','maltodextrin'),('Carbohydrate','fructose'),('Chất béo','dầu thực vật'),('Chất béo','dầu cá'),('Chất béo','MCT'),
('Phụ gia','chất ổn định'),('Phụ gia','gelatin'),('Phụ gia','chất bảo quản'),('Phụ gia','chất nhũ hóa'),('Phụ gia','471'),('Phụ gia','407'),('Phụ gia','412'),('Phụ gia','460'),('Phụ gia','466'),('Phụ gia','440'),('Phụ gia','1442'),('Phụ gia','452'),('Phụ gia','chất điều chỉnh độ axit'),
('Phụ gia','hương liệu'),('Phụ gia','chất tạo màu'),('Phụ gia','960'),('Phụ gia','sucralose'),
('Vi chất','vitamin'),('Vi chất','khoáng chất'),('Vi chất','tricalci phosphat'),('Vi chất','DHA'),('Vi chất','Lysine'),('Vi chất','Choline'),('Vi chất','Taurine'),('Vi chất','Vitamin K2'),
('Hoạt chất chức năng',"2'-FL"),('Hoạt chất chức năng','FOS'),('Hoạt chất chức năng','GOS'),('Hoạt chất chức năng','Lacto-N-tetraose'),('Men / vi sinh','Streptococcus'),('Men / vi sinh','Lactobacillus'),('Hoạt chất chức năng','Inulin'),('Hoạt chất chức năng','sữa non'),('Hoạt chất chức năng','Lactoferrin'),('Hoạt chất chức năng','Probiotic'),('Hoạt chất chức năng','Postbiotic'),('Hoạt chất chức năng','HMB'),('Hoạt chất chức năng','Isomaltulose'),('Hoạt chất chức năng','palatinose'),('Hoạt chất chức năng','collagen'),
('Khác','nước ép trái cây'),('Khác','thạch dừa'),('Khác','cacao'),('Khác','yến mạch')]
YEL=PatternFill('solid',fgColor='FFFF00')
for i,(g,k) in enumerate(keys):
    rr=5+i
    wm.cell(rr,1,g).font=BF
    c=wm.cell(rr,2,k); c.font=Font(name=F,size=10,color='0000FF'); c.fill=YEL
    for j in range(3,3+len(mcomp)):
        L=get_column_letter(j)
        c=wm.cell(rr,j,f"=COUNTIFS('{P}'!$B$4:$B${last},{L}$4,'{P}'!$G$4:$G${last},\"*\"&$B{rr}&\"*\")"); c.font=BF; c.number_format='0;-0;"-"'
    c=wm.cell(rr,3+len(mcomp),f'=SUM(C{rr}:{get_column_letter(2+len(mcomp))}{rr})'); c.font=Font(name=F,bold=True,size=10); c.number_format='0;-0;"-"'
    for j in range(1,4+len(mcomp)): wm.cell(rr,j).border=BOX
wm.freeze_panes='C5'
from openpyxl.formatting.rule import ColorScaleRule
wm.conditional_formatting.add(f'C5:{get_column_letter(2+len(mcomp))}{4+len(keys)}',ColorScaleRule(start_type='num',start_value=0,start_color='FFFFFF',end_type='max',end_color='5B9BD5'))
for w in wb.worksheets: w.sheet_view.zoomScale=90
wb.save(OUT); print('saved',OUT,last)

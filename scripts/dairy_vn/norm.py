# Ingredient dictionary + customer mapping shared by the build scripts.
import re
N=r'(?:INS|E)?\s?'            # optional INS/E prefix
def ins(code):                 # an INS number in an ingredient list, not a quantity
    return r'(?:(?:INS|E)\s?%s|(?<=[\(,;\s])%s)(?:\s?\(i+\)|[a-z])?(?![\d.,]?\d)(?!\s?(?:mg|g|ml|kcal|IU|µg|mcg|%%))'%(code,code)
# (group, canonical VN name, English/trade name, regex)
ING=[
('Nền sữa','Sữa tươi / sữa bò tươi','Fresh milk',r'sữa (?:bò )?tươi(?! cô đặc)|fresh milk|sữa tươi nguyên chất'),
('Nền sữa','Sữa tươi cô đặc (nhập khẩu)','Concentrated fresh milk',r'sữa tươi cô đặc'),
('Nền sữa','Sữa bột gầy (SMP)','Skim milk powder',r'(?:bột )?sữa (?:bột )?gầy|sữa bột tách béo|skim(?:med)? milk'),
('Nền sữa','Sữa bột nguyên kem (WMP)','Whole milk powder',r'nguyên kem|whole milk powder|full cream'),
('Nền sữa','Sữa bột (không ghi rõ loại)','Milk powder (unspecified)',r'sữa bột|bột sữa|milk powder'),
('Nền sữa','Whey protein cô đặc (WPC)','Whey protein concentrate',r'whey protein concentrate|đạm whey cô đặc|whey cô đặc|\bWPC'),
('Nền sữa','Whey giàu alpha-lactalbumin','Alpha-lactalbumin enriched whey',r'alpha-?lactalbumin'),
('Nền sữa','Whey protein thủy phân / phân lập','Hydrolysed / isolated whey',r'whey[^,]{0,25}(?:thủy phân|phân lập|isolate|hydroly)|(?:thủy phân|phân lập)[^,]{0,10}whey'),
('Nền sữa','Bột whey / whey (khác)','Whey powder',r'\bwhey'),
('Nền sữa','Bột buttermilk (sữa tách bơ)','Buttermilk powder',r'buttermilk|tách bơ'),
('Nền sữa','Chất béo sữa / AMF / kem sữa','Milk fat / AMF / cream',r'chất béo (?:từ )?sữa|milk fat|\bAMF\b|kem sữa|bơ sữa|anhydrous'),
('Nền sữa','Lactose','Lactose',r'lactos|lactoza'),
('Nền sữa','Casein / caseinat','Caseinate',r'casein'),
('Nền sữa','Đạm sữa cô đặc (MPC) / đạm sữa','Milk protein concentrate',r'đạm sữa|milk protein'),
('Nền sữa','Sữa non (colostrum)','Bovine colostrum',r'sữa non|colostrum|\bIgG'),
('Nền sữa','MFGM (màng cầu mỡ sữa)','MFGM',r'MFGM|màng cầu mỡ|milk fat globule'),
('Nền sữa','Lactoferrin','Lactoferrin',r'lactoferrin'),
('Nền sữa','Phô mai','Cheese',r'phô mai|cheese'),
('Đường & tạo ngọt','Đường (sucrose)','Sugar / sucrose',r'đường(?! ?&)(?! (?:fructo|palatinose|glucose|lactose|isomalt|mạch nha|ăn kiêng|tổng|huyết))|sucrose|saccharose'),
('Đường & tạo ngọt','Maltodextrin','Maltodextrin',r'maltodextrin'),
('Đường & tạo ngọt','Siro glucose / đường glucose','Glucose syrup',r'gluco(?:se|za)|xirô gluc|siro gluc'),
('Đường & tạo ngọt','Fructose / siro fructose','Fructose',r'fructo(?:se|za)(?!-?oligo)|(?:siro|xirô) fructo'),
('Đường & tạo ngọt','Isomaltulose (Palatinose)','Isomaltulose',r'isomaltulose|palatinose'),
('Đường & tạo ngọt','Isomalt / Maltitol / Erythritol (polyol)','Polyols',r'isomalt(?!ulose)|maltitol|erythritol|sorbitol|xylitol'),
('Đường & tạo ngọt','Sucralose (955)','Sucralose',r'sucralose|'+ins('955')),
('Đường & tạo ngọt','Steviol glycosid / stevia (960)','Stevia',r'stevi|steviol|'+ins('960')),
('Đường & tạo ngọt','Acesulfame K (950)','Acesulfame K',r'acesulfam|'+ins('950')),
('Đường & tạo ngọt','Chất tạo ngọt KHÔNG ghi rõ loại','Unspecified sweetener',r'chất tạo ngọt(?!\s*(?:tự nhiên|tổng hợp)?\s*(?:dùng (?:cho|trong) thực phẩm)?\s*:?\s*[(\dEs])'),
('Đường & tạo ngọt','Tinh bột / tinh bột bắp thủy phân','Starch / corn syrup solids',r'tinh bột(?! biến tính)|corn syrup'),
('Chất xơ & prebiotic','FOS / oligofructose','FOS',r'\bFOS\b|oligofructo|fructo-?oligo'),
('Chất xơ & prebiotic','Inulin','Inulin',r'inulin'),
('Chất xơ & prebiotic','GOS','GOS',r'\bGOS\b|galacto-?oligo'),
('Chất xơ & prebiotic',"HMO 2'-FL","2'-Fucosyllactose",r"2\s?['’`]?\s?-?\s?FL\b|2\s?['’]\s?-?\s?fucosyl|HMO"),
('Chất xơ & prebiotic','HMO khác (LNT, 3-FL, 3’-SL, 6’-SL, DFL)','Other HMOs',r"\bLNT\b|lacto-?N-?tetraose|3-?FL\b|[36]\s?['’]-?SL\b|sialyllactose|\bDFL\b"),
('Chất xơ & prebiotic','Polydextrose / dextrin kháng tiêu','Polydextrose / resistant dextrin',r'polydextrose|dextrin kháng|fibersol|resistant dextrin'),
('Chất xơ & prebiotic','Beta-glucan','Beta-glucan',r'beta-?glucan|β-?glucan'),
('Chất béo','Dầu thực vật (không ghi rõ)','Vegetable oil (unspecified)',r'dầu thực vật|vegetable oil'),
('Chất béo','Dầu cọ / palm olein','Palm oil / olein',r'dầu cọ|palm'),
('Chất béo','Dầu hướng dương (high oleic)','Sunflower oil',r'hướng dương|sunflower'),
('Chất béo','Dầu đậu nành','Soybean oil',r'dầu đậu nành|soybean oil'),
('Chất béo','Dầu hạt cải','Rapeseed / canola oil',r'hạt cải|canola|rapeseed'),
('Chất béo','Dầu dừa','Coconut oil',r'dầu dừa|coconut oil'),
('Chất béo','Dầu bắp','Corn oil',r'dầu bắp|corn oil'),
('Chất béo','Bột béo thực vật / creamer','Fat powder / non-dairy creamer',r'bột béo|béo thực vật|creamer'),
('Chất béo','MCT','MCT oil / powder',r'\bMCT\b|chuỗi trung bình'),
('Chất béo','DHA (dầu cá / dầu tảo)','DHA',r'\bDHA\b|dầu cá|dầu tảo|fish oil'),
('Chất béo','ARA','ARA',r'\bARA\b|arachidonic'),
('Chất béo','OPO / sn-2 palmitate','OPO / sn-2 palmitate',r'\bOPO\b|sn-?2|beta-?palmit'),
('Chất béo','Omega 3 / 6 / 9, ALA','Omega 3/6/9',r'omega|\bALA\b|linolenic'),
('Chất béo','Phospholipid / sphingomyelin / gangliosid','Phospholipids',r'phospholipid|sphingomyelin|gangliosid'),
('Đạm & axit amin','Đạm đậu nành (soy protein)','Soy protein isolate',r'đạm đậu nành|soy protein|protein đậu nành'),
('Đạm & axit amin','Collagen','Collagen peptides',r'collagen'),
('Đạm & axit amin','Lysine','L-Lysine',r'lysin'),
('Đạm & axit amin','Taurine','Taurine',r'taurin'),
('Đạm & axit amin','L-Carnitine','L-Carnitine',r'carnitin'),
('Đạm & axit amin','Arginine','L-Arginine',r'arginin'),
('Đạm & axit amin','HMB','HMB',r'\bHMB\b'),
('Đạm & axit amin','Leucine / BCAA','Leucine / BCAA',r'leucin|BCAA'),
('Đạm & axit amin','Glutamine','Glutamine',r'glutamin'),
('Vi chất','Premix vitamin','Vitamin premix',r'vitamin'),
('Vi chất','Vitamin K2 (MK-7)','Vitamin K2 MK-7',r'K2|MK-?7'),
('Vi chất','Vitamin D3','Vitamin D3',r'D3'),
('Vi chất','Premix khoáng','Mineral premix',r'khoáng'),
('Vi chất','Canxi (tricalci phosphat / carbonat / lactat…)','Calcium salts',r'tricalci|calci carbonat|canxi carbonat|canxi lact|calci lact|canxi|calci|calcium'),
('Vi chất','Sắt (pyrophosphat / sulfat)','Iron salts',r'sắt|ferric|ferrous'),
('Vi chất','Kẽm','Zinc salts',r'kẽm|zinc'),
('Vi chất','Selen (natri selenit)','Selenium',r'selen'),
('Vi chất','Choline','Choline',r'cholin'),
('Vi chất','Inositol','Inositol',r'inositol'),
('Vi chất','Nucleotide','Nucleotides',r'nucleotid'),
('Vi chất','Lutein','Lutein',r'lutein'),
('Vi chất','Beta-carotene','Beta-carotene',r'carotene|caroten'),
('Men & vi sinh','Men cái sữa chua (S. thermophilus, L. bulgaricus)','Yogurt cultures',r'thermophilus|bulgaricus|men lactic|men sữa chua|lên men'),
('Men & vi sinh','Probiotic Bifidobacterium (BB-12…)','Bifidobacterium',r'bifido|BB-?12'),
('Men & vi sinh','Probiotic Lactobacillus (LGG, casei, paracasei, acidophilus…)','Lactobacillus probiotics',r'rhamnosus|\bLGG\b|casei|paracasei|acidophilus|reuteri|lactobacillus(?! bulgaricus)'),
('Men & vi sinh','Lactococcus / Leuconostoc','Lactococcus',r'lactococcus|leuconostoc'),
('Men & vi sinh','Postbiotic','Postbiotics',r'postbiotic'),
('Chất ổn định & nhũ hóa','Chất ổn định / nhũ hóa KHÔNG ghi mã','Unspecified stabiliser / emulsifier',r'chất (?:ổn định|nhũ hóa|làm dày|làm dầy)(?!\s*(?:dùng (?:cho|trong) thực phẩm)?\s*:?\s*[(\dE])'),
('Chất ổn định & nhũ hóa','Mono- & diglycerid (471)','Mono- & diglycerides',r'mono-? ?(?:và|&)? ?diglycerid|'+ins('471')),
('Chất ổn định & nhũ hóa','Carrageenan (407)','Carrageenan',r'carrageenan|'+ins('407a?')),
('Chất ổn định & nhũ hóa','Gôm guar (412)','Guar gum',r'guar|'+ins('412')),
('Chất ổn định & nhũ hóa','Gôm đậu carob (410)','Locust bean gum',r'carob|locust|'+ins('410')),
('Chất ổn định & nhũ hóa','Gellan (418)','Gellan gum',r'gellan|'+ins('418')),
('Chất ổn định & nhũ hóa','Cellulose vi tinh thể (460)','Microcrystalline cellulose',r'cellulose vi tinh thể|microcrystalline|'+ins('460')),
('Chất ổn định & nhũ hóa','CMC (466)','Carboxymethyl cellulose',r'carboxymethyl|\bCMC\b|'+ins('466')),
('Chất ổn định & nhũ hóa','Pectin (440)','Pectin',r'pectin|'+ins('440')),
('Chất ổn định & nhũ hóa','Tinh bột biến tính (1422, 1442, 1450, 1412…)','Modified starch',r'tinh bột biến tính|modified starch|'+ins(r'14\d\d')),
('Chất ổn định & nhũ hóa','Gelatin','Gelatin',r'gelatin'),
('Chất ổn định & nhũ hóa','Alginat (401) / PGA (405)','Alginate / PGA',r'alginat|'+ins('401')+'|'+ins('405')),
('Chất ổn định & nhũ hóa','Phosphat / polyphosphat (339, 340, 452…)','Phosphates',r'polyphosphat|'+ins('452')+'|'+ins('339')+'|'+ins('340')+'|'+ins('341')+'|'+ins('450')),
('Chất ổn định & nhũ hóa','Citrat (331, 332)','Citrates',r'natri citrat|kali citrat|'+ins('331')+'|'+ins('332')),
('Chất ổn định & nhũ hóa','Lecithin (322)','Lecithin',r'lecithin|lecitin|'+ins('322')),
('Chất ổn định & nhũ hóa','Este khác (472e, 473, 475…)','Other emulsifiers (DATEM, sucrose esters)',ins('472e?')+'|'+ins('473')+'|'+ins('475')+'|'+ins('477')),
('Chất ổn định & nhũ hóa','Agar / thạch','Agar / jelly agents',r'agar|bột làm thạch|konjac'),
('Điều chỉnh độ axit & bảo quản','Axit citric (330)','Citric acid',r'axit citric|acid citric|citric acid|'+ins('330')),
('Điều chỉnh độ axit & bảo quản','Axit lactic (270)','Lactic acid',r'axit lactic|acid lactic|'+ins('270')),
('Điều chỉnh độ axit & bảo quản','Axit malic (296) / khác','Malic acid',r'malic|'+ins('296')),
('Điều chỉnh độ axit & bảo quản','Kali sorbat (202) / bảo quản','Potassium sorbate',r'sorbat|chất bảo quản|'+ins('202')+'|'+ins('211')),
('Điều chỉnh độ axit & bảo quản','Chất chống oxy hóa (304, 306, 307…)','Antioxidants (ascorbyl palmitate, tocopherols)',r'chống oxy hóa|ascorbyl|tocopherol|'+ins('304')+'|'+ins('306')+'|'+ins('307')),
('Màu & hương','Hương liệu','Flavours',r'hương(?! vị)|flavou?r'),
('Màu & hương','Màu tổng hợp (102, 110, 124, 129, 133…)','Synthetic colours',r'màu tổng hợp|tạo màu tổng hợp|'+ins('102')+'|'+ins('110')+'|'+ins('124')+'|'+ins('129')+'|'+ins('133')),
('Màu & hương','Màu tự nhiên (120 carmin, 150 caramel, 160…)','Natural colours',r'màu tự nhiên|carmin|caramel|'+ins('120')+'|'+ins('150[a-d]?')+'|'+ins('160[a-e]?')+'|'+ins('100')),
('Nguyên liệu tạo vị','Bột cacao','Cocoa powder',r'cacao|ca cao|cocoa|socola'),
('Nguyên liệu tạo vị','Chiết xuất malt / lúa mạch','Malt extract',r'\bmalt\b|protomalt|lúa mạch|mạch nha'),
('Nguyên liệu tạo vị','Ngũ cốc / yến mạch','Cereals / oats',r'yến mạch|ngũ cốc|\boat|gạo|bắp non'),
('Nguyên liệu tạo vị','Nước ép / mứt trái cây','Fruit juice / preparation',r'nước ép|nước trái cây|mứt|trái cây|fruit'),
('Nguyên liệu tạo vị','Thạch dừa / nata de coco','Nata de coco',r'thạch dừa|nata de coco'),
('Nguyên liệu tạo vị','Đậu nành (hạt / dịch trích)','Soybean base',r'(?:dịch|hạt|bột|sữa)[^,]{0,15}đậu nành|soybean(?! oil)'),
('Nguyên liệu tạo vị','Trà / matcha','Tea / matcha',r'trà|matcha'),
('Nguyên liệu tạo vị','Hạt (hạnh nhân, óc chó, macca, đậu…)','Nuts / seeds',r'hạnh nhân|óc chó|macca|mắc ca|hạt điều|đậu phộng|hạt sen|hạt chia|almond|walnut'),
('Nguyên liệu tạo vị','Mật ong / tổ yến / nha đam / khác','Honey / bird nest / aloe',r'mật ong|yến sào|tổ yến|nha đam|aloe'),
]
CRX=[(g,n,e,re.compile(r,re.I)) for g,n,e,r in ING]
SPECIFIC_DAIRY={'Sữa bột gầy (SMP)','Sữa bột nguyên kem (WMP)'}
def ingredients(text):
    """Return list of canonical ingredient names found in an ingredient text."""
    t=' '+text+' '
    t=re.sub(r'(Khoáng chất|Vitamin|Chất béo|Đường & Chất xơ|Thành phần khác)\s+Không có',' ',t)   # empty groups on grouped retailer pages
    t=re.sub(r'Đường & Chất xơ|Thành phần khác',' , ',t)
    found=[n for g,n,e,rx in CRX if rx.search(t)]
    # generic milk powder only if no specific powder matched
    if 'Sữa bột (không ghi rõ loại)' in found and SPECIFIC_DAIRY & set(found) and not re.search(r'sữa bột(?! gầy| nguyên kem| tách)',t,re.I): found.remove('Sữa bột (không ghi rõ loại)')
    if 'Bột whey / whey (khác)' in found and re.search(r'whey',t,re.I) and not re.search(r'bột whey|whey powder|whey(?! protein| cô đặc| giàu| thủy| phân)',t,re.I): found.remove('Bột whey / whey (khác)')
    if 'Dầu thực vật (không ghi rõ)' in found and any(x in found for x in ['Dầu cọ / palm olein','Dầu hướng dương (high oleic)','Dầu đậu nành','Dầu hạt cải','Dầu dừa','Dầu bắp']) and re.search(r'dầu thực vật\s*\(',t,re.I): found.remove('Dầu thực vật (không ghi rõ)')
    return found
GROUP={n:g for g,n,e,r in ING}; EN={n:e for g,n,e,r in ING}; ORDER=[n for g,n,e,r in ING]
# customer mapping: manufacturer text or product title -> canonical customer
CUST=[
('Vinamilk',r'sữa việt nam|vinamilk|\bVNM\b|ông thọ|ngôi sao phương nam|\bsusu\b|\bprobi\b|dielac|optimum gold|\byoko\b|green farm|vinamilk sure|vnm sure|ridielac'),
('Mộc Châu Milk',r'mộc châu|moc chau|yo-?pro'),
('FrieslandCampina VN',r'friesland|dutch lady|cô gái hà lan|fristi|yomost|hoàn hảo|trường sinh'),
('TH Group',r'\bTH\b|th true|topkid|tập đoàn th'),
('Dalatmilk',r'dalat ?milk|đà lạt milk'),
('Nutifood',r'nutifood|growplus|grow plus|nuvi|v[aä]rna|nutimilk|famna'),
('VitaDairy',r'vitadairy|colosbaby|oggi|calosure|calokid|colos gain|colos dha|vitagrow|fohepta|gluvita|nepro'),
('Nutricare',r'nutricare|metacare|glucare|smarta|care 100|coloscare|glugold|nutricare'),
('LOF (IDP)',r'\bLOF\b|\bIDP\b|sữa quốc tế|\bkun\b|ba vì|malto'),
('Hanoimilk',r'hanoimilk|izzi|yotuti|sữa hà nội'),
('Nestlé VN',r'nestl|milo|nan grow'),
('Abbott VN',r'abbott'),
('Morinaga VN',r'morinaga'),
]
CRX_C=[(c,re.compile(r,re.I)) for c,r in CUST]
def customer(*texts):
    for x in texts:
        for c,rx in CRX_C:
            if x and rx.search(x): return c
    return ''

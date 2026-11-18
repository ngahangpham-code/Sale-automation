# Dairy VN ingredient report – collection scripts

Scripts used to build `reports/Bao_cao_nha_san_xuat_sua_VN.xlsx`. Run them from a scratch directory.

- `links.py` – list links on a downloaded page that match a pattern
- `dl_profiles.py` – read the declaration PDF links (hồ sơ công bố) from Dutch Lady product pages
- `ocr.sh` + `extract.py` – OCR a scanned declaration PDF (needs `tesseract-ocr tesseract-ocr-vie`) and pull out the "Thành phần" paragraph
- `page_ing.py` – read the ingredient text from product pages (Hanoimilk)
- `nut.py` – find key actives in the nutrition table (Nutifood, VitaDairy)
- `ph.py` – read ingredients, place of manufacture and manufacturer from Pharmacity product pages
- `data/extra.json` – SKUs whose ingredients came from retailer pages via web search (with source URL)
- `data/hn_manual.json` – manual fixes for Hanoimilk declarations the OCR could not read cleanly
- `collect.py` – merge everything into `products.json`
- `build_xlsx.py products.json out.xlsx` – write the Excel report

## Ingredient opportunity workbook (`reports/Co_hoi_nguyen_lieu_khach_hang_sua_VN.xlsx`)
- `sm.py` – list URLs from a sitemap (follows sitemap indexes)
- `fetch.sh` – cache a page by URL hash
- `rt.py` – parse retailer product pages (Thế Giới Sữa, Kingfoodmart, Sữa Cho Bé Yêu, Medigo): ingredients, place of manufacture, manufacturer
- `norm.py` – ingredient dictionary (~110 canonical ingredients, INS codes) and customer mapping
- `consolidate.py` – merge official + retailer records, grade reliability A–D, flag truncated/grouped/conflicting sources -> `records.json`
- `build_v2.py records.json out.xlsx` – write the opportunity workbook

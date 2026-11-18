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

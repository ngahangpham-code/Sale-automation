import sys,re
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
m=re.search(r'(Thành phần cấu tạo|Thành phần nguyên liệu|Thanh phần|Thành phần|Nguyên liệu)\s*[^:\n]{0,40}:\s*(.*?)(?=\n\s*\d\s*[\.,]\s|Thời hạn|Hạn sử dụng|Hướng dẫn|Chỉ tiêu|\n\s*\n)',t,re.S|re.I)
print(re.sub(r'\s+',' ',m.group(2)).strip() if m else '')

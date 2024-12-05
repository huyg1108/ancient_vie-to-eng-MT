import pandas as pd
import re

# Đọc file CSV
file_path = 'translate.csv'  # Thay bằng đường dẫn tới file của bạn
df = pd.read_csv(file_path)

# Kiểm tra cột 'eng'
non_latin_rows = []
pattern = re.compile(r'^[\x00-\x7F“”‘’\'"–-]*$')  # Bao gồm cả “ ” ‘ ’ ' " – -

for index, value in df['eng'].dropna().items():  # Thay iteritems() bằng items()
    if not pattern.match(value):  # Nếu không khớp với ký tự ASCII
        non_latin_rows.append((index, value))

# In kết quả
if non_latin_rows:
    print("Các dòng có ký tự không phải Latinh hoặc dấu câu:")
    for index, value in non_latin_rows:
        print(f"Dòng {index}: {value}")
else:
    print("Không tìm thấy ký tự nào không thuộc bảng Latinh hoặc dấu câu.")

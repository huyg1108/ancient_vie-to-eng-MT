import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def preprocess_data(raw_data):
    clean_data = []
    for line in raw_data:
        # Loại bỏ ký tự *
        line = re.sub(r'\*', ' ', line)
        
        # Loại bỏ cụm [x]
        line = re.sub(r'\[\d+\]', ' ', line)
        
        # Loại bỏ ký tự xuống dòng, khoảng trắng thừa
        line = re.sub(r'\s+', ' ', line).strip()
        
        # Loại bỏ phần đánh số đầu dòng (ví dụ: "1. ", "2. ", ...)
        line = re.sub(r'^\d+\.\s*', '', line)
        
        # Loại bỏ phần đánh số
        line = re.sub(r'^\d\s*', '', line)
        # Dùng regex để tìm các câu kết thúc bằng dấu . ! ? : ;
        sentences = re.split(r'(?<=[.!?:;])\s*', line.strip())
        # print(f"Sentences: {sentences}")
        clean_data.extend(sentence.strip() for sentence in sentences if sentence.strip())
    
    return clean_data


def extract_phien_am(url):
    """
    Trích xuất dữ liệu phần 'Phiên âm' từ URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"  
    soup = BeautifulSoup(response.text, 'html.parser')
    
    phien_am_section = soup.find_all("p", class_="MsoNormal")
    phien_am_data = []
    is_phien_am = False
    
    for p in phien_am_section:
        text = p.get_text(strip=False)

        if "Phiên âm:" in text:
            is_phien_am = True
            continue  
        
        if is_phien_am and ("Dịch xuôi:" in text or "Dịch thơ:" in text or "BÌNH GIẢNG" in text):
            break 
        
        if is_phien_am:
            phien_am_data.append(f" {text} ")
    
    # Tiền xử lý dữ liệu: loại bỏ ký tự thừa và tách câu
    phien_am_data = preprocess_data(phien_am_data)
    return [sentence.strip() for sentence in phien_am_data if sentence.strip()]

# Tạo danh sách URL
base_url = "https://nhantu.net/TonGiao/DaoDucKinh/DDK{xx}.htm"
urls = [base_url.format(xx=str(i).zfill(2)) for i in range(1, 82)]  # Lấy 1 chương để thử nghiệm

# Thu thập dữ liệu
for i, url in enumerate(urls, start=1):
    all_data = []
    try:
        print(f"Đang xử lý chương {i}: {url}")
        sentences = extract_phien_am(url)
        for sentence in sentences:
            if "Dịch xuôi:" in sentence:
                break
            all_data.append({"vie": sentence})
    except Exception as e:
        print(f"Lỗi khi xử lý chương {i}: {e}")

    # Lưu vào CSV
    df = pd.DataFrame(all_data)
    output_file = f"dao_duc_kinh_phien_am_chuong_{i}.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"Dữ liệu đã được lưu vào tệp: {output_file}")

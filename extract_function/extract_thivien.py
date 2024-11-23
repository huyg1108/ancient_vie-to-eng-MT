import csv
import requests
from bs4 import BeautifulSoup
import time
import random
import os

# List of user-agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Safari/601.6.17",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18363",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5X Build/N2G47F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
]

# Create the 'extracted' folder if it doesn't exist
output_folder = "extracted"
os.makedirs(output_folder, exist_ok=True)
link_web = input("Enter the link of the website you want to extract poems from: ")
headers = {'User-Agent': random.choice(user_agents)}
response = requests.get(link_web, headers=headers)
html_content = response.content.decode()
soup = BeautifulSoup(html_content, 'html.parser')

poem_group_lists = soup.find_all('div', class_='poem-group-list')
sub_links = [a['href'] for div in poem_group_lists for a in div.find_all('a', href=True)]
total_poem_sentences = 0
title_number = 0
for sub_link in sub_links:
    time.sleep(random.uniform(3, 10))
    headers = {'User-Agent': random.choice(user_agents)}
    sub_response = requests.get('https://www.thivien.net/' + sub_link, headers=headers)
    sub_html_content = sub_response.content.decode()
    sub_soup = BeautifulSoup(sub_html_content, 'html.parser')

    header = sub_soup.find('header', class_='page-header')
    header_name = header.find('h1').get_text(strip=True) if header else 'Unknown'
    print(f"Extracting poems from '{header_name}'...")
    poem_contents = sub_soup.find_all('div', class_='poem-view-alternative')
    data = []

    for poem_content in poem_contents:
        h4_elements = poem_content.find_all('h4')
        for h4 in h4_elements:
            strong_element = h4.find('strong')
            if strong_element:
                p_elements = h4.find_next_siblings('p')
                total_poem_sentences += len(p_elements)
                for p in p_elements:
                    poem_text = p.get_text(separator='\n').strip()
                    lines = poem_text.split('\n')
                    data.append(lines)

    # Save the file in the 'extracted' folder
    title_number += 1
    file_path = os.path.join(output_folder, str(title_number) + ".csv")
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Chinese', 'Ancient Vietnamese', 'Current Vietnamese'])
        csvwriter.writerows(data)
print(f"Total poems sentence extracted: {total_poem_sentences}")
print("Poems have been extracted and saved in the 'extracted' folder.")
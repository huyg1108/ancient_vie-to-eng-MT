import os
import pandas as pd
import csv
import time
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

# parent folder of the csv files
key = ''
folder = input('Enter the folder name: ')
csv_files = [f for f in os.listdir(f'{folder}/') if f.endswith('.csv')]
input_start = int(input('Enter the starting index: '))
# merge all csv files into one

merged_data = []
for file in csv_files:
    df = pd.read_csv(f'{folder}/{file}', header=None)
    # remove first row
    df = df[1:]
    merged_data.append(df)
merged_data = pd.concat(merged_data)
merged_data.dropna(inplace=True)
modern_vietnamese_poems = merged_data[2].tolist()
ancient_vietnamese_poems = merged_data[1].tolist()
print('Number of poems:', len(modern_vietnamese_poems))
def create_prompt(content):
    return (
        "Translate the following sentences from Vietnamese to English according to the requirements below:\n"
        "- **The output must have exactly the same number of lines as the input**\n"
        "- Only print those lines, do not include any other output or explanation\n"
        "- English text has no diacritics, e.g. \"Lũng\" -> Lung\n"
        "- Proper names should be written without diacritics or translated to their English equivalent, e.g. "
        "\"Thượng Hải\" -> Shanghai, \"Anh Vũ\" -> Anh Vu, or \"Trương Hàn\" -> Truong Han\n"
        "Translate those lines to English following my instruction:\n\n"
        f"{content}"
    )

def not_match_line_prompt(content):
    return (
        "The previous output did not match the number of lines in the input.\n"
        "Please translate those content again and make sure **the output must have exactly the same number of lines as the input**\n\n"
        f"{content}"
    )
    
genai.configure(api_key=key)

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('models/gemini-1.5-pro')

def remove_empty_or_whitespace(lst):
    return [item for item in lst if item.strip()]


# loop through each 50 lines each time
batch_size = 50
total_poem_sentences = 0


with open(f'translate.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['vie', 'eng'])

print('Extract...')
for i in range(input_start, len(modern_vietnamese_poems), batch_size):
    print(i)
    data = []
    modern_vietnamese_poems_batch = modern_vietnamese_poems[i:i+batch_size]
    ancient_vietnamese_poems_batch = ancient_vietnamese_poems[i:i+batch_size]
    english = []
    text = ""
    for i in range(len(modern_vietnamese_poems_batch)):
        text += modern_vietnamese_poems_batch[i] + '\n'

    response = model.generate_content(create_prompt(text))
    english_poem = remove_empty_or_whitespace(response.text.split('\n'))

    while (len(ancient_vietnamese_poems_batch) != len(english_poem)):
        print('English translation does not match with Vietnamese texts')
        time.sleep(20)
        response = model.generate_content(not_match_line_prompt(text))
        english_poem = response.text.split('\n')

    for i in range(len(modern_vietnamese_poems_batch)):
        data.append([ancient_vietnamese_poems_batch[i], english_poem[i]])

    with open(f'translate.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # append the data to the csv file
        csvwriter.writerows(data)

    time.sleep(20)
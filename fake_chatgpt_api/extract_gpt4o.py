from fake_chatgpt_api import FakeChatGPTAPI
import os
import pandas as pd
import csv
import time

# parent folder of the csv files
csv_files = [f for f in os.listdir('./extracted') if f.endswith('.csv')]
# merge all csv files into one
merged_data = []
for file in csv_files:
    df = pd.read_csv(f'./extracted/{file}', header=None)
    # remove first row
    df = df[1:]
    merged_data.append(df)
merged_data = pd.concat(merged_data)
merged_data.dropna(inplace=True)
modern_vietnamese_poems = merged_data[2].tolist()
ancient_vietnamese_poems = merged_data[1].tolist()
# drop the first row
modern_vietnamese_poems = modern_vietnamese_poems[1:]
ancient_vietnamese_poems = ancient_vietnamese_poems[1:]

def create_prompt(content):
    return (
        "Translate the following sentences from Vietnamese to English according to the requirements below\n"
        "- Keep exactly the same number of lines in total (if input has 50 lines, output must have 50 lines too)\n"
        "- Only print those lines, do not include any other output or explanation\n"
        "- No diacritics, e.g. \"Lũng\" -> Lung\n"
        "- Proper names should be written without diacritics or translated to their English equivalent, e.g. "
        "\"Thượng Hải\" -> Shanghai, \"Anh Vũ\" -> Anh Vu, or \"Trương Hàn\" -> Truong Han\n"
        f"{content}"
    )

# loop through each 50 lines each time
batch_size = 50
total_poem_sentences = 0

fake = FakeChatGPTAPI()

with open(f'translate.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
for i in range(0, len(modern_vietnamese_poems), batch_size):
    modern_vietnamese_poems_batch = modern_vietnamese_poems[i:i+batch_size]
    ancient_vietnamese_poems_batch = ancient_vietnamese_poems[i:i+batch_size]
    text = ""
    for i in range(len(modern_vietnamese_poems_batch)):
        text += str(i) + ') ' + modern_vietnamese_poems_batch[i] + '\n'
    # print(text)
    data = []
    respond_text = fake.send_request(text)
    english_poem = respond_text.split('\n')
    for i in range(len(english_poem)):
        data.append([ancient_vietnamese_poems_batch[i], english_poem[i]])
    # total_poem_sentences += 1
    # write csv file with 2 columns vie,eng
    with open(f'translate.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # append the data to the csv file
        csvwriter.writerows(data)

    time.sleep(10)

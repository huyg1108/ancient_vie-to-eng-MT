from fake_chatgpt_api import FakeChatGPTAPI
import os
import pandas as pd
import csv


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


    
# loop through each 50 lines each time
batch_size = 50
total_poem_sentences = 0

fake = FakeChatGPTAPI()
data = []
for i in range(0, len(modern_vietnamese_poems), batch_size):
    modern_vietnamese_poems_batch = modern_vietnamese_poems[i:i+batch_size]
    ancient_vietnamese_poems_batch = ancient_vietnamese_poems[i:i+batch_size]
    english = []
    text = ""
    for i in range(len(modern_vietnamese_poems_batch)):
        text += modern_vietnamese_poems_batch[i] + '\n'
    # print(text)
    respond_text = fake.send_request(text)
    english_poem = respond_text.split('\n')
    for i in range(len(english_poem)):
        data.append([ancient_vietnamese_poems_batch[i], english_poem[i]])
    # total_poem_sentences += 1
    # write csv file with 2 columns vie,eng
with open(f'translate.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['vie','eng'])
    csvwriter.writerows(data)

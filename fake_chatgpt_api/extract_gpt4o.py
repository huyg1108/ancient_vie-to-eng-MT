from fake_chatgpt_api import FakeChatGPTAPI
import os
import pandas as pd
import csv
import time

# parent folder of the csv files
csv_files = [f for f in os.listdir('./for_trans') if f.endswith('.csv')]
# merge all csv files into one
merged_data = []
for file in csv_files:
    df = pd.read_csv(f'./for_trans/{file}', header=None)
    # remove first row
    df = df[1:]
    merged_data.append(df)
merged_data = pd.concat(merged_data)
merged_data.dropna(inplace=True)
modern_vietnamese_poems = merged_data[2].tolist()
ancient_vietnamese_poems = merged_data[1].tolist()
# # drop the first row
# modern_vietnamese_poems = modern_vietnamese_poems[1:]
# ancient_vietnamese_poems = ancient_vietnamese_poems[1:]

def create_prompt(content):
    return (
        "Translate the following sentences from Vietnamese to English according to the requirements below\n"
        "    - Print each corresponding line (all without punctuation at the end)\n"
        "    - Keep exactly number of lines in total (if input has 10 lines, output must have 10 lines too)\n"
        "        - Example:\n"
        "            + Input:\n"
        "            1. Bãi thơm cây xanh biếc làm sao!\n"
        "            2. Khói toả ra từ lá cây lan làm gió thơm nổi dậy\n"
        "            3. Bờ liền với hoa đào, sóng gấm sinh\n"
        "            + Output:\n"
        "            1. The fragrant field the lush green trees how beautiful\n"
        "            2. The smoke rising from the leaves of the trees carries the scent of the wind\n"
        "            3. The shore merges with the peach blossoms and the brocade waves are born\n"
        "    - Only print those lines, do not include any other output or explanation\n"
        f"\n{content}"
    )


def not_match_line_prompt(content):
    return (
        "The previous output did not match the number of lines in the input.\n"
        "Please translate those content again and make sure **the output must have exactly the same number of lines as the input**\n\n"
        f"{content}"
    )
    
# loop through each 50 lines each time
batch_size = 50
total_poem_sentences = 0

fake = FakeChatGPTAPI()
# clean csv file
with open(f'translate.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['vie', 'eng'])

for i in range(0, len(modern_vietnamese_poems), batch_size):
    print(i)
    data = []
    modern_vietnamese_poems_batch = modern_vietnamese_poems[i:i+batch_size]
    ancient_vietnamese_poems_batch = ancient_vietnamese_poems[i:i+batch_size]
    english = []
    text = ""
    for i in range(len(modern_vietnamese_poems_batch)):
        text += str(i) + ') ' + modern_vietnamese_poems_batch[i] + '\n'

    respond_text = fake.send_request(create_prompt(text))
    english_poem = respond_text.split('\n')

    while (len(ancient_vietnamese_poems_batch) != len(english_poem)):
        print('English translation does not match with Vietnamese texts')
        time.sleep(10)
        respond_text = fake.send_request(not_match_line_prompt(text))
        english_poem = respond_text.split('\n')

    for i in range(len(modern_vietnamese_poems_batch)):
        data.append([ancient_vietnamese_poems_batch[i], english_poem[i]])

    with open(f'translate.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # append the data to the csv file
        csvwriter.writerows(data)

    time.sleep(10)

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer_vi2en = AutoTokenizer.from_pretrained("vinai/vinai-translate-vi2en-v2", src_lang="vi_VN")
model_vi2en = AutoModelForSeq2SeqLM.from_pretrained("vinai/vinai-translate-vi2en-v2")

def translate_vi2en(vi_text: str) -> str:
    input_ids = tokenizer_vi2en(vi_text, return_tensors="pt").input_ids
    output_ids = model_vi2en.generate(
        input_ids,
        decoder_start_token_id=tokenizer_vi2en.lang_code_to_id["en_XX"],
        num_return_sequences=1,
        num_beams=5,
        early_stopping=True
    )   
    en_text = tokenizer_vi2en.batch_decode(output_ids, skip_special_tokens=True)
    en_text = " ".join(en_text)
    return en_text

# read multiple csv files in folder ./extracted
import os
import pandas as pd
import csv
output_folder = "translate"
os.makedirs(output_folder, exist_ok=True)
csv_files = [f for f in os.listdir('./extracted') if f.endswith('.csv')]
for file in csv_files:
    df = pd.read_csv(f'./extracted/{file}', header=None)
    df.dropna(inplace=True)
    modern_vietnamese_poems = df[2].tolist()
    ancient_vietnamese_poems = df[1].tolist()
    modern_vietnamese_poems = modern_vietnamese_poems[1:]
    ancient_vietnamese_poems = ancient_vietnamese_poems[1:]
    english = []
    data = []
    file_path = f'./translate/{file}'
    print(file_path)
    for i in range(len(modern_vietnamese_poems)):
        modern_vietnamese_poem = modern_vietnamese_poems[i]
        ancient_vietnamese_poem = ancient_vietnamese_poems[i]
        english_poem = translate_vi2en(modern_vietnamese_poem)
        data.append([ancient_vietnamese_poem, english_poem])
    # write csv file with 2 columns vie,eng
    
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['vie','eng'])
        csvwriter.writerows(data)


    
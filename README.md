# Ancient Vietnamese to English Machine Translation

##  Overview

This project aims to develop a machine translation system that converts Ancient Vietnamese texts into English. The workflow includes data crawling, preprocessing, augmentation, and fine-tuning a T5 (Text-to-Text Transfer Transformer) model to enhance translation accuracy.

## Project Pipeline

### Data Crawling 

We collected data from multiple sources, primarily from Thi Viện, a repository of Vietnamese poetry .

To crawl data from specific collections, run:
```
cd ancient_ViET-to-eng-mt
python extract_function/extract_thivien.py
```
### Data Augmentation 

To expand the dataset from minhtoan/t5-
translate-vietnamese-nom model, we applied back-translation, using two-way translation models from Hugging Face to generate more diverse training data.

### Fine-tuning T5 Model 

We fine-tuned a T5 model on our dataset for sequence-to-sequence translation, optimizing it for Ancient Vietnamese to English translation.

4️⃣ Evaluation & Inference 📊

We evaluated the model using BLEU-4 scores to measure translation quality.

Let me know if you need further refinements! 🚀

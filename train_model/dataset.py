import torch
import numpy as np
from torch.utils.data import DataLoader, Dataset

class VieEngPairDataset(Dataset):
    def __init__(self, df, prefix="translate ancient Vietnamese to English: "):
        self.df = df
        self.prefix = prefix

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        vie_sentence = self.prefix + self.df.iloc[idx]["vie"]  # Add prefix to Vietnamese sentence
        # vie_sentence = self.df.iloc[idx]["vie"]  # Add prefix to Vietnamese sentence
        eng_sentence = self.df.iloc[idx]["eng"]

        return (vie_sentence, eng_sentence)


def collate_fn(batch, tokenizer, max_length=64):
    vie_sentences, eng_sentences = zip(*batch)

    inputs = tokenizer(
        list(vie_sentences), max_length=max_length, truncation=True, padding="max_length", return_tensors="pt"
    )
    targets = tokenizer(
        list(eng_sentences), max_length=max_length, truncation=True, padding="max_length", return_tensors="pt"
    )

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]
    labels = targets["input_ids"]

    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
    }
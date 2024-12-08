import argparse
import torch
import json
import torch.nn as nn
import pandas as pd
import numpy as np
from dataset import *
from function import *
from transformers import T5ForConditionalGeneration, T5Tokenizer

import sys
sys.stdout.reconfigure(line_buffering=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Fine-tuning Old Vietnamese to English MT")
    parser.add_argument('--run_name', type=str, default='', help="Name of the run")
    parser.add_argument('--task_name', type=str, default='', help="Name of the task")
    parser.add_argument('--model_name', type=str, default='NlpHUST/t5-vi-en-small')
    parser.add_argument('--tokenizer_path', type=str, default='', help='Path to tokenizer')
    parser.add_argument('--epochs', type=int, default=5, help='Number of training epochs')
    parser.add_argument('--lr', type=float, default=5e-5, help='Learning rate')
    parser.add_argument('--train_data', type=str, default='', help='Path to the train data')
    parser.add_argument('--test_data', type=str, default='', help='Path to the test data')
    parser.add_argument('--val_data', type=str, default='', help='Path to the validation data')
    parser.add_argument('--best_fine_tuned_ckpt', type=str, default='', help='Path to best model')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size for training')
    parser.add_argument('--early_stop_patience', type=int, default=5, help="Patience for early stopping")
    parser.add_argument('--output_path', type=str, default='', help='Path to save the output model')
    parser.add_argument('--ckpt_name', type=str, default='/best_model.pth', help='Name of model checkpoint file')
    parser.add_argument('--mode', type=str, choices=['train', 'eval'], default='train', help="Mode: 'train' or 'eval'")
    return parser.parse_args()


def main():
    args = parse_arguments()
    print(f"Running {args.task_name} with run name: {args.run_name}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # load model
    model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    tokenizer = T5Tokenizer.from_pretrained(args.model_name, legacy=False)
    model = model.to(device)

    if args.mode == 'train':
        # load dataset
        train_df = pd.read_csv(args.train_data)
        val_df = pd.read_csv(args.val_data)

        train_dataset = VieEngPairDataset(train_df)
        val_dataset = VieEngPairDataset(val_df)

        train_dataloader = DataLoader(
            train_dataset,
            batch_size=args.batch_size,
            shuffle=True,
            collate_fn=lambda batch: collate_fn(batch, tokenizer, max_length=64),
        )

        val_dataloader = DataLoader(
            val_dataset,
            batch_size=args.batch_size,
            collate_fn=lambda batch: collate_fn(batch, tokenizer, max_length=64),
        )

        print('Training...')
        optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
        criterion = nn.CrossEntropyLoss()

        train_model(
            train_dataloader=train_dataloader,
            val_dataloader=val_dataloader,
            model=model,
            optimizer=optimizer,
            device=device,
            num_epochs=args.num_epochs,
            patience=args.early_stop_patience,
            save_path=args.output_path + args.ckpt_name
        )

    elif args.mode == 'eval':
        test_df = pd.read_csv(args.test_data)

        print('Loading checkpoint...')
        model.load_state_dict(torch.load(args.best_fine_tuned_ckpt, weights_only=False))
        model.to(device)

        print('Evaluating...')

        avg_bleu = calculate_bleu(
            test_df=test_df, 
            model=model, 
            tokenizer=tokenizer, 
            device=device, 
            prefix="translate ancient Vietnamese to English: "
        )

if __name__ == "__main__":
    print("Script is starting...")
    #torch.cuda.empty_cache()

    if torch.cuda.is_available():
        print(f"Number of GPUs available: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"Memory Allocated: {torch.cuda.memory_allocated(i) / 1024 ** 3:.2f} GB")
            print(f"Memory Cached: {torch.cuda.memory_reserved(i) / 1024 ** 3:.2f} GB")
            print(f"Memory Total: {torch.cuda.get_device_properties(i).total_memory / 1024 ** 3:.2f} GB")
    else:
        print("No GPU available.")

    main()


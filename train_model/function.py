import torch
import numpy as np
from dataset import *
from tqdm import tqdm

def train_model(
    train_dataloader,
    val_dataloader,
    model,
    optimizer,
    device,
    num_epochs=3,
    patience=3,
    save_path="/kaggle/working/"
):
    model.to(device)

    best_val_loss = float("inf")
    epochs_without_improvement = 0

    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")            
        # Training loop
        model.train()
        epoch_loss = 0
        for batch in tqdm(train_dataloader, desc="Training"):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            optimizer.zero_grad()

            # Forward pass
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        train_loss = epoch_loss / len(train_dataloader)

        # Validation loop
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in tqdm(val_dataloader, desc="Validating"):
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)

                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                val_loss += outputs.loss.item()

        val_loss = val_loss / len(val_dataloader)

        print(f"Epoch {epoch + 1} - Training Loss: {train_loss:.8f} - Validation Loss: {val_loss:.8f}")

        # Check for improvement
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_without_improvement = 0
            torch.save(model.state_dict(), save_path + "best_model.pth")
        else:
            epochs_without_improvement += 1
            print(f"No improvement for {epochs_without_improvement} epoch(s).")

        # Early stopping
        if epochs_without_improvement >= patience:
            print(f"Early stopping triggered. Stopping training at epoch {epoch + 1}.")
            break

        torch.cuda.empty_cache()


from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from tqdm import tqdm

def calculate_bleu(test_df, model, tokenizer, device, max_length=64, prefix=""):
    model.eval()  # Set model to evaluation mode
    total_bleu = 0
    # smooth_fn = SmoothingFunction().method4  # Use smoothing to avoid zero BLEU scores
    
    for index, row in tqdm(test_df.iterrows(), total=len(test_df), desc="Calculating BLEU"):
        src = prefix + row['vie']  # Add prefix to the input sentence
        reference = row['eng'].split()  # Reference: English translation (split into words)
        
        # Tokenize and generate translation
        tokenized_text = tokenizer.encode(src, return_tensors="pt").to(device)
        summary_ids = model.generate(
            tokenized_text,
            max_length=max_length, 
            num_beams=5,
            repetition_penalty=2.5, 
            length_penalty=1.0, 
            early_stopping=True
        )
        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        candidate = output.split()  # Candidate: Generated translation (split into words)
        
        # Compute BLEU score for this pair
        # bleu_score = sentence_bleu([reference], candidate, smoothing_function=smooth_fn)
        bleu_score = sentence_bleu([reference], candidate, smoothing_function=smooth_fn)
        total_bleu += bleu_score

    # Compute average BLEU score scaled to 0-100
    avg_bleu = (total_bleu / len(test_df)) * 100
    print(f"\nAverage BLEU score: {avg_bleu:.2f}")
    return avg_bleu
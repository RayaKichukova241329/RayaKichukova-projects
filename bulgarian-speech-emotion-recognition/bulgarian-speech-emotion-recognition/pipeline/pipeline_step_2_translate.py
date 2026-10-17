"""
pipeline_step_2_translate.py

This module handles the translation of text using a fine-tuned
Hugging Face model.

It has been modified to remove all training code and only
provide an inference function.
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List

def run_translation(sentences: List[str], model_path: str) -> List[str]:
    """
    Translates a list of sentences using a fine-tuned model.
    """
    print(f"--- Step 2: Translation ---")
    print(f"Loading translation model from: {model_path}")
    
    try:
        # Load model and tokenizer explicitly
        # We add use_fast=False to bypass potential tokenizer.json corruption
        # and force it to use the spiece.model (legacy)
        tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        
        device = 0 if torch.cuda.is_available() else -1
        # Create pipeline with loaded components
        translator = pipeline(
            "translation", 
            model=model, 
            tokenizer=tokenizer, 
            device=device
        )
        print(f"Model loaded. Using device: {'cuda:0' if device == 0 else 'cpu'}")
    except Exception as e:
        print(f"Error loading translation model from {model_path}: {e}")
        print("Please ensure the model directory is correct and contains all necessary files.")
        return None

    if not sentences:
        print("No sentences to translate.")
        return []

    print(f"Translating {len(sentences)} sentences...")
    translations = []
    batch_size = 16 
    try:
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i+batch_size]
            # Set max_length for generation
            translated_batch = translator(batch, max_length=128)
            translations.extend([t['translation_text'] for t in translated_batch])
        print("Translation complete.")
        return translations
    except Exception as e:
        print(f"Error during translation: {e}")
        return None


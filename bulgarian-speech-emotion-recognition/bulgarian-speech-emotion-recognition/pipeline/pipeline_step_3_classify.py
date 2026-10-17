"""
pipeline_step_3_classify.py

This module handles loading the pre-trained emotion classification model
and running inference on a list of sentences.

Based on: autobots_assemble.py
"""

import tensorflow as tf
import numpy as np
import os
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

# ----------------------------
# Configuration
# ----------------------------
MAX_LEN = 128
# Define emotion labels (must match the training script)
EMOTION_LABELS = ['neutral', 'sadness', 'fear', 'happiness', 'anger', 'disgust', 'surprise']
IDX_TO_LABEL = {idx: label for idx, label in enumerate(EMOTION_LABELS)}


def load_emotion_model(model_dir: str):
    """
    Loads the fine-tuned TFXLMRobertaForSequenceClassification model and tokenizer
    from a specified directory.

    Args:
        model_dir (str): The directory where the model and tokenizer are saved.

    Returns:
        tuple: (model, tokenizer) or (None, None) if loading fails.
    """
    try:
        if not os.path.exists(model_dir):
            print(f"Error: Emotion model directory not found at: {model_dir}")
            return None, None
            
        # 1. Load Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_dir)

        # 2. Load Model
        model = TFAutoModelForSequenceClassification.from_pretrained(
            model_dir,
            id2label=IDX_TO_LABEL
        )
        
        print("Emotion model and tokenizer loaded.")
        return model, tokenizer
        
    except Exception as e:
        print(f"Error loading emotion model from {model_dir}: {e}")
        return None, None

def run_classification(sentences: list, model, tokenizer):
    """
    Runs emotion classification on a list of sentences.

    Args:
        sentences (list): A list of sentences (in Bulgarian) to classify.
        model (TFAutoModelForSequenceClassification): The loaded model.
        tokenizer (AutoTokenizer): The loaded tokenizer.

    Returns:
        list: A list of predicted emotion labels (e.g., ['neutral', 'happiness', ...])
              or None if classification fails.
    """
    if not sentences:
        print("Classification: No sentences to classify.")
        return []
        
    try:
        print(f"Classifying {len(sentences)} sentences...")
        
        # 1. Tokenize the input sentences
        # The tokenizer expects a list of strings
        encodings = tokenizer(
            sentences,
            max_length=MAX_LEN,
            padding='max_length',
            truncation=True,
            return_tensors='np'  # Return NumPy arrays
        )
        
        # 2. Create a tf.data.Dataset for efficient prediction
        # The model expects a dictionary of {'input_ids': ..., 'attention_mask': ...}
        tf_dataset = tf.data.Dataset.from_tensor_slices(
            (dict(encodings))
        ).batch(32)  # Use a reasonable batch size for inference

        # 3. Predict
        # model.predict() returns a sequence classifier output object
        predictions = model.predict(tf_dataset, verbose=0)
        
        # 4. Get the class with the highest probability
        # The 'logits' contain the raw scores for each class
        predicted_indices = np.argmax(predictions.logits, axis=1)
        
        # 5. Map indices back to labels
        predicted_labels = [IDX_TO_LABEL.get(idx, 'unknown') for idx in predicted_indices]
        
        print("Classification complete.")
        return predicted_labels

    except Exception as e:
        print(f"Error during emotion classification: {e}")
        # Print a more detailed traceback
        import traceback
        traceback.print_exc()
        return None


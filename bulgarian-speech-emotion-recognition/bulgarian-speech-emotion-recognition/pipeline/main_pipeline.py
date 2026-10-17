"""
main_pipeline.py

This is the main script to run the complete end-to-end NLP pipeline.
It integrates transcription, translation, and emotion classification.

To run:
python main_pipeline.py --youtube-url "YOUR_YOUTUBE_URL" \
                        --api-key "YOUR_ASSEMBLYAI_API_KEY" \
                        --trans-model-dir "./my_bg_en_model_hf_base" \
                        --emotion-model-dir "./transformer_emotion_fold_1" \
                        --output-csv "final_pipeline_output.csv"
"""

import argparse
import os
import pandas as pd
from pipeline_step_1_transcribe import run_transcription
from pipeline_step_2_translate import run_translation
from pipeline_step_3_classify import load_emotion_model, run_classification

def run_full_pipeline(youtube_url, api_key, trans_model_dir, emotion_model_dir, output_csv):
    """
    Executes the full NLP pipeline from video URL to final CSV.
    """
    print("--- Starting End-to-End NLP Pipeline ---")
    
    # Define a directory to store the downloaded audio
    audio_dir = "./audio_files"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    # --- Step 1: Transcription ---
    # This function downloads the audio and returns a DataFrame
    # with "Start Time", "End Time", and "Sentence"
    df = run_transcription(youtube_url, audio_dir, api_key)

    if df is None or df.empty:
        print("Transcription failed or returned no data. Exiting pipeline.")
        return

    print(f"Step 1 Complete. Transcribed {len(df)} sentences.")
    
    # Get list of sentences to translate
    original_sentences = df["Sentence"].tolist()

    # --- Step 2: Translation ---
    # This function translates a list of sentences
    translated_sentences = run_translation(original_sentences, trans_model_dir)
    
    if translated_sentences is None:
        print("Translation failed. Exiting pipeline.")
        return

    df["Translation"] = translated_sentences
    print("Step 2 Complete. Sentences translated.")

    # --- Step 3: Emotion Classification ---
    # Load the model and tokenizer
    print("\n--- Step 3: Classification ---")
    print("Loading emotion model...")
    emotion_model, emotion_tokenizer = load_emotion_model(emotion_model_dir)
    
    if emotion_model is None or emotion_tokenizer is None:
        print("Failed to load emotion model. Exiting pipeline.")
        return 

    # --- CORRECT: Pass the original_sentences (Bulgarian) to the multilingual model ---
    # <-- FIX: Pass the loaded 'emotion_model' and 'emotion_tokenizer' variables
    emotions = run_classification(original_sentences, emotion_model, emotion_tokenizer)

    if emotions is None:
        print("Emotion classification failed. Exiting pipeline.")
        return
        
    df["Emotion"] = emotions
    print("Step 3 Complete. Emotions classified.")

    # --- Step 4: Final Output ---
    # Ensure columns are in the correct order
    final_columns = ["Start Time", "End Time", "Sentence", "Translation", "Emotion"]
    
    # Handle case where some columns might be missing (e.g., if a step fails partially)
    for col in final_columns:
        if col not in df.columns:
            df[col] = "N/A"
            
    df = df[final_columns]
    
    # Save to CSV
    try:
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"\n--- Pipeline Finished Successfully! ---")
        print(f"Output saved to: {output_csv}")
    except Exception as e:
        print(f"Error saving final CSV: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full NLP Pipeline for Emotion Classification from Video")
    
    parser.add_argument(
        "--youtube-url",
        type=str,
        required=True,
        help="The URL of the YouTube video to process."
    )
    parser.add_argument(
        "--api-key",
        type=str,
        required=True,
        help="Your AssemblyAI API key."
    )
    parser.add_argument(
        "--trans-model-dir",
        type=str,
        required=True,
        help="Path to the directory containing your fine-tuned translation model."
    )
    parser.add_argument(
        "--emotion-model-dir",
        type=str,
        required=True,
        help="Path to the directory containing your saved emotion classification model (e.g., './transformer_emotion_fold_1')."
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="final_pipeline_output.csv",
        help="Name of the final output CSV file."
    )
    
    args = parser.parse_args()
    
    run_full_pipeline(
        youtube_url=args.youtube_url,
        api_key=args.api_key,
        trans_model_dir=args.trans_model_dir,
        emotion_model_dir=args.emotion_model_dir,
        output_csv=args.output_csv
    )



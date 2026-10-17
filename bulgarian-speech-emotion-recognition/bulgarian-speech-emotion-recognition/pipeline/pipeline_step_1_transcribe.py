"""
pipeline_step_1_transcribe.py

This module handles downloading audio from a YouTube URL
and transcribing it using AssemblyAI.

It has been modified to extract sentence-level timestamps,
which are required for the final pipeline output.
"""

import assemblyai as aai
from pytubefix import YouTube
import os
import pandas as pd
import re

def downloader(URL, destination):
    """
    Downloads the audio track from a YouTube URL.
    (Original function from user)
    """
    # url input from youtube
    yt = YouTube(URL)

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download(output_path=destination)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    # Use os.replace for atomicity and to avoid errors if file exists
    if os.path.exists(new_file):
        os.remove(new_file)
    os.replace(out_file, new_file)
    return new_file

def format_timestamp(milliseconds):
    """Converts milliseconds to HH:MM:SS,mmm format."""
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def run_transcription(youtube_url, audio_dir, api_key):
    """
    Downloads and transcribes a YouTube video, returning a DataFrame 
    with 'Start Time', 'End Time', and 'Sentence'.
    """
    print(f"--- Step 1: Transcription ---")
    print("Downloading audio...")
    try:
        audio_file = downloader(youtube_url, audio_dir)
        print(f"Audio downloaded to: {audio_file}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

    print("Transcribing audio... (This may take a while)")
    aai.settings.api_key = api_key
    # Assuming Bulgarian as per original script
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.universal, language_code="bg")
    
    try:
        transcript = aai.Transcriber(config=config).transcribe(audio_file)
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

    if transcript.status == "error":
        print(f"Transcription failed: {transcript.error}")
        return None

    # CRITICAL CHANGE: Use transcript.get_sentences() to get timestamps
    sentences = transcript.get_sentences()
    if not sentences:
        print("Transcription successful, but no sentences were detected.")
        return pd.DataFrame(columns=["Start Time", "End Time", "Sentence"])

    print("Transcription successful. Processing sentences.")
    data = []
    for sent in sentences:
        data.append({
            "Start Time": format_timestamp(sent.start),
            "End Time": format_timestamp(sent.end),
            "Sentence": sent.text
        })
    
    # Clean up the downloaded audio file
    try:
        os.remove(audio_file)
        print(f"Cleaned up audio file: {audio_file}")
    except Exception as e:
        print(f"Warning: Could not remove audio file {audio_file}: {e}")
        
    return pd.DataFrame(data)


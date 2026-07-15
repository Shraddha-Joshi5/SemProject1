import os
import json
import numpy as np

from database_module import get_db_connection
from VoiceCapture import VoiceCapture

def run_multimodal_pipeline():
    print("\n Phase 1: Initializing Voice Capture System...")
    
    try:
        voice_engine = VoiceCapture(model_size='base', device='cpu')
        transcript, audio_path = voice_engine.capture_and_transcribe(duration=5)
        print(f" Transcribed Text: \"{transcript}\"")
        print(f" Audio file cached at: {audio_path}")
        system_lang = voice_engine.language
    except Exception as e:
        print(f" Voice capture init failed ({e}). Using mock speech transcription fallback...")
        transcript = "नमस्ते, मेरो नाम अदिति हो।"
        audio_path = "data/audio/mock_fallback.wav"
        system_lang = "ne"

    print("\n Phase 2: Processing Facial Vectors...")
    
    mock_face_embedding = list(np.random.uniform(-0.1, 0.1, 512))
    person_name = "Aditi Pradhan"
    print(f" Generated {len(mock_face_embedding)}-dimensional face embedding vector.")
    
    print("\n Phase 3: Packaging and Injecting into PostgreSQL...")
    
    metadata_context = {
        "audio_source_file": os.path.basename(audio_path),
        "voice_note_transcript": transcript,  
        "device_tag": "desktop_microphone",
        "system_language": system_lang
    }
    
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        
        cursor.execute(
            "INSERT INTO public.persons (name) VALUES (%s) RETURNING person_id;",
            (person_name,)
        )
        person_id = cursor.fetchone()[0]
        
        
        cursor.execute(
            """
            INSERT INTO public.face_embeddings (person_id, embedding, context)
            VALUES (%s, %s::vector, %s);
            """,
            (person_id, mock_face_embedding, json.dumps(metadata_context))
        )
        
        conn.commit()
        print("\n SUCCESS! Face vector and audio transcript successfully stored inside PostgreSQL.")
        
    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback()
        print(f"\n Pipeline insertion transaction failed: {e}")
        print(" Hint: If running outside a Docker network, make sure host='localhost' in database_module.py")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    run_multimodal_pipeline()
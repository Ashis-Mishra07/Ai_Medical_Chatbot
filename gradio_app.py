import os
import gradio as gr
from dotenv import load_dotenv

from brain import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from voice_of_doctor import text_to_speech_with_gtts

load_dotenv()

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image? Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Always answer as if you are answering a real person.
Start your answer right away, no markdown or AI talk. Keep it max 2 sentences."""

def process_inputs(audio_filepath, image_filepath):
    # Step 1: Transcribe
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Step 2: Vision + Diagnosis
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Step 3: TTS
    doctor_voice_path = "final_doctor_response.wav"
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=doctor_voice_path)

    # ✅ Only return transcript, diagnosis, and doctor's voice
    return speech_to_text_output, doctor_response, doctor_voice_path


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(type="filepath", label="Patient's Voice"),
        gr.Image(type="filepath", label="Medical Image")
    ],
    outputs=[
        gr.Textbox(label="Transcribed Text"),
        gr.Textbox(label="Doctor's Diagnosis"),
        gr.Audio(label="Doctor's Voice", type="filepath")
    ],
    title="🧠 AI Doctor with Vision & Voice"
)




iface.launch(debug=True)

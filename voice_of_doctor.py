import os
from gtts import gTTS
import elevenlabs
from elevenlabs.client import  ElevenLabs
from dotenv import load_dotenv
load_dotenv()
from pydub import AudioSegment


ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
input_text = "Hello, Myself Ashis Kumar Mishra . I am from NIT Rourkela currently in my final year ."



def text_to_speech_with_gtts_old(input_text , output_filepath):
    language = 'en'

    audioobj = gTTS(
        text = input_text ,
        lang = language,
        slow = False
    )
    audioobj.save(output_filepath)

# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")


def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)


# text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 





import subprocess
import platform
import pygame

AudioSegment.converter = "/usr/bin/ffmpeg"

# def text_to_speech_with_gtts(input_text, output_filepath):
#     language="en"

#     audioobj= gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)
    

#     return output_filepath 

def text_to_speech_with_gtts(input_text, output_filepath):
    # Step 1: Save TTS output as temp MP3
    temp_mp3 = "temp_voice.mp3"
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(temp_mp3)

    # Step 2: Convert MP3 to WAV
    audio = AudioSegment.from_mp3(temp_mp3)
    audio.export(output_filepath, format="wav")

    # Step 3: Clean up temp MP3
    os.remove(temp_mp3)

    # Step 4: Return WAV path
    return output_filepath

# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")
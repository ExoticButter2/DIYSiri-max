from faster_whisper import WhisperModel
from kokoro import KPipeline
import soundfile as sf
import torch
import numpy
from google import genai

client = genai.Client()

pipeline = KPipeline(lang_code='a', device='cpu')

model_size = "large-v3"

model = WhisperModel(model_size, device="cpu", compute_type="int8")

def ProcessAudioPrompt(audioPromptArray):
    reshapedPromptArray = audioPromptArray.reshape(-1, 1)
    sf.write("prompt.wav", reshapedPromptArray, 16000)
    
    segments, _ = model.transcribe("prompt.wav", beam_size=5)
    transcription = " ".join([segment.text for segment in segments])
    
    print("Transcribed audio")
    
    return transcription
    
def ProcessTextPrompt(textPrompt):
    try:
        response = client.models.generate_content(
            model = "gemini-3.1-flash-lite",
            contents = [textPrompt + " Answer in maximum 60 words."]
        )
        
        if response.text:
            print(response.text)
            return response.text
    except Exception as e:
        print(f"Failed text generation: {e}")
    
    if not response.text:
        print("Gemini text generation failed")
    
    print("Text generation failed")
    
    return "Failed to generate text response."
    
def ConvertTextResponseToAudio(textResponse):
    ttsAudioArray = []
    generator = pipeline(textResponse, voice='am_eric')
    
    for _, _, audio in generator:
        ttsAudioArray.append(audio)
        
    concatArray = numpy.concatenate(ttsAudioArray)
    convertedArray = concatArray
    
    print("Generated tts response")
    return concatArray
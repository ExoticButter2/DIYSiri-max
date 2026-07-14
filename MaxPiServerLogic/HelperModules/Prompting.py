from ollama import chat
from faster_whisper import WhisperModel
from kokoro import KPipeline
import soundfile as sf
import torch
import numpy

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
    response = chat(
        model='qwen3.5:9b',
        messages=[{'role': 'user', 'content': textPrompt}],
        keep_alive=-1,
        options={
            "temperature": 0.2
        },
        think=False
    )
    
    if not response.message.content:
        print("Ollama text generation failed")
        return "I'm sorry, I couldn't generate a response."
    
    print("Generated ollama text prompt")
    
    return response.message.content
    
def ConvertTextResponseToAudio(textResponse):
    ttsAudioArray = []
    generator = pipeline(textResponse, voice='am_eric')
    
    for _, _, audio in generator:
        ttsAudioArray.append(audio)
        
    concatArray = numpy.concatenate(ttsAudioArray)
    
    print("Generated tts response")
    return concatArray
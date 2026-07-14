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

previousPromptId = None

def ProcessAudioPrompt(audioPromptArray):
    reshapedPromptArray = audioPromptArray.reshape(-1, 1)
    sf.write("prompt.wav", reshapedPromptArray, 16000)
    
    segments, _ = model.transcribe("prompt.wav", beam_size=5)
    transcription = " ".join([segment.text for segment in segments])
    
    print("Transcribed audio")
    
    return transcription
    
def ProcessTextPrompt(textPrompt):
    try:
        if previousPromptId != None:
            interaction = client.interactions.create(
                model = "gemini-3.1-flash-lite",
                input = f"{textPrompt} Use maximum 50 words.",
                generation_config = {
                    "thinking_level": "low"
                },
                store = True,
                previous_interaction_id=previousPromptId
            )
            
            print(interaction.output_text)
            previousPromptId = interaction.id
            return interaction.output_text
        else:
            interaction = client.interactions.create(
                model = "gemini-3.1-flash-lite",
                input = f"{textPrompt} Use maximum 50 words.",
                generation_config = {
                    "thinking_level": "low"
                },
                store = True,
            )
            
            print(interaction.output_text)
            previousPromptId = interaction.id
            return interaction.output_text
    except Exception as e:
        print(f"Failed text generation: {e}")
    
    print("Text generation failed")
    
    return "Failed to generate text response."
    
def ConvertTextResponseToAudio(textResponse):
    ttsAudioArray = []
    generator = pipeline(textResponse, voice='am_eric')
    
    for _, _, audio in generator:
        ttsAudioArray.append(audio)
        
    concatArray = numpy.concatenate(ttsAudioArray)
    
    print("Generated tts response")
    return concatArray
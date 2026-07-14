from ollama import chat
from google import genai
from faster_whisper import WhisperModel
from kokoro import KPipeline
import soundfile as sf
import numpy

pipeline = KPipeline(lang_code='a', device='cpu')

model_size = "large-v3"

model = WhisperModel(model_size, device="cpu", compute_type="int8")

client = genai.Client()

mode = 'cloud'#OPTIONS: mode = 'cloud' (gemini), mode = 'local' (ollama)
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
        if mode == 'local':
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
            
            print(response.message.content)
            
            return response.message.content
        elif mode == 'cloud':
            global previousPromptId
            if previousPromptId:
                interaction = client.interactions.create(
                    model = "gemini-3.1-flash-lite",
                    input = f"{textPrompt} Use maximum 50 words.",
                    generation_config = {
                        "thinking_level": "low",
                    },
                    store = True,
                    previous_interaction_id=previousPromptId
                )
                
                previousPromptId = interaction.id
                
                print(interaction.output_text)
                return interaction.output_text
            else:
                interaction = client.interactions.create(
                    model = "gemini-3.1-flash-lite",
                    input = f"{textPrompt} Use maximum 50 words.",
                    generation_config = {
                        "thinking_level": "low"
                    },
                    store = True
                )
                
                previousPromptId = interaction.id
                
                print(interaction.output_text)
                return interaction.output_text
    except Exception as e:
        print(f"Failed to generate text response: {e}")
        
    return "I'm sorry, I couldn't generate a response."
    
def ConvertTextResponseToAudio(textResponse):
    ttsAudioArray = []
    generator = pipeline(textResponse, voice='am_eric')
    
    for _, _, audio in generator:
        ttsAudioArray.append(audio)
        
    concatArray = numpy.concatenate(ttsAudioArray)
    
    print("Generated tts response")
    return concatArray
from google import genai

client = genai.Client()

audioFileName = "audioResponse.wav"

def OnFail(exception):
    print(f"Exception: {exception}")

def AudioPromptToText(filePath):
    try:
        audio_prompt = client.files.upload(file = filePath)
        extra_text_prompt = "Write a maximum 80 word response to the audio file."
        
        response = client.models.generate_content(
            model ="gemini-3.1-flash-lite",
            contents = [audio_prompt, extra_text_prompt]
        )
    except Exception as e:
        OnFail(e)
    else:
        print(response)#only for debugging
        return response
from ollama import chat
from google import genai

client = genai.Client(vertexai=False)

def ProcessTextPrompt(textPrompt):
    try:
        # response = chat(
        #     model='qwen3.5:2b',
        #     messages=[{'role': 'user', 'content': textPrompt + "Answer with less than 50 words."}],
        #     keep_alive=-1,
        #     options={
        #         "temperature": 1.0,
        #         "top_p": 0.95,
        #         "top_k": 20,
        #         "min_p": 0.0,
        #         "presence_penalty": 1.5,
        #         "repetition_penalty": 1.0
        #     }
        # )
        
        response = client.models.generate_content(
            model = "gemini-3.1-flash-lite",
            contents = [textPrompt + " Answer in maximum 60 words."]
        )
        
        if response.text:
            print("Generated gemini text prompt")
            return response.text
    
    except Exception as e:
        print(f"Failed text generation: {e}")
    
    print("Text generation failed")
    return "I'm sorry, I couldn't generate a response."

regularResponse = ProcessTextPrompt("Give me an operation one loadout in roblox")
print(regularResponse)

# response = chatSession.send("What is in your opinion the best gun in operation one?")
# print(response)
# secondResponse = chatSession.send("Why?")
# print(secondResponse)

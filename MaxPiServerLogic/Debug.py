from ollama import chat
from google import genai

client = genai.Client(vertexai=False)

previousPromptId = None

def ProcessTextPrompt(textPrompt):
    try:
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
        print(f"Failed text generation: {e}")
    
    print("Text generation failed")
    
    return "Failed to generate text response."

print("First response:")
regularResponse = ProcessTextPrompt("Do you know anything about the new g36 weapon in operation one roblox? What attachments does it have?")
print("Second response:")
contextResponse = ProcessTextPrompt("Why?")
print("Third response:")
ultraContextResponse = ProcessTextPrompt("What did you say 2 prompts before this?")
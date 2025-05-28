import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-preview-05-20"

# Load system prompt or fallback
prompt = (
    open("system-prompt.txt", encoding="utf-8").read().strip()
    if os.path.exists("system-prompt.txt")
    else "Você é o chatbot da Altervision para atendimento de clientes inbound. Responda com educação e simplicidade."
)

history = [{"role": "model", "text": prompt}]

def chat():
    print("Chatbot Altervision (digite 'x' para sair)")
    while True:
        msg = input("You: ")
        if msg.lower() == 'x':
            print("Tchau!")
            break
        history.append({"role": "user", "text": msg})

        # Stream and print response
        resp = []
        contents = [
            types.Content(
                role=e["role"],
                parts=[types.Part(text=e["text"])],
            )
            for e in history
        ]
        config = types.GenerateContentConfig(response_mime_type="text/plain")

        for chunk in client.models.generate_content_stream(
            model=MODEL,
            contents=contents,
            config=config,
        ):
            print(chunk.text, end="", flush=True)
            resp.append(chunk.text)
        print()

        history.append({"role": "model", "text": ''.join(resp)})

if __name__ == '__main__':
    chat()

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.9)

response = chat_model.invoke("What is the capital of France?")
print(response.content)

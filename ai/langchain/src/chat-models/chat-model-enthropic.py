from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatAnthropic(model="claude-2", temperature=0.9)

response = chat_model.invoke("What is the capital of France?")
print(response.content)

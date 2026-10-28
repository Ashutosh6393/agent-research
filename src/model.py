from dotenv import load_dotenv
from langchain_xai import ChatXAI

load_dotenv()


model = ChatXAI(model="grok-4", temperature=0)

response = model.invoke("What is the weather in Tokyo?")

print(response.content)

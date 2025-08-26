import os

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

# Need to call this to load env variables into os. Can be moved to main.py
load_dotenv()

# Initialize OpenAI model (you can use gpt-4o-mini for cheap or gpt-4o for advanced)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

# Create the conversation chain
conversation = ConversationChain(llm=llm, verbose=True)

print("AI Agent Ready! Type 'exit' to quit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = conversation.run(user_input)
    print("AI:", response)

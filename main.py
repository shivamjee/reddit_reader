import logging as log
import os
import uvicorn
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_community.cache import InMemoryCache

from router.chat_router import chat_router
from router.health_router import health_router
from router.reddit_reader_router import reddit_reader_router
from dotenv import load_dotenv

#Intialize logging
log.basicConfig(
    level=log.INFO,  # or INFO depending on your needs
    format="%(asctime)s [%(levelname)s] %(message)s",
)

#Initialize Environment Variables
load_dotenv()
log.info(f"Env variables loaded")

# Initialize OpenAI model (you can use gpt-4o-mini for cheap or gpt-4o for advanced)
cache = InMemoryCache()
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
    cache=cache
)
log.info(f"LLM connection Loaded")

#Initialize FastAPI Router
app = FastAPI()

app.state.llm = llm
app.include_router(health_router)
app.include_router(reddit_reader_router, prefix="/reddit")
app.include_router(chat_router, prefix="/chat")

log.info(f"FastAPI loaded, Application setup complete")


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
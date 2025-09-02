import logging as log
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from langchain_core.runnables.base import RunnableSerializable
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional
import json
import os

from helper.json_reader import extract_bodies

# Build the chain lazily (on first request)
chain: Optional[RunnableSerializable] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chain
    llm = app.state.llm
    analysis_prompt = ChatPromptTemplate.from_template("""
            You are an expert content analyst. Analyze the following Q&A and return a JSON with the following fields:
            - political: true or false
            - leaning: "left", "right", "centrist", or "none"
            - helpfulness: "high", "medium", "low" (how useful is the answer)
            - explanation: a short explanation for your classifications.

            Q: {question}
            A: {answer}
            """)
    chain = analysis_prompt | llm | JsonOutputParser()
    yield
reddit_reader_router = APIRouter(lifespan=lifespan)

@reddit_reader_router.get('/')
async def get_reddit_details():

    #need to update this function to get json from internet based on query params, instead of using a static file
    output = await get_json()

    result = await chain.ainvoke(output)
    log.info(f"Response from AI: {result}")
    return result


async def get_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Load JSON from file
    with open(os.path.join(current_dir, "reddit.json"), "r") as f:
        data = json.load(f)

    question, answer = extract_bodies(data)
    # Return JSON of all body values
    output = {"question": question, "answer": answer}
    # Print or save to file
    print(json.dumps(output, indent=2))
    return output
import logging as log
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Query, HTTPException
from langchain_core.runnables.base import RunnableSerializable
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional

from helper.url_helper import extract_json_from_url, add_json_to_url, validate_reddit_url
from helper.json_reader import pre_process_reddit_json

# Build the chain lazily (on first request)
chain: Optional[RunnableSerializable] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chain
    llm = app.state.llm
    analysis_prompt = ChatPromptTemplate.from_template("""
    You are an expert discourse analyst with speciality in reddit threads.
    
    You will be provided with a list of JSON object representing a thread of question, comments and its replies. 
    Each item contains:
    - "question": This represents the main topic that the rest of the comments will be about
    - "author": The username of the person starting the topic
    OR
    - "body": A comment to the question.
    - "author": The username of the commenter.
    - "replies": A list of nested replies with the same structure.
    
    Your task:
    1. Determine if the overall conversation is **political or non-political**.
    2. If political:
       - Identify if the conversation is **left-leaning or right-leaning**, with a confidence percentage (e.g., "Left: 70%" or "Right: 60%").
    3. Assess the **helpfulness** of the conversation: does it meaningfully answer or address the main topic?
    4. Provide a **short explanation** summarizing the discussion.
    
    Return your answer as JSON in this format:
    {{
      "is_political": true/false,
      "leaning": "Left: X%" or "Right: X%" or null,
      "helpfulness": "High" / "Medium" / "Low",
      "explanation": "A concise summary of the discussion."
    }}
    
    Now analyze this thread:
    
    {pre_processed_data}
    """)
    chain = analysis_prompt | llm | JsonOutputParser()
    yield
reddit_reader_router = APIRouter(lifespan=lifespan)

@reddit_reader_router.get('/')
async def get_reddit_details(url: str = Query(..., description="URL to fetch Reddit-style JSON")):

    try:

        #URL validations
        if not validate_reddit_url(url):
            return {"supported": False}

        #Add .json to url
        url = add_json_to_url(url)

        #get json data from url
        json_response = extract_json_from_url(url)

        #Pre-process the data to send it to model
        pre_processed_data = pre_process_reddit_json(json_response)

        result = await chain.ainvoke({"pre_processed_data" : pre_processed_data})
        log.info(f"Response from AI: {result}")
        return result
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=400, detail=str(e))


#http://127.0.0.1:8000/reddit?url=https://www.reddit.com/r/PoliticalDebate/comments/1n6yyv7/israel_ideal_model_for_minorities_developmental/
#http://127.0.0.1:8000/reddit/?url=https://www.reddit.com/r/travel/comments/1bs2azu/how_do_you_give_a_trip_as_a_gift

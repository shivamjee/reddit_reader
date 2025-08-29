import logging as log
import os
import uuid

from pojo.chat_pojo import *
from fastapi import APIRouter, Request
from langchain.chains.conversation.base import ConversationChain
from starlette.responses import FileResponse

# Steps to load the UI. These details are initialized once on startup when importing the file in main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(current_dir, '../templates')

if not os.path.exists(templates_path):
    raise RuntimeError(f"Template folder '{templates_path}' doesn't exist.")

chat_router = APIRouter()
@chat_router.get("/")
@chat_router.get("/load")
async def star_chat():
    """
        Loading the chat UI
    """

    log.info(f"Chat UI Loading...")
    return FileResponse(os.path.join(templates_path, "chat_ui.html"))

# Temporary in-memory store
conversation_store = {}
@chat_router.get("/start", response_model=ConversationResponse)
async def star_chat(request: Request):
    """
            Starts a chat. It initializes a conversationChain with the OpenAI LLM and creates a conversationId for tracking purposes
    """
    llm = request.app.state.llm
    conversation_id = str(uuid.uuid4())
    conversation_store[conversation_id] = ConversationChain(llm=llm, verbose=True)
    log.info(f"Starting chat with conversation id: {conversation_id}")
    return ConversationResponse(conversation_id=conversation_id)

@chat_router.post("/send", response_model=MessageResponse)
async def send_chat_message(message_request: MessageRequest):
    """
        Send a chat message to LLM. The API responds with a response from the LLM model
    """

    log.info(f"Request from user: {message_request.message} for conversation: {message_request.conversation_id}")
    conversation = conversation_store[message_request.conversation_id]
    response = conversation.run(message_request.message)
    log.info(f"Response from AI: {response}")
    return MessageResponse(reply=response)
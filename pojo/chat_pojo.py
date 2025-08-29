from pydantic import BaseModel


class MessageRequest(BaseModel):
    """
        Message Request Model for Chat System
    """
    conversation_id: str
    message: str

class MessageResponse(BaseModel):
    """
        Response Model from the AI model
    """
    reply: str

class ConversationResponse(BaseModel):
    """
        Response Model with conversation details when the chat starts
    """
    conversation_id: str
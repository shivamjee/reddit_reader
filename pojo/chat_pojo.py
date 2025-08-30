from pydantic import BaseModel


class MessageRequest(BaseModel):
    """
        Message Request Model for Chat System
    """
    session_id: str
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
    session_id: str
from fastapi import APIRouter

from router.health_router import HealthResponse

reddit_reader_router = APIRouter()

@reddit_reader_router.get('/', response_model=HealthResponse)
async def get_reddit_details():
    return HealthResponse(status="RedditReader ok")

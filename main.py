import uvicorn
from fastapi import FastAPI
from router.health_router import health_router
app = FastAPI()
app.include_router(health_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
# reddit_reader
1. AI agent that that scans and summarises reddit posts. 
2. ChatSystem -> Something similar to chatGPT

### How to run this project

1. create venv with 3.11 or higher
2. create .env file and add OPENAI_API_KEY to it
3. Install Packages using ->  `pip install -r requirements.txt`
4. Run the main app using -> `uvicorn main:app --reload` or run the main.py file using any code editor


### API Documentation 

All API documentation can be found here-> http://127.0.0.1:8000/docs#/

### ChatSystem

Start chat system by calling -> http://127.0.0.1:8000/chat/

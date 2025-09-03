# reddit_reader
1. AI agent that scans and summarises reddit posts.
2. Chrome extension integration to allow the AI agent to share its findings for every google search result by clicking the "analyze" button next to each result.
3. ChatSystem -> Something similar to chatGPT

### How to run this project

1. create venv with 3.11 or higher
2. create .env file and add OPENAI_API_KEY to it
3. Install Packages using ->  `pip install -r requirements.txt`
4. Run the main app using -> `uvicorn main:app --reload` or run the main.py file using any code editor


### API Documentation 

All API documentation can be found here-> http://127.0.0.1:8000/docs#/

### ChatSystem

Start chat system by calling -> http://127.0.0.1:8000/chat/

### How to add chrome extension

1. Go to -> chrome://extensions/
2. toggle developer mode in top right
3. Click load unpacked
4. Navigate to the chrome-extension folder in this repo
5. Click add
6. Ensure application is up and running before clicking on the icons

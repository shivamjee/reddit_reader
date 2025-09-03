import requests

def extract_json_from_url(url: str):
    """Fetches JSON from a URL and extracts comment bodies/authors."""
    response = requests.get(url, headers={"User-Agent": "fastapi-app/1.0"})
    response.raise_for_status()
    json_data = response.json()

    return json_data

def validate_reddit_url(url: str):
    """Validates that the input URL starts with https://reddit.com."""
    return  url.startswith("https://www.reddit.com")

def add_json_to_url(url: str):
    """Adds /.json to input URL."""
    return url + ".json" if url.endswith("/") else url + "/.json"
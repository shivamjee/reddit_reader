#Pythom file which takes a reddit json and formats it in a prompt readable json for processing

def extract_comment(item):
    """
    Extract a single comment's body, author, and its nested replies (if any).
    Returns a dict: { "body": str, "author": str, "replies": [...] } or {"question": question, "author": author} (if it is a question)
    """

    # Each item is expected to have 'data'
    if not isinstance(item, dict) or 'data' not in item:
        return None

    data = item['data']

    # Extract the body
    body = data.get("body")
    author = data.get("author")
    question = data.get("selftext")
    if question:
        return {"question": question, "author": author}
    if not body:  # Skip items without a body
        return None

    # Check for replies (may be empty string or actual JSON)
    replies = data.get('replies')
    replies_list = []

    if replies and isinstance(replies, dict):
        # Recursively process replies: replies['data']['children']
        children = replies.get('data', {}).get('children', [])
        for child in children:
            nested = extract_comment(child)
            if nested:
                replies_list.append(nested)

    return {"body": body, "author": author, "replies": replies_list}


def pre_process_reddit_json(json_data):
    """
    Traverses the top-level list and extracts all comments
    with their nested replies.
    """
    comments = []

    def traverse(item):
        # Ensure it's a valid dict with 'data' and maybe 'children'
        if not isinstance(item, dict) or 'data' not in item:
            return

        data = item['data']
        if 'children' in data and isinstance(data['children'], list):
            for child in data['children']:
                comment = extract_comment(child)
                if comment:
                    comments.append(comment)

    if isinstance(json_data, list):
        for item in json_data:
            traverse(item)

    return comments
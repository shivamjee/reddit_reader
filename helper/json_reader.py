#This function only fetches top level questions and answers, and does not account for replies to particular answers.

def extract_bodies(json_data):
    """
    Recursively traverse the Reddit-like JSON structure
    and extract all "body" values.
    """
    answers = []
    questions = []

    def traverse(item):
        # Check if item has 'data'
        if not isinstance(item, dict) or 'data' not in item:
            return

        data = item['data']

        # If 'body' exists in this data, add it
        if 'body' in data:
            answers.append(data['body'])
        if 'selftext' in data:
            questions.append(data['selftext'])


        # If 'children' exist, recurse into each child
        if 'children' in data and isinstance(data['children'], list):
            for child in data['children']:
                traverse(child)

    # The top-level JSON is a list of items
    if isinstance(json_data, list):
        for item in json_data:
            traverse(item)

    return questions, answers
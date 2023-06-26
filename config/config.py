import json
with open('config.json', 'r') as f:
    config = json.load(f)


def get_openai_api_key():
    return config['OPENAI_API_KEY']

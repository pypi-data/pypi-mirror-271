import json


def parse_json_file(filepath: str) -> dict:
    with open(filepath) as file:
        json_content: dict = json.load(file)
        return json_content

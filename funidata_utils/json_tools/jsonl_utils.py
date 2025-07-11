import json


def read_jsonl(jsonl_file_path: str) -> list[dict]:
    list_of_dicts: list[dict] = []
    try:
        with open(jsonl_file_path) as f:
            for line in f:
                json_data = json.loads(line)
                list_of_dicts.append(json_data)
    except FileNotFoundError as e:
        print(f"File {jsonl_file_path} not found.")
        raise e
    return list_of_dicts


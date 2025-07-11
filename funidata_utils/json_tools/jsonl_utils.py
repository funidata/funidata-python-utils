import simplejson

from src.json_tools.json_encoder import CustomJsonEncoder


def read_jsonl(jsonl_file_path: str) -> list[dict]:
    list_of_dicts: list[dict] = []
    try:
        with open(jsonl_file_path) as f:
            for line in f:
                json_data = simplejson.loads(line)
                list_of_dicts.append(json_data)
    except FileNotFoundError as e:
        print(f"File {jsonl_file_path} not found.")
        raise e
    return list_of_dicts


def write_jsonl(jsonl_file_path: str, list_of_dicts: list[dict]) -> None:
    try:
        with open(jsonl_file_path, 'w+') as f:
            for json_data in list_of_dicts:
                f.write(simplejson.dumps(json_data, cls=CustomJsonEncoder, ensure_ascii=False))
                f.write('\n')
    except FileNotFoundError as e:
        print(f"File {jsonl_file_path} not found.")
        raise FileNotFoundError(e)

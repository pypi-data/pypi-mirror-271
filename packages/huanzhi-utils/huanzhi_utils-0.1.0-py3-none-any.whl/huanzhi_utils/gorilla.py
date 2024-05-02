import json
import os

def load_file(file_path:str):
    result = []
    with open(file_path) as f:
        file = f.readlines()
        for line in file:
            result.append(json.loads(line))
    return result


def write_list_of_dicts_to_file(filename: str, data: list, subdir=None, appendMode=False):
    if subdir:
        # Ensure the subdirectory exists
        os.makedirs(subdir, exist_ok=True)

        # Construct the full path to the file
        filename = os.path.join(subdir, filename)

    # Write the list of dictionaries to the file in JSON format
    with open(filename, "a" if appendMode else "w") as f:
        for i, entry in enumerate(data):
            json_str = json.dumps(entry)
            f.write(json_str)
            if i < len(data) - 1:
                f.write("\n")
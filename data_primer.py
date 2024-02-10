### This scripts parses this file: input_data.jsonl and sets the system promt to the value of system_prompt.txt

import json

# Read the content from the system_prompt.txt file
with open("system_prompt.txt", "r") as file:
    content = file.read().strip()

# Process each line from the original .jsonl file and write to primed_data.jsonl
with open("input_data.jsonl", "r") as input_file, open("primed_data.jsonl", "w") as output_file:
    for line in input_file:
        try:
            data = json.loads(line)
            for message in data["messages"]:
                if message["role"] == "system":
                    message["content"] = content
            output_file.write(json.dumps(data) + "\n")

        except json.JSONDecodeError:
            print(f"Error decoding JSON for line: {line}")
            raise



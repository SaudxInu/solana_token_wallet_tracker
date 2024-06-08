import os
import json


def create_directory_if_not_exists(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_file_if_not_exists(file_path: str) -> None:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass


def read_input(input_file_path: str) -> list:
    lines = []
    with open(input_file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())

    return lines


def write_output(output: dict, output_file_path: str) -> None:
    output_as_str = json.dumps(output)
        
    with open(output_file_path, 'a') as file:
        file.write(output_as_str + '\n')

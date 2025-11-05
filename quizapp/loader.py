import json
import os

def load_quiz_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка: файл {file_path} поврежден")
        return None

def get_quiz_list(folder_path="tests"):
    quiz_files = []
    try:
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                quiz_files.append(file)
    except FileNotFoundError:
        print(f"Папка {folder_path} не найдена")
    return quiz_files
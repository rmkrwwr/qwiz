"""
Модуль загрузки данных викторины.

Обеспечивает загрузку тестов из базы данных.
"""

import json
import os
from . import database

def load_quiz_from_db(quiz_id=None):
    """Загружает данные викторины из базы данных.

    Args:
        quiz_id (int, optional): ID викторины. По умолчанию None (первая викторина).

    Returns:
        dict or None: Словарь с данными викторины или None при ошибке
    """
    return database.get_quiz_from_db(quiz_id)

def get_quiz_list():
    """Получает список доступных викторин.

    Returns:
        list: список викторин с id и названиями
    """
    return database.get_available_quizzes()


def load_quiz_from_file(file_path):
    """Загружает данные викторины из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу с викториной

    Returns:
        dict or None: Словарь с данными викторины или None при ошибке
    """
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

def get_quiz_list_files(folder_path="tests"):
    """Получает список доступных файлов с викторинами.

    Args:
        folder_path (str, optional): путь к папке с тестами. По умолчанию "tests".

    Returns:
        list: список имен JSON-файлов с викторинами
    """
    quiz_files = []
    try:
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                quiz_files.append(file)
    except FileNotFoundError:
        print(f"Папка {folder_path} не найдена")
    return quiz_files
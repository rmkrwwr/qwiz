"""
Модуль для работы с PostgreSQL базой данных викторин.
"""

import psycopg2
import json
import os
from typing import List, Dict, Any

def get_connection():
    """Устанавливает соединение с PostgreSQL базой данных."""
    try:
        conn = psycopg2.connect(
            dbname="quizapp_db",
            user="postgres",
            password="admin",  # ЗАМЕНИТЕ НА ВАШ ПАРОЛЬ!
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def init_database():
    """Инициализирует базу данных и создает таблицы."""
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                quiz_id INTEGER REFERENCES quizzes(id),
                text TEXT NOT NULL,
                option1 TEXT NOT NULL,
                option2 TEXT NOT NULL,
                option3 TEXT NOT NULL,
                option4 TEXT NOT NULL,
                correct_answer INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id SERIAL PRIMARY KEY,
                user_name TEXT NOT NULL,
                quiz_id INTEGER REFERENCES quizzes(id),
                correct_answers INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage DECIMAL(5,2) NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        print("База данных PostgreSQL инициализирована успешно")
        return True

    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def migrate_json_to_db(json_folder="tests"):
    """Мигрирует данные из JSON-файлов в PostgreSQL базу данных."""

    def get_quiz_list_files(folder_path="tests"):
        quiz_files = []
        try:
            for file in os.listdir(folder_path):
                if file.endswith('.json'):
                    quiz_files.append(file)
        except FileNotFoundError:
            print(f"Папка {folder_path} не найдена")
        return quiz_files

    def load_quiz_from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Ошибка загрузки файла {file_path}: {e}")
            return None

    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions")
        cursor.execute("DELETE FROM quizzes")

        quiz_files = get_quiz_list_files(json_folder)

        for quiz_file in quiz_files:
            quiz_path = f"{json_folder}/{quiz_file}"
            quiz_data = load_quiz_from_file(quiz_path)

            if quiz_data:
                cursor.execute(
                    "INSERT INTO quizzes (name, description) VALUES (%s, %s) RETURNING id",
                    (quiz_data['name'], quiz_data.get('description', ''))
                )
                quiz_id = cursor.fetchone()[0]
                for question in quiz_data['questions']:
                    options = question['options']
                    while len(options) < 4:
                        options.append("")

                    cursor.execute(
                        """INSERT INTO questions 
                        (quiz_id, text, option1, option2, option3, option4, correct_answer) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (quiz_id, question['text'],
                         options[0], options[1], options[2], options[3],
                         question['correct_answer'])
                    )

        conn.commit()
        print(f"Мигрировано {len(quiz_files)} викторин в PostgreSQL базу данных")
        return True

    except psycopg2.Error as e:
        print(f"Ошибка при миграции данных: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_quiz_from_db(quiz_id=None):
    """Загружает викторину из базы данных."""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        if quiz_id is None:
            cursor.execute("SELECT id FROM quizzes ORDER BY id LIMIT 1")
            result = cursor.fetchone()
            if result:
                quiz_id = result[0]
            else:
                return None

        cursor.execute("SELECT name, description FROM quizzes WHERE id = %s", (quiz_id,))
        quiz_row = cursor.fetchone()

        if not quiz_row:
            return None

        quiz_data = {
            'id': quiz_id,
            'name': quiz_row[0],
            'description': quiz_row[1],
            'questions': []
        }

        cursor.execute(
            """SELECT text, option1, option2, option3, option4, correct_answer 
            FROM questions WHERE quiz_id = %s ORDER BY id""",
            (quiz_id,)
        )

        for question_row in cursor.fetchall():
            options = [question_row[1], question_row[2], question_row[3], question_row[4]]
            options = [opt for opt in options if opt]

            quiz_data['questions'].append({
                'text': question_row[0],
                'options': options,
                'correct_answer': question_row[5]
            })

        return quiz_data

    except psycopg2.Error as e:
        print(f"Ошибка при загрузке викторины: {e}")
        return None
    finally:
        conn.close()

def get_available_quizzes():
    """Получает список доступных викторин из базы данных."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description FROM quizzes ORDER BY id")
        quizzes = []

        for row in cursor.fetchall():
            quizzes.append({
                'id': row[0],
                'name': row[1],
                'description': row[2]
            })

        return quizzes

    except psycopg2.Error as e:
        print(f"Ошибка при получении списка викторин: {e}")
        return []
    finally:
        conn.close()

def add_quiz_result(user_name, quiz_id, correct_answers, total_questions):
    """Добавляет результат прохождения викторины в базу данных."""
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        cursor.execute(
            """INSERT INTO quiz_results 
            (user_name, quiz_id, correct_answers, total_questions, percentage) 
            VALUES (%s, %s, %s, %s, %s)""",
            (user_name, quiz_id, correct_answers, total_questions, percentage)
        )

        conn.commit()
        return True

    except psycopg2.Error as e:
        print(f"Ошибка при сохранении результата: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
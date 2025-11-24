"""
Модуль команд приложения.

Содержит функции для обработки команд от пользователя:
показа списка тестов и запуска выбранной викторины.
"""

from . import loader, engine, results, database


def show_available_quizzes():
    """Показывает список доступных викторин."""
    quiz_list = loader.get_quiz_list()
    if not quiz_list:
        print("Тесты не найдены")
        return

    print("Доступные тесты:")
    for quiz in quiz_list:
        print(f"  ID: {quiz['id']}. {quiz['name']} - {quiz['description']}")


def run_selected_quiz(quiz_id=None, shuffle=False):
    """Запускает выбранную викторину.

    Args:
        quiz_id (int, optional): ID викторины. По умолчанию None.
        shuffle (bool, optional): флаг перемешивания вопросов. По умолчанию False.
    """
    quiz_list = loader.get_quiz_list()
    if not quiz_list:
        print("Нет доступных тестов")
        return

    if not quiz_id:
        print("Доступные тесты:")
        for quiz in quiz_list:
            print(f"  ID: {quiz['id']}. {quiz['name']}")

        try:
            quiz_id = int(input("Выберите ID теста: "))
        except ValueError:
            print("Нужно ввести число")
            return


    user_name = input("Введите ваше имя для сохранения результата: ").strip()
    if not user_name:
        user_name = "Аноним"

    quiz_data = loader.load_quiz_from_db(quiz_id)

    if quiz_data:
        correct, total = engine.start_quiz(quiz_data, mix_questions=shuffle)
        results.show_quiz_results(correct, total, quiz_data['name'], quiz_id, user_name)
    else:
        print("Тест не найден")


def init_database():
    """Инициализирует базу данных и мигрирует данные из JSON."""
    if database.init_database():
        database.migrate_json_to_db()
        print("База данных PostgreSQL готова к работе")
    else:
        print("Ошибка инициализации базы данных")
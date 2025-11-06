"""
Модуль команд приложения.

Содержит функции для обработки команд от пользователя:
показа списка тестов и запуска выбранной викторины.
"""

from . import loader, engine, results


def show_available_quizzes():
    """Показывает список доступных викторин."""
    quiz_files = loader.get_quiz_list()
    if not quiz_files:
        print("Тесты не найдены")
        return

    print("Доступные тесты:")
    for i, quiz_file in enumerate(quiz_files, 1):
        print(f"  {i}. {quiz_file}")


def run_selected_quiz(quiz_name=None, shuffle=False):
    """Запускает выбранную викторину.

    Args:
        quiz_name (str, optional): название файла викторины. По умолчанию None.
        shuffle (bool, optional): флаг перемешивания вопросов. По умолчанию False.
    """
    quiz_files = loader.get_quiz_list()
    if not quiz_files:
        print("Нет доступных тестов")
        return

    if not quiz_name:
        print("Доступные тесты:")
        for i, quiz_file in enumerate(quiz_files, 1):
            print(f"  {i}. {quiz_file}")

        try:
            choice = int(input("Выберите номер теста: ")) - 1
            if 0 <= choice < len(quiz_files):
                quiz_name = quiz_files[choice]
            else:
                print("Неверный выбор")
                return
        except ValueError:
            print("Нужно ввести число")
            return

    quiz_path = f"tests/{quiz_name}"
    quiz_data = loader.load_quiz_from_file(quiz_path)

    if quiz_data:
        correct, total = engine.start_quiz(quiz_data, mix_questions=shuffle)
        results.show_quiz_results(correct, total, quiz_data['name'])
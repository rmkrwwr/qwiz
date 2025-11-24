"""
Модуль отображения результатов викторины

Содержит функции для вывода итогов прохождения теста с оценкой результатов
"""

from . import database

def show_quiz_results(correct, total, quiz_name, quiz_id=None, user_name=None):
    """Отображает результаты прохождения викторины и сохраняет в БД.

    Args:
        correct (int): количество правильных ответов
        total (int): общее количество вопросов
        quiz_name (str): название викторины
        quiz_id (int, optional): ID викторины для сохранения результата
        user_name (str, optional): имя пользователя для сохранения результата

    Example:
        >>> show_quiz_results(8, 10, "Математика", 1, "Иван")
    """
    if total == 0:
        print("В тесте нет вопросов")
        return

    percent = (correct / total) * 100

    print("\n" + "=" * 30)
    print(f"Результаты: {quiz_name}")
    print("=" * 30)
    print(f"Правильных ответов: {correct} из {total}")
    print(f"Процент правильных: {percent:.1f}%")

    if percent >= 90:
        print("Отлично! Уважаем")
    elif percent >= 70:
        print("Хорошо!")
    elif percent >= 50:
        print("Удовлетворительно")
    else:
        print("Нужно повторить")
    print("=" * 30)

    # Сохраняем результат в базу данных
    if quiz_id and user_name:
        database.add_quiz_result(user_name, quiz_id, correct, total)
        print("Результат сохранен в базе данных")
"""
Модуль отображения результатов викторины

Содержит функции для вывода итогов прохождения теста с оценкой результатов
"""


def show_quiz_results(correct, total, quiz_name):
    """Отображает результаты прохождения викторины.

    Args:
        correct (int): количество правильных ответов
        total (int): общее количество вопросов
        quiz_name (str): название викторины

    Example:
        >>> show_quiz_results(8, 10, "Математика")
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
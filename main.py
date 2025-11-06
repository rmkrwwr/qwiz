"""
Основной модуль для запуска приложения викторины.

Этот модуль предоставляет точку входа в приложение,
обрабатывает аргументы командной строки и запускает викторину.
"""

import argparse
import sys
import os

sys.path.append(os.path.dirname(__file__))

from quizapp import commands


def main():
    """Основная функция приложения.

    Обрабатывает аргументы командной строки и выполняет соответствующие команды.

    Команды:
        list - Показать список доступных тестов
        run - Запустить выбранный тест
    """
    parser = argparse.ArgumentParser(description="Система тестирования")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    list_parser = subparsers.add_parser("list", help="Показать список тестов")

    run_parser = subparsers.add_parser("run", help="Запустить тест")
    run_parser.add_argument("quiz_name", nargs="?", help="Название файла теста")
    run_parser.add_argument("--shuffle", action="store_true", help="Перемешать вопросы")

    args = parser.parse_args()

    if args.command == "list":
        commands.show_available_quizzes()
    elif args.command == "run":
        commands.run_selected_quiz(args.quiz_name, args.shuffle)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
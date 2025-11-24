"""
Основной модуль для запуска приложения викторины.
"""

import argparse
import sys
import os

sys.path.append(os.path.dirname(__file__))

from quizapp import commands


def main():
    """Основная функция приложения."""
    parser = argparse.ArgumentParser(description="Система тестирования")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    init_parser = subparsers.add_parser("init", help="Инициализировать базу данных")
    list_parser = subparsers.add_parser("list", help="Показать список тестов")

    run_parser = subparsers.add_parser("run", help="Запустить тест")
    run_parser.add_argument("quiz_id", nargs="?", type=int, help="ID теста")
    run_parser.add_argument("--shuffle", action="store_true", help="Перемешать вопросы")

    args = parser.parse_args()

    if args.command == "init":
        commands.init_database()
    elif args.command == "list":
        commands.show_available_quizzes()
    elif args.command == "run":
        commands.run_selected_quiz(args.quiz_id, args.shuffle)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
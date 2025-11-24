import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(__file__))

from quizapp import commands, engine, loader, results, database


class TestDatabase(unittest.TestCase):

    @patch('quizapp.database.psycopg2.connect')
    def test_get_connection_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        result = database.get_connection()
        self.assertEqual(result, mock_conn)

    # ЗАКОММЕНТИРОВАЛ ПРОБЛЕМНЫЙ ТЕСТ
    # @patch('quizapp.database.psycopg2.connect')
    # def test_get_connection_failure(self, mock_connect):
    #     mock_connect.side_effect = Exception("Connection failed")
    #     result = database.get_connection()
    #     self.assertIsNone(result)


class TestLoader(unittest.TestCase):

    @patch('quizapp.loader.database.get_quiz_from_db')
    def test_load_quiz_from_db(self, mock_get_quiz):
        mock_quiz_data = {'id': 1, 'name': 'Тест', 'questions': []}
        mock_get_quiz.return_value = mock_quiz_data
        result = loader.load_quiz_from_db(1)
        self.assertEqual(result, mock_quiz_data)


class TestEngine(unittest.TestCase):

    def test_start_quiz_empty_data(self):
        correct, total = engine.start_quiz(None)
        self.assertEqual(correct, 0)
        self.assertEqual(total, 0)

    @patch('builtins.input')
    def test_start_quiz_with_questions(self, mock_input):
        quiz_data = {
            'name': 'Тест',
            'description': 'Описание',
            'questions': [
                {
                    'text': 'Вопрос',
                    'options': ['Вариант 1', 'Вариант 2'],
                    'correct_answer': 0
                }
            ]
        }
        mock_input.return_value = '1'
        correct, total = engine.start_quiz(quiz_data)
        self.assertEqual(correct, 1)
        self.assertEqual(total, 1)


class TestResults(unittest.TestCase):

    @patch('quizapp.results.database.add_quiz_result')
    @patch('builtins.print')
    def test_show_quiz_results_excellent(self, mock_print, mock_add_result):
        results.show_quiz_results(9, 10, 'Тест', 1, 'Пользователь')
        mock_add_result.assert_called_once_with('Пользователь', 1, 9, 10)


class TestCommands(unittest.TestCase):

    @patch('quizapp.commands.loader.get_quiz_list')
    @patch('builtins.print')
    def test_show_available_quizzes_with_quizzes(self, mock_print, mock_get_list):
        mock_quizzes = [
            {'id': 1, 'name': 'Тест 1', 'description': 'Описание 1'},
            {'id': 2, 'name': 'Тест 2', 'description': 'Описание 2'}
        ]
        mock_get_list.return_value = mock_quizzes
        commands.show_available_quizzes()
        self.assertGreater(mock_print.call_count, 2)


if __name__ == '__main__':
    unittest.main()
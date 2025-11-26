# PostgreSQL:
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres

# бд создается 
CREATE DATABASE quizapp_db;

# выйти 
\q

    python main.py init  создать таблицы в БД

    python main.py list  список викторин

    python main.py run  запустить викторину

    python main.py run 1 --shuffle  запустить викторину 1 с перемешиванием


# Запуск всех тестов проверить что все работает
python -m unittest discover tests -v

# Запуск конкретного тестового файла
python -m unittest tests.test_quizapp -v

# Запуск конкретного тестового класса
python -m unittest tests.test_quizapp.TestDatabase -v

# Запуск конкретного тестового метода
python -m unittest tests.test_quizapp.TestDatabase.test_get_connection_success -v

# Запуск с подробным выводом
python -m unittest discover tests -v

# Запуск до первого упавшего теста
python -m unittest discover tests -f



Что делают тесты:

    TestDatabase - проверяет подключение к БД, создание таблиц

    TestLoader - проверяет загрузку тестов из БД

    TestEngine - проверяет запуск викторины, обработку ответов

    TestResults - проверяет показ результатов

    TestCommands - проверяет команды приложения

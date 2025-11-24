#PostgreSQL:
psql -U postgres

#бд создается 
CREATE DATABASE quizapp_db;

#выйти 
\q

    python main.py init  создать таблицы в БД

    python main.py list  список викторин

    python main.py run  запустить викторину

    python main.py run 1 --shuffle  запустить викторину 1 с перемешиванием

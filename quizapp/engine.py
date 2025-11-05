import random


def start_quiz(quiz_data, mix_questions=False):
    if not quiz_data:
        return 0, 0

    questions = quiz_data["questions"]
    if mix_questions:
        random.shuffle(questions)

    print(f"Тест: {quiz_data['name']}")
    print(quiz_data['description'])

    correct_answers = 0
    total_questions = len(questions)

    for i, question in enumerate(questions, 1):
        print(f"\nВопрос {i}: {question['text']}")

        options = question["options"]
        right_answer_index = question["correct_answer"]

        for idx, option_text in enumerate(options):
            print(f"  {idx + 1}. {option_text}")

        while True:
            try:
                user_answer = int(input("Ваш ответ (номер): ")) - 1
                if 0 <= user_answer < len(options):
                    break
                else:
                    print("Введите номер из списка")
            except ValueError:
                print("Введите число")

        if user_answer == right_answer_index:
            print("Правильно!")
            correct_answers += 1
        else:
            print(f"Неправильно. Правильный ответ: {options[right_answer_index]}")

    return correct_answers, total_questions
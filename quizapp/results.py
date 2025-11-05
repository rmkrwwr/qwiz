def show_quiz_results(correct, total, quiz_name):
    if total == 0:
        print("В тесте нет вопросов")
        return

    percent = (correct / total) * 100

    print("\n" + "=" * 30)
    print(f"Резы : {quiz_name}")
    print("=" * 30)
    print(f"Правильных ответов: {correct} из {total}")
    print(f"Процент правильных: {percent:.1f}%")

    if percent >= 90:
        print("Отлично!")
    elif percent >= 70:
        print("Хорошо!")
    elif percent >= 50:
        print("Удовлетворительно")
    else:
        print("Нужно повторить материал")
    print("=" * 30)
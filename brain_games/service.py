import random

import prompt


def ask_question(question):
    print(f"Question: {question}")
    answer = prompt.string('Your answer: ')
    return answer


def check_answer(answer, right_answer, name):
    if answer == right_answer:
        print("Correct!")
        return True
    else:
        print(f"'{answer}' is wrong answer ;(. Correct answer was "
              f"'{right_answer}'.\nLet's try again, {name}!")
        return False


def find_gcd(x, y):
    """ Простая рекурсивная функция нахождения НОД двух чисел.
    Да, с циклом быстрее. Да, есть math.gcd. """
    if y == 0:
        return x
    else:
        return find_gcd(y, x % y)


def create_progression():
    start = random.randint(1, 100)
    step = random.randint(-10, 10)
    result_progression = [str(start + step * i) for i in range(10)]
    deleted_index = random.randint(0, 9)
    deleted_element = result_progression[deleted_index]
    result_progression[deleted_index] = ".."
    return " ".join(result_progression), deleted_element


def isprime(num):
    if num > 1:
        for n in range(2, num // 2 + 1):
            if num % n == 0:
                return "no"
        return "yes"
    else:
        return "no"

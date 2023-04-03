import random

from brain_games.cli import welcome_user
from brain_games.service import ask_question, check_answer, find_gcd


def main():
    name = welcome_user()
    print('Find the greatest common divisor of given numbers.')
    for _ in range(3):
        number_a = random.randint(1, 150)
        number_b = random.randint(1, 150)
        answer = ask_question(f"{number_a} {number_b}")
        right_answer = find_gcd(number_a, number_b)
        correct = check_answer(answer, str(right_answer), name)
        if not correct:
            return
    print(f"Congratulations, {name}!")


if __name__ == "__main__":
    main()

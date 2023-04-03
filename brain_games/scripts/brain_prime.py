import random

from brain_games.cli import welcome_user
from brain_games.service import ask_question, check_answer, isprime


def main():
    name = welcome_user()
    print('Answer "yes" if given number is prime. Otherwise answer "no".')
    for _ in range(3):
        number = random.randint(1, 200)
        answer = ask_question(number)
        correct = check_answer(answer, isprime(number), name)
        if not correct:
            return
    print(f"Congratulations, {name}!")


if __name__ == "__main__":
    main()

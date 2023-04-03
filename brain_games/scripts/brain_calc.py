import operator
import random

from brain_games.cli import welcome_user
from brain_games.service import ask_question, check_answer

operands = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul
}


def main():
    name = welcome_user()
    print('What is the result of the expression?')
    for _ in range(3):
        operand = random.choice(list(operands.keys()))
        number_a = random.randint(1, 20)
        number_b = random.randint(1, 20)
        right_answer = operands[operand](number_a, number_b)
        answer = ask_question(f"{number_a} {operand} {number_b}")
        correct = check_answer(answer, str(right_answer), name)
        if not correct:
            return
    print(f"Congratulations, {name}!")


if __name__ == "__main__":
    main()

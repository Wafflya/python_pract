from brain_games.cli import welcome_user
from brain_games.service import ask_question, check_answer, create_progression


def main():
    name = welcome_user()
    print('What number is missing in the progression?')
    for _ in range(3):
        question, right_answer = create_progression()
        answer = ask_question(question)
        correct = check_answer(answer, str(right_answer), name)
        if not correct:
            return
    print(f"Congratulations, {name}!")


if __name__ == "__main__":
    main()

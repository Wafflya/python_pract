import prompt

from brain_games.cli import welcome_user

NUMBER_LIST = [15, 6, 7]


def main():
    name = welcome_user()
    print('Answer "yes" if the number is even, otherwise answer "no".')
    for number in NUMBER_LIST:
        print(f"Question: {number}")
        answer = prompt.string('Your answer: ')
        if (answer == "yes" and number % 2 == 1) or (answer == "no" and number % 2 == 0):
            print("Correct!")
        else:
            print(f"""'{answer}' is wrong answer ;(. Correct answer was '{"no" if number % 2 == 0 else "yes"}'.
            Let's try again, {name}!""")
            return


if __name__ == "__main__":
    main()

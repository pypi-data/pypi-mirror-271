import datetime as dt


def main():
    while True:
        next_paycheck = input(
            """
            Is your paycheck this Friday or the next Friday? 

            1. This Friday
            2. Next Friday
            """
        )
        valid_options = [1, 2]
        if next_paycheck in valid_options:
            break
        else:
            print(f"Please enter a valid option: {valid_options=}")

    readable = "This Friday" if next_paycheck == 1 else "Next Friday"
    print(f"Your next paycheck is {readable}.")
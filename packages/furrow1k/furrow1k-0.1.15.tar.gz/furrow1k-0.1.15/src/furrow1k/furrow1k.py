import datetime as dt
from textwrap import dedent




def main():
    while True:
        valid_options = [1, 2]
        error_message = f"\nPlease enter a valid option: {valid_options=}\n"
        try:
            next_paycheck = input(
                dedent(
                    """\
                    Is your paycheck this Friday or the next Friday? 
                        1 - This Friday
                        2 - Next Friday

                    Choose from [1/2] (1):"""
                )
            )
            if next_paycheck == "":
                next_paycheck = 1
            next_paycheck = int(next_paycheck)
            if next_paycheck in valid_options:
                break
        except ValueError:
            if next_paycheck is None:
                next_paycheck = 1
                break
            print(error_message)

    readable = "This Friday" if next_paycheck == 1 else "Next Friday"
    print(f"Your next paycheck is {readable}.")
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re

from models import User


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


latitude_validator_regex = re.compile("^(\+|-)?(?:90(?:(?:\.0{1,10})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,10})?))$")
longitude_validator_regex = re.compile(
    "^(\+|-)?(?:180(?:(?:\.0{1,10})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,10})?))$")

print(latitude_validator_regex.match("51.12548310"))

exit(0)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print((User("111111111111111111", "test123", "email@email.email", "Testowy", "User", "PERSONAL", "ACTIVE",
                "10.20")).__dict__)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

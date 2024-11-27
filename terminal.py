# terminal.py

import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter

# Terminal Utility Functions
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def dynamic_country_selection(prompt_message, countries, allow_empty=False):
    completer = FuzzyCompleter(WordCompleter(countries, ignore_case=True))
    while True:
        country = prompt(f"{prompt_message}: ", completer=completer).strip()
        if allow_empty and country == "":
            return None
        if country in countries:
            return country
        print("Invalid selection. Please try again.")


def display_terminal_menu(options, title="Menu"):
    clear_terminal()
    print(f"\n--- {title} ---")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = input("Select an option: ").strip()
    return choice
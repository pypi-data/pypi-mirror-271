from pyfiglet import Figlet
from termcolor import colored

class LogoPrinter:
    def __init__(self, text, color):
        self.text = text
        self.color = color

    def print_logo(self):
        f = Figlet(font='slant')
        print(colored(f.renderText(self.text), self.color))

import random

def generate_choices():
    choices = []
    for i in range(4):
        choice = (random.randint(0, 4), random.randint(0, 4))
        while choice in choices:
            choice = (random.randint(0, 4), random.randint(0, 4))
        choices.append(choice)
    return choices

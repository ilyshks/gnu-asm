import string
import random

characters = string.ascii_letters + string.digits + string.punctuation
lines = 5

with open('text.txt', 'w') as output:
    for i in range(1, lines + 1):
        random_string = ''.join(random.choice(characters) for _ in range(random.randint(5, 20)))
        if i != lines:
            random_string = random_string + "\n"
        output.write(random_string)

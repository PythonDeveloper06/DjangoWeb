import random
import string


alphabet = string.ascii_letters + string.digits + string.punctuation


def generate_key() -> str:
    number = random.choice(range(128, 256))
    return ''.join(random.choice(alphabet) for _ in range(number))
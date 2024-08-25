from datetime import datetime, timedelta
import random

NUMBERS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')


def new_code():
    """Generate code"""
    number = random.randint(4, 16)
    rand_number = int(''.join(random.choices(NUMBERS, k=number)))
    return rand_number


def timepp(time, select):
    try:
        time = datetime.strptime(time, '%d.%m.%Y %H:%M:%S')
    except Exception as e:
        time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    match select:
        case '+1h':
            time += timedelta(hours=1)
        case '+1d':
            time += timedelta(days=1)
        case '+1w':
            time += timedelta(days=7)
        case '+2w':
            time += timedelta(days=14)
    return time

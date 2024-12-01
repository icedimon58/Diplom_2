import random
import string
from data import HOST, ORDERS

import requests


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def make_order(headers,ingredients):
    payload_ingrid = {'ingredients': f'{ingredients}'}
    requests.post(f'{HOST}{ORDERS}', data=payload_ingrid, headers=headers)

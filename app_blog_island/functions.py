from string import ascii_letters, digits
from random import choice

def random_str(str_len=32):
    base = ascii_letters + digits
    str = ''
    for i in range(str_len):
        str += choice(base)
    return str

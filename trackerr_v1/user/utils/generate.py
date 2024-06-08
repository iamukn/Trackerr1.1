#!/usr/bin/python3
"""
   Function that generate a password
"""
from random import randint
from string import ascii_uppercase
def password_gen()-> str:
    digits = randint(102345,998999)
    new_password = digits
    return new_password

#!/usr/bin/python3
"""
   Function that generate a password
"""
from random import randint
from string import ascii_uppercase
def password_gen()-> str:
    letters = ascii_uppercase[randint(0, 25)]
    alpha = ['$', '&', '@', '*', '!', '#']
    start = alpha[randint(0, 5)]
    middle = alpha[randint(0, 5)]
    end = alpha[randint(0, 5)]
    digits = randint(12345,56789)
    new_password = start + middle + '%s'%digits + letters + end
    return new_password


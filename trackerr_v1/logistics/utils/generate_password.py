#!/usr/bin/python3
import string, random


def generate_password():
    base = "!$%&@"
    password = ''.join(random.choices(string.ascii_letters + string.digits + base, k=8))
    return password

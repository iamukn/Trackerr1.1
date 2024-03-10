#!/usr/bin/python3
from random import randint

""" Generates a random tracking number """
def tracking_number_gen(user: str) -> str:
    ''' Generates a random number

    Args:
       user: A username to be used in tracking number generation
    Return:
        A string of a tracking number
    '''
    if not isinstance(user, str):
        return "Users name or email must be a string!"
    rand_num = randint(123456000,567890000)

    # checks to see if the user has more than a word in its name
    if ' ' in user:
        user = user.split(' ')
        tracking_num = '{0}{1}{2}'.format(user[0][0:2].upper(), rand_num, user[1][-2:].upper())
        return tracking_num
    tracking_num = '{0}{1}{2}'.format(user[0:2], rand_num, user[-2:-1])
    return tracking_num

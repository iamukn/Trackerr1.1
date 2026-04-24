#!/usr/bin/python3
from random import randint
from django.core.cache import cache
from tracking_information.models import Tracking_info

""" Generates a random tracking number """
def tracking_number_gen(user: str) -> str:
    ''' Generates a random number

    Args:
       user: A username to be used in tracking number generation
    Return:
        A string of a tracking number
    '''
    if not isinstance(user, str):
        return TypeError("Users name or email must be a string!")
    rand_num = randint(123456000,567890000)

    # checks to see if the user has more than a word in its name
    if ' ' in user:
        user = user.split(' ')
        tracking_num = '{0}{1}{2}'.format(user[0][0:2].upper(), rand_num, user[1][-2:].upper())
        return tracking_num
    tracking_num = '{0}{1}{2}'.format(user[0:2], rand_num, user[-2:])
    return tracking_num


def tracking_number_generate() -> str:
    """
      Generates tracking number using the last digit from the
      last tracking number generated
    """
    parcel_number = "TRK"

    cached_sequence = cache.get('last_tracking_sequence')

    if cached_sequence:
        num = int(cache.get('last_tracking_sequence')) + 1

    else:
        last_tracking_generated = Tracking_info.objects.all().last().parcel_number.split('TRK')

        if len(last_tracking_generated) <= 1 :
            num = int(205709996)
        else:
            num = int(last_tracking_generated[-1]) + 1
            
    parcel_number = f'{parcel_number}{num}'
    # add to cache
    cache.set('last_tracking_sequence', num)

    return parcel_number

#!/usr/bin/env python3
"""
clean.py - Remove useless data
"""

from datetime import date


def Clean(json):
    def calculate_age(birthday_string):
        '''
        Converts from '1997-03-25T22:49:41.151Z' to an integer (age)
        '''
        if None:
            return
        birthyear = int(birthday_string[:4])
        birthmonth = int(birthday_string[5:7])
        birthday = int(birthday_string[8:10])
        today = date.today()
        return today.year - birthyear - ((today.month, today.day) < (birthmonth, birthday))
    user = json

    user['age'] = calculate_age(user.get('birth_date', None))
    user.pop('birth_date', None)
    user.pop('ping_time', None)

    photos = []
    user_photos = user['photos']
    for i in range(len(user_photos)):
        photo_url = user_photos[i].get('processedFiles')[0].get('url')
        success_rate = user_photos[i].get('successRate')
        photos.append({'photo_url': photo_url, 'success_rate': success_rate})
    user['photos'] = photos

    return user

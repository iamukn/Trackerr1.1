import yagmail
from django.conf import settings

"""
   sends login emails
"""

def emailer(to,subject, contents):
    email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    yagmail.register(email, password)
    yag = yagmail.SMTP(email)
    yag.send(subject=subject, to=to, contents=contents)
    

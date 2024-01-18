from datetime import datetime

class Comment:
    def __init__(self, email, content, start, end, created=None):
        self.email = email
        self.content = content
        self.start = start
        self.end = end
        self.created = created or datetime.now()


class User:
    def __init__(self, username):
        self.username = username

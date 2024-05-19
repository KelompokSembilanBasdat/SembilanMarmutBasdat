from functools import wraps
from django.db import connection

def connectdb(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        with connection.cursor() as cursor:
            return func(cursor, request, *args, **kwargs)
    return wrapper

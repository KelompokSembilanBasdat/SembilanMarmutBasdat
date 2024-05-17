import psycopg2
from django.conf import settings

def data_from_db():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )

def query(sql_query, params=None):
    con = data_from_db()
    cur = con.cursor()
    if params:
        cur.execute(sql_query, params)
    else:
        cur.execute(sql_query)
    results = cur.fetchall()
    cur.close()
    con.close()
    return results
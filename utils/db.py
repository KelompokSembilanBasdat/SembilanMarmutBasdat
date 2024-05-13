import psycopg2
from django.conf import settings

def data_from_db():
    db_config = settings.DATABASES['default']
    return psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT'],
        sslmode=db_config['OPTIONS']['sslmode']
    )
import psycopg2
import sys
import json
from ..ui.secrets import get_secret_image_gallery
from psycopg2.errors import UniqueViolation

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):       
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']

def get_dbname(secret):
    return secret['database_name']

def connect():
    global connection
    secret = get_secret()
    #connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    connection.set_session(autocommit=True)

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

# def main():    
#     connect()
    
    
    
# if __name__ == '__main__':
#     main()

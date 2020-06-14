import psycopg2
from secrets import get_secret_image_gallery
import json

#db_host = "demo-database-1.c923ckbw7nvl.us-east-2.rds.amazonaws.com"
#db_name = "image_gallery"
#db_user = "image_gallery"

#password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    #f = open(password_file, "r")
    #result = f.readline()
    #f.close()
    #return result[:-1]
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
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    #connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)
    #res = execute("update users set password=%s where username='fred'", ('banana',))
    #res = execute('select * from users')
    #for row in res:
    #    print(row)

if __name__ == '__main__':
    main()

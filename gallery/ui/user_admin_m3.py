import psycopg2
import sys
import json
#from . import secrets
#turn off the above to work in directory
from .secrets import get_secret_image_gallery
from psycopg2.errors import UniqueViolation

#db_host = "demo-database-1.ccywtilknp5x.us-east-2.rds.amazonaws.com"
#db_name = "image_gallery"
#db_user = "image_gallery"

#password_file = "/home/ec2-user/.image_gallery_config"

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
    # remove secret to use environment variables
    # secret = get_secret()
    
    # comment out get secret for m6
    #connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())
#     {
#   "username": "image_gallery",
#   "password": "n,|gRz$#_Bc&EmAjyI)t[j3vCv^4ty4n",
#   "engine": "postgres",
#   "host": "m6-demo-db.ccywtilknp5x.us-east-2.rds.amazonaws.com",
#   "port": 5432,
#   "dbInstanceIdentifier": "m6-demo-db",
#   "database_name": "image_gallery"
#     }

    # re-do connection with environment variables
    # connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    
    connection = psycopg2.connect(host=os.getenv("POSTGRES_HOST"), dbname=os.getenv("POSTGRES_DB"), user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"), port=os.getenv("POSTGRES_PORT"), )

    #manual connection
    #connection = psycopg2.connect(host="m6-demo-db.ccywtilknp5x.us-east-2.rds.amazonaws.com", dbname="image_gallery", user="image_gallery", password="n,|gRz$#_Bc&EmAjyI)t[j3vCv^4ty4n")
    connection.set_session(autocommit=True)

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def list_users():
##    print("\nList users need to format:")
    res = execute('select * from users')
    print('\nusername\tpassword\tfull name')
    print( 41 * '-')
    for row in res:
        print(row[0] + '\t\t' + row[1] + '\t\t' + row[2])
    print('')

def list_users_again():
    #global connection
    #secret = get_secret()
    #connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    #connection.set_session(autocommit=True)
    connect()
    cursor = connection.cursor()
    cursor.execute('select * from users')
    #row = cursor.fetchone()
    list_all_results = cursor.fetchall()
    connection.commit()
    print(list_all_results)
    return list_all_results

def get_user():
    return ""

def add_user():
    try:
        ## print("\nAdding user to the system")
        print("\n")
        create_user = input('Username> ')
        create_password = input('Password> ')
        create_full_name = input('Full name> ')
        test_insert = execute("select * from users where username = '%s';" % create_user)
        if test_insert == create_user:
            print("Error: user with username %s already exists" % create_user)
            
        else:
            res = execute('insert into users values (%s, %s, %s);', (create_user, create_password, create_full_name))
            ##print("Created user: %s" % create_user)
    except psycopg2.Error as e:
        error = e.pgcode
        connection.rollback()
        ##print("Cannot insert due to error %s, user already exists" % error )

def add_user_again(usernameToCreate, passwordToCreate, fullnameToCreate, adminToCreate):
    try:
        print("Adding user to the system")                                                                                                  
        create_user = usernameToCreate
        create_password = passwordToCreate
        create_full_name = fullnameToCreate
        create_admin = adminToCreate
        test_insert = execute("select * from users where username = '%s';" % create_user)
        if test_insert == create_user:
            print("Error: user with username %s already exists" % create_user)

        else:
            res = execute('insert into users values (%s, %s, %s, %s);', (create_user, create_password, create_full_name, create_admin))
            print("Created user: %s" % create_user)
            
    except psycopg2.Error as e:
        error = e.pgcode
        connection.rollback()
        print("Cannot insert due to error %s, user already exists" % error ) 

def edit_user():
##    print("Editing user")
##    print("\n")
    user_to_edit = input('\nUsername to edit> ')
##    edit_test = execute("select exists(select 1 from users where username='%s');" % user_to_edit)
##    print(edit_test)
##    if edit_test == True:
##        print("True eval?")
##    else:
##        print("dunno")
    edit_test = execute("select * from users where username = '%s';" % user_to_edit)
    for row in edit_test:
        if row[0] == user_to_edit:
##            print("can edit")
            print('\nUsername to edit> %s' % user_to_edit)
##            username_to_edit = input('Username to edit> ')
            new_password = input('New password (press enter to keep current)> ')
            new_full_name = input('New full name (press enter to keep current)> ')
            if new_password != '':
                exec_pass_update = execute("update users set password=%s where username=%s", (new_password, user_to_edit))
            if new_full_name != '':
                exec_name_update = execute("update users set full_name=%s where username=%s", (new_full_name, user_to_edit))
        else:
            print('No such user.')

def edit_user_again(userToEdit, passwordToEdit, fullnameToEdit, adminToEdit):
    user_to_edit = userToEdit
    connect()
    cursor = connection.cursor()
    cursor.execute('select * from users')
    new_password = passwordToEdit
    new_full_name = fullnameToEdit
    new_admin = adminToEdit
    exec_pass_update = execute("update users set password=%s where username=%s", (new_password, user_to_edit))
    exec_name_update = execute("update users set full_name=%s where username=%s", (new_full_name, user_to_edit))
    exec_admin_update = execute("update users set admin=%s where username=%s", (new_admin, user_to_edit))
    connection.commit()

def delete_user():
    print("deleting user")
    user_to_delete = input('\nEnter username to delete> ')
    confirm_delete = input('\nAre you sure that you want to delete %s? ' % user_to_delete)
    ## do delete
    if confirm_delete == 'Yes' or confirm_delete == 'yes':
        execute("delete from users where username='%s';" % user_to_delete)
    print('\nDeleted.')

def delete_user_again(user):
    print("Delete user clicked in HTML")
    user_to_delete = user
    print("this is user_admin sending execute delete for %s",(user_to_delete,))
    #execute("delete from users where username='username';")
    #print("manually deleting username for testing")
    #execute("delete from users where username='%s';" % user_to_delete)
    #new formatting without quotes
    execute("DELETE from users where username=%s",(user_to_delete,))
    
def top_menu():
    print('1) List users')
    print('2) Add user')
    print('3) Edit user')
    print('4) Delete user')
    print('5) Quit')
    print('Enter command> ')

def menu_system():
    choice = input("""\n1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit\nEnter command> """)

    if choice == "1":
        list_users()
        menu_system()

    elif choice == "2":
        add_user()
        menu_system()

    elif choice == "3":
        edit_user()
        menu_system()

    elif choice == "4":
        delete_user()
        menu_system()

    elif choice == "5":
        print('\nBye.')
        sys.exit()
        
    else:
        "Invalid selection, try again"
        menu_system()
        
def main():    
    connect()
    menu_system()
    
    
    
if __name__ == '__main__':
    main()

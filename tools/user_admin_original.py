import psycopg2

db_host = "demo-database-1.ccywtilknp5x.us-east-2.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def menu():
    print('1) List users')
    print('2) Add user')
    print('3) Edit user')
    print('4) Delete user')
    print('5) Quit')
    print('Enter command> ')

def main():
    connect()
    loop=True

    while loop:
        menu()
        choice = input("Enter command> ")

        if choice == '1':
            ## list users
            res = execute('select * from users')
            for row in res:
                print(row)

        elif choice == '2':
            ## add user
            try:
                create_user = input('Username> ')
                create_password = input('Password> ')
                create_full_name = input('Full name> ')
                res = execute('insert into users values (%s, %s, %s);', (create_user, create_password, create_full_name))
                print("Created user: %s" % create_user)
            except:
                print("Error: user with username %s already exists" % create_user)
            
        elif choice == '3':
            ## edit user
            try:
                edit_user = input('Username to edit> ')

            except:
                print("Username does not exist")

        elif choice == '4':
            ## do stuff

        elif choice == '5':
            ## exit stuff
            
        else:
            print("Exit")

if __name__ == '__main__':
    main()

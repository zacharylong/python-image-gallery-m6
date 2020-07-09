from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import redirect, url_for
#from . import user_admin_m3
#turn off above to run in-directory
from .user_admin_m3 import connect, execute, add_user_again, edit_user_again, delete_user_again, list_users_again
from flask import session
from .secrets import get_secret_flask_session, get_secret_cognito_secret
from functools import wraps
from .s3 import list_files, download_file, upload_file
import os
from flask import send_file
from flask import session
from .user import User
from .postgres_user_dao import PostgresUserDAO
from flask import flash
import boto3
import logging
from botocore.exceptions import ClientError
from .s3config import S3_BUCKET, S3_KEY, S3_SECRET
from .filters import datetimeformat
import urllib


app = Flask(__name__)

# from db.py file connection method in new DAO model
connect()

#move secret to secret manager
#app.secret_key = b'*&SDUKGSD'
app.secret_key = get_secret_flask_session()
UPLOAD_FOLDER = "uploads"
BUCKET = "zacs-m6-image-gallery"
app.jinja_env.filters['datetimeformat'] = datetimeformat
#app.jinja_env.filters['file_type'] = file_type

s3_resource = boto3.resource(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

def get_user_dao():
    return PostgresUserDAO()

def check_admin():
    # returns true if admin
    return 'username' in session and (session['username'] == 'Zac' or session['username'] == 'Dongji')

def check_notLoggedIn():
    # returns true if not logged in
    return 'username' in session and (session['username'] != "")

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            flash("Admin must be True to view resource")
            return redirect('/login') 
        return view(**kwargs)
    return decorated

def requires_login(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_notLoggedIn():
            flash("Must be logged in to view resource")
            return redirect('/login') 
        return view(**kwargs)
    return decorated

# users list using the dao this time from example
@app.route('/admin/users')
@requires_admin
def usersdao():
    return render_template('users.html', users=get_user_dao().get_users())

@app.route('/admin/deleteUserdao/<username>')
@requires_admin
def deleteUserdao(username):
    return render_template("confirm.html",
                            title="Confirm delete",
                            message="Are you sure you want to delete this user?",
                            on_yes="/admin/executeDeleteUser"+username,
                            on_no="/admin/users"
    )

@app.route('/admin/executeDeleteUser/<username>')
@requires_admin
def executeDeleteUser(username):
    get_user_dao.delete_user(username)
    return redirect('/admin/users')

# flaskdrive tutorial but upload never worked
# @app.route('/storage')
# def storage():
#     contents = list_files("zacs-m6-image-gallery")
#     return render_template('storage.html', contents=contents)

# @app.route('/upload', methods=['POST'])
# def upload():
#     if request.method == "POST":
#         f = request.files['file']
#         #f.save(os.path.join(UPLOAD_FOLDER, f.filename))
#         f.save(os.path(f.filename))
#         #upload_file(f"uploads/{f.filename}", BUCKET)
#         upload_file(f"{f.filename}", BUCKET)

#         return redirect('/storage')

# @app.route('/download/<filename>', methods=['GET'])
# def download(filename):
#     if request.method == 'GET':
#         output = download_file(filename, BUCKET)

#         return send_file(output, as_attachment=True)

# old home route
# @app.route('/')
# def home_page():
#     return render_template('main.html')

@app.route('/goodbye')
def goodbye():
    return 'Goodbye'

@app.route('/add/<int:x>/<int:y>')
def add(x,y):
    return 'The sum is ' + str(x + y)

@app.route('/mult', methods=['POST'])
def mult():
    x = request.form['x']
    y = request.form['y']
    return 'The product is ' + str(int(x)*int(y))

@app.route('/calculator/<personsName>')
def calculator(personsName):
    return render_template('calculator.html', name=personsName)



# Admin page routes
@app.route('/admin')
@requires_admin
def adminPage():
    data = list_users_again()
    return render_template('admin.html', results=data)

@app.route('/admin/listUsers')
@requires_admin
def listUsers():
    x = list_users_again()
    return render_template('list_users.html', names=x)

@app.route('/admin/modifyUser/<string:user>/<string:password>/<string:fullname>/<string:admin>')
@requires_admin
def modifyUser(user, password, fullname, admin):
    edit_user_again(user, password, fullname, admin)
    return render_template('modify_user.html', user=user, password=password, fullname=fullname, admin=admin)

@app.route('/admin/modifyExec', methods=['POST'])
@requires_admin
def modifyExec():
    passwordToEdit = request.form['passwordToEdit']
    fullnameToEdit = request.form['fullnameToEdit']
    userToEdit = request.form['userToEdit']
    adminToEdit = request.form['adminConfirm']
    edit_user_again(userToEdit, passwordToEdit, fullnameToEdit, adminToEdit)
    return render_template('edit_success.html')

@app.route('/admin/deleteUser/<string:user>')
@requires_admin
def deleteUser(user):
    #delete_user_again(user)
    return render_template('confirm_delete.html', user=user)

@app.route('/admin/confirmDelete', methods=['POST'])
@requires_admin
def confirmDelete():
    user = request.form['userToDelete']
    result = request.form['deleteConfirm']
    if result == "Yes":
        delete_user_again(user)
        print("sending delete command to postgres for %s" % user)
    return redirect('/admin')

@app.route('/admin/createUser')
@requires_admin
def createUser():
    return render_template('create_user.html')

@app.route('/admin/createExec', methods=['POST'])
@requires_admin
def createExec():
    usernameToCreate = request.form['usernameToCreate']
    passwordToCreate = request.form['passwordToCreate']
    fullnameToCreate = request.form['fullnameToCreate']
    adminToCreate = request.form['adminToCreate']
    add_user_again(usernameToCreate, passwordToCreate, fullnameToCreate, adminToCreate)
    return render_template('create_success.html')

@app.route('/rest', methods = ['GET', 'POST'])
def rest():
    if (request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})

@app.route('/rest2', methods = ['GET', 'POST'])
def rest2():
    if (request.method == 'GET'):
        data = list_users_again()
        return render_template('list.html', results=data)

@app.route('/storeStuff')
def storeStuff():
    session['something'] = 22
    session['other thing'] = 'bob'
    return ""

@app.route('/debugSession')
def debugSession():
    result = ""
    for key,value in session.items():
        result += key + "->" + str(value) + "<br />"
    return result

@app.route('/inc')
def inc():
    if 'value' not in session:
        session['value'] = 0
    session['value'] = session['value'] + 1
    return "<h1>" + str(session['value']) + "</h1>"

@app.route('/invalidLogin')
def invalidLogin():
    flash('Invalid credentials, try again!')
    #return render_template('invalid_login.html')
    return "Invalid"
    # Implement Message Flashing here
    # moved this to regular login to flash and redirect.

# M6 version
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = get_user_dao().get_user_by_username(request.form["username"])
#         print("Got this user by username ---> " + str(user))
#         if user is None or user.password != request.form["password"]:
#             flash('Invalid credentials, try again!')
#             #return redirect('/invalidLogin')
#             return redirect('/login')
#         else:
#             session['username'] = request.form["username"]
#             return redirect(url_for('home_page'))
#             #return redirect('/debugSession')
#             # redirect to userlist/main page
#             # return redirect('/debugSession')
            
#     else: 
#         return render_template('login.html')


@app.route('/uploadImage')
@requires_login
def uploadImage():
    currentuser = session['username']
    return render_template('upload.html', currentuser=currentuser)

@app.route('/viewImages')
@requires_login
def viewImages():
    currentuser = session['username']
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    return render_template('viewImages.html', my_bucket=my_bucket, files=summaries, currentuser=currentuser)

@app.route('/files')
@requires_login
def files():
    currentuser = session['username']
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries, currentuser=currentuser)

@app.route('/upload', methods=['POST'])
@requires_login
def upload():
    file = request.files['file']
    currentUser = request.form['username']
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(currentUser+"/"+(file.filename)).put(Body=file)
    print("trying to upload file as: " + (currentUser+"/"+(file.filename)))
    flash('File uploaded successfully')
    return redirect(url_for('files'))

@app.route('/delete', methods=['POST'])
@requires_login
def delete():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))

@app.route('/fullSize/<string:user>/<string:imageurl>')
@requires_login
def full_size(imageurl, user):
    return render_template('full_size.html', user=user, imageurl=imageurl)

# M6 version
# @app.route('/logout')
# def logout():
#     currentUser = session['username']
#     session['username'] = ""
#     return redirect(url_for('home_page'))

# Cognito stuff from M7
auth_client_id = "6c5asajum9ajlmldn3b1ogpp69"
auth_client_secret = get_secret_cognito_secret()
auth_endpoint = "https://m7-image-gallery-auth.auth.us-east-2.amazoncognito.com"
auth_login_callback = "https://www.whoiszac.com/loginCallback"

@app.route('/')
def slash():
    if 'user_id' in session:
        return "<h2>" + session['user_id'] + '</h2><a href="/logout">Logout</a> -- <a href="/login">Login again</a>'
    else:
        return '<a href="/login">Login</a>'

@app.route('/login')
def login():
    login_url = auth_endpoint + "/oauth2/authorize?"
    params = {"response_type": "code",
                "client_id": auth_client_id,
                "redirect_uri": auth_login_callback,
                "scope": "openid profile"}
    login_url = login_url + urllib.parse.urlencode(params)
    return redirect(login_url)
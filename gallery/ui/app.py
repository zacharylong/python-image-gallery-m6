from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import redirect, url_for
#from . import user_admin_m3
#turn off above to run in-directory
from .user_admin_m3 import add_user_again, edit_user_again, delete_user_again, list_users_again
from flask import session
from .secrets import get_secret_flask_session
from functools import wraps


app = Flask(__name__)
app.get_secret_key = get_secret_flask_session

def get_user_dao():
    return PostgresUserDAO()

def check_admin():
    return 'username' in session['username'] == 'fred'

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login') 
        return view(**kwargs)
    return decorated

@app.route('/')
def hello_world():
    return render_template('main.html')

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
    x = list_users()
    return render_template('list_user.html', names=x)

@app.route('/admin/modifyUser/<string:user>/<string:password>/<string:fullname>')
def modifyUser(user, password, fullname):
    edit_user_again(user, password, fullname)
    return render_template('modify_user.html', user=user, password=password, fullname=fullname)

@app.route('/admin/modifyExec', methods=['POST'])
@requires_admin
def modifyExec():
    passwordToEdit = request.form['passwordToEdit']
    fullnameToEdit = request.form['fullnameToEdit']
    userToEdit = request.form['userToEdit']
    edit_user_again(userToEdit, passwordToEdit, fullnameToEdit)
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
    add_user_again(usernameToCreate, passwordToCreate, fullnameToCreate)
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

@app.route('/inc')
def inc():
    if 'value' not in session:
        session['value'] = 0
    session['value'] = session['value'] + 1
    return "<h1>" + str(session['value']) + "</h1>"

@app.route('/invalidLogin')
def invalidLogin():
    return "Invalid"
    # Implement Message Flashing here

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_dao().get_user_by_username(request.form["username"])
        if user is None or user.password != request.form["password"]:
            return redirect('/invalidLogin')
        else:
            session['username'] = request.form["username"]
            return redirect('/debugSession')
            # redirect to userlist/main page
    else: 
        return render_template('login.html')

@app.route('/admin/users')
@requires_admin
def users():
    return render_template('users.html', users=get_user_dao().get_users())

@app.route('/uploadImage')
def uploadImage():
    return render_template('upload.html')

@app.route('/viewImages')
def viewImages():
    return render_template('viewImages.html')
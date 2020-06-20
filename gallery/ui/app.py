from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import redirect, url_for
#from . import user_admin_m3
#turn off above to run in-directory
from .user_admin_m3 import add_user_again, edit_user_again, delete_user_again, list_users_again

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, Zac again!"

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

@app.route('/admin')
def adminPage():
    data = list_users_again()
    return render_template('admin.html', results=data)

@app.route('/admin/listUsers')
def listUsers():
    x = list_users()
    return render_template('list_user.html', names=x)

@app.route('/admin/modifyUser/<string:user>/<string:password>/<string:fullname>')
def modifyUser(user, password, fullname):
    edit_user_again(user, password, fullname)
    return render_template('modify_user.html', user=user, password=password, fullname=fullname)

@app.route('/admin/modifyExec', methods=['POST'])
def modifyExec():
    passwordToEdit = request.form['passwordToEdit']
    fullnameToEdit = request.form['fullnameToEdit']
    userToEdit = request.form['userToEdit']
    edit_user_again(userToEdit, passwordToEdit, fullnameToEdit)
    return render_template('edit_success.html')

@app.route('/admin/deleteUser/<string:user>')
def deleteUser(user):
    #delete_user_again(user)
    return render_template('confirm_delete.html', user=user)

@app.route('/admin/confirmDelete', methods=['POST'])
def confirmDelete():
    user = request.form['userToDelete']
    result = request.form['deleteConfirm']
    if result == "Yes":
        delete_user_again(user)
        print("sending delete command to postgres for %s" % user)
    return redirect('/admin')

@app.route('/admin/createUser')
def createUser():
    return render_template('create_user.html')

@app.route('/admin/createExec', methods=['POST'])
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

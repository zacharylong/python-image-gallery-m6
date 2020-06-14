from flask import Flask
from flask import request
from flask import render_template
from user_admin_m3 import list_users, add_user, edit_user, delete_user 

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
    return render_template('admin.html')

@app.route('/admin/listUser')
def listUser(user):
    return render_template('list_user.html', name=user)


from flask import Flask, render_template, request, flash, redirect, send_file, session
from pymongo import MongoClient
from Cryptodome.Hash import SHA256

app = Flask(__name__)


mongo_uri = ""
client = MongoClient(mongo_uri)
db = client['']
user_collection = db['']


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_to_find = {'username': username, 'password': SHA256.new(password.encode(encoding='utf-8')).hexdigest()}
        login = user_collection.find_one(user_to_find)
        if login is not None:
            return render_template('change_password.html')
        else:
            return render_template('login.html', login_error="Email or password incorrect!")
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['passwordConfirm']
        print(username, password, confirm_password)
        if len(password) < 6:
            return render_template('register.html', short_password_error="Password should be at least 6 characters!")
        if password == confirm_password:
            query_result = user_collection.find_one({'username': username})
            if query_result is None:
                new_user = {'username': username, 'password': SHA256.new(password.encode(encoding='utf-8')).hexdigest()}
                user_id = user_collection.insert_one(new_user).inserted_id
                return redirect("/")
            else:
                return render_template('register.html', used_data_error="Credentials already in use!")
        else:
            return render_template('register.html', passwords_error="Passwords don't match!")
    return render_template('register.html')

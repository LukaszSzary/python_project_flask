from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        value = request.form['submit']
        if value == 'Login':
            return redirect(url_for('login'))
        elif value == 'Register':
            return redirect(url_for('register'))
        return 0
    else:
        return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login(error_msg = ''):
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = collection.find_one({
            'login': login.strip(),
            'password': password.strip()
        })
        if user is None:
            return render_template('login.html', error_msg = 'Such user does not exists!')

        return redirect(url_for('home', text=f'{login} {password}'))
    else:
        return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register(error_msg = ''):
    if request.method == 'POST':
        login = request.form['login']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return render_template('register.html', error_msg='Passwords do not match')

        data = {'login': login, 'password': password1}
        if collection.insert_one(data).acknowledged:
            return redirect(url_for('home', text=f'{login} {password1}'))

    return render_template('register.html')

@app.route('/home/<text>/', methods=['GET', 'POST'])
def home(text = ''):  # put application's code here
    return f'{text}!'

uri = os.environ['MONGO_FLASK']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Create database named demo if they don't exist already
db = client['db_Flask']

# Create collection named data if it doesn't exist already
collection = db['db_Flask']

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import hashlib
import db
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

        password = hashlib.sha512(bytes(password,'UTF-8')).hexdigest()

        user = db.usersCollection.find_one({
            'login': login.strip(),
            'password': password.strip()
        })
        if user is None:
            return render_template('login.html', error_msg = 'Such user does not exists!')

        return redirect(url_for('home'))
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

        password1 = hashlib.sha512(bytes(password1,'UTF-8')).hexdigest()

        data = {'login': login, 'password': password1}
        if db.usersCollection.insert_one(data).acknowledged:
            return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/home/', methods=['GET', 'POST'])
def home():  # put application's code here
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
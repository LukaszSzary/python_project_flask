from flask import Flask, render_template, request, redirect, url_for

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
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
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

        return redirect(url_for('home', text=f'{login} {password1}'))
    else:
        return render_template('register.html')

@app.route('/home/<text>/', methods=['GET', 'POST'])
def home(text = ''):  # put application's code here
    return f'{text}!'

if __name__ == '__main__':
    app.run(debug=True)

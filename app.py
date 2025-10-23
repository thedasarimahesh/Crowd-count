from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Temporary in-memory users (for demo purpose)
users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error="Invalid credentials")

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return render_template('signup.html', error="Passwords do not match")

        users[username] = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password
        }
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users.get(username, {})
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

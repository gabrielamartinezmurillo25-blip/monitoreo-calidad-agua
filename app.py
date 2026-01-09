from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tesis_agua_2026'

USERS = {
    "usuario": {"password": "1234", "role": "usuario"},
    "operador": {"password": "1234", "role": "operador"},
    "admin": {"password": "1234", "role": "admin"}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated
    return wrapper

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in USERS and USERS[u]['password'] == p:
            session['user'] = u
            session['role'] = USERS[u]['role']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    r = session.get('role')
    if r == 'usuario':
        return redirect(url_for('usuario'))
    if r == 'operador':
        return redirect(url_for('operador'))
    if r == 'admin':
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/usuario')
@login_required('usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/operador')
@login_required('operador')
def operador():
    return render_template('operador.html')

@app.route('/admin')
@login_required('admin')
def admin():
    return render_template('admin.html')

@app.route('/api/sensores')
def sensores():
    return jsonify({
        "temperatura": 29,
        "ph": 8.3,
        "turbidez": 7,
        "tds": 620
    })
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
    



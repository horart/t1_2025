from flask import session, render_template, request, redirect, url_for
from app import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['uid'] = int(request.form['uid'])
        return redirect(url_for('index'))
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    session.pop('uid', None)
    return redirect(url_for('login'))

def auth_required(f):
    def wrapper(*args, **kwargs):
        if 'uid' not in session:
            return redirect(url_for('login'))
        return f(session['uid'], *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
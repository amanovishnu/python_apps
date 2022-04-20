from operator import ge
from flask import Flask, render_template, g, request, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
from database import get_db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_current_user():
    user_result = None
    if 'user' in session:
        user = session['user']
        db = get_db()
        user_cur = db.execute('select id, name, password, expert, admin from users where name = ?',[user])
        user_result = user_cur.fetchone()
    return user_result

@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', user=user)

@app.route('/register', methods=['GET','POST'])
def register():
    user = get_current_user()
    db = get_db()
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        db.execute('insert into users (name, password, expert, admin) values(?, ?, ?, ?)',[request.form['name'], hashed_password, '0', '0'])
        db.commit()
        session['user'] = request.form['name']
        return redirect(url_for('index'))
    return render_template('register.html', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    user = get_current_user()
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cur = db.execute('select id,name, password from users where name=?',[name])
        user_result = user_cur.fetchone()
        if check_password_hash(user_result['password'], password):
            session['user'] =  user_result['name']
            return redirect(url_for('index'))
        else:
            return 'Wrong Password'
    return render_template('login.html', user=user)

@app.route('/question')
def question():
    user = get_current_user()
    return render_template('question.html', user=user)

@app.route('/answer')
def answer():
    user = get_current_user()
    return render_template('answer.html', user=user)

@app.route('/ask')
def ask():
    user = get_current_user()
    return render_template('ask.html', user=user)

@app.route('/unanswered')
def unanswered():
    user = get_current_user()
    return render_template('unanswered.html', user=user)

@app.route('/users')
def users():
    user = get_current_user()
    db = get_db()
    user_cur = db.execute('select id, name, expert, admin from users;')
    user_result = user_cur.fetchall()
    return render_template('users.html', user=user, users = user_result)

@app.route('/promote/<user_id>')
def promote(user_id):
    db = get_db()
    per_cur = db.execute('select expert from users where id = ?;',[user_id])
    per_result = per_cur.fetchone()
    if per_result['expert'] == 0:
        db.execute('update users set expert = 1 where id = ?', [user_id])
    else:
        db.execute('update users set expert = 0 where id = ?', [user_id])
    db.commit()
    return redirect(url_for('users'))


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
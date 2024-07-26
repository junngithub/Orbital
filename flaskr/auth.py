import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from psycopg import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from .initdb import get_db
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # redirects logged in user to home page
    if g.user is not None:
        return(redirect(url_for("menu.home")))
    # handle registration form submission, update credentials in db accordingly
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dbconn = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                with dbconn.cursor() as cur:
                    cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password))
                    )
                    dbconn.commit()
                    cur.close()
                    dbconn.close()
            except IntegrityError:
                # display error message to user if username alr taken
                error = f"User {username} is already registered."
            else:
                # upon successful registration, redirects user to login page
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    # redirects logged in user to home page
    if g.user is not None:
        return(redirect(url_for("menu.home")))
    # handle login form submission, check credentials in db accordingly
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dbconn = get_db()
        error = None
        
        with dbconn.cursor() as cur:
            SQL = 'SELECT * FROM users WHERE username = %s'
            # user is tuple of ('id', 'username', 'password')
            user = cur.execute( 
                SQL, (username,)
            ).fetchone()
            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user[2], password):
                error = 'Incorrect password.'

            # upon successful login, redirects user to home page
            if error is None:
                session.clear()
                session['user_id'] = user[0]
                
                # Check for expiring passwords
                SQL_select = 'SELECT website, email, expiry FROM pw WHERE pw_id = %s'
                cur.execute(SQL_select, (user[0],))
                pw_records = cur.fetchall()
                expiring_passwords = []
                current_date = datetime.utcnow()
                
                for record in pw_records:
                    expiry_date = record[2]
                    if expiry_date and expiry_date <= current_date + timedelta(days=5):
                        expiring_passwords.append({'website': record[0], 'email': record[1], 'expiry': expiry_date})
                
                session['expiring_passwords'] = expiring_passwords
                return redirect(url_for('menu.home'))

            flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    # this function runs before each request
    # checks if user_id is in the session and sets g.user accordingly
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        SQL = 'SELECT * FROM users WHERE id = %s'
        g.user = get_db().cursor().execute(
            SQL, (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    # upon logout,redirects user to login page
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    # ensures a logged in user is calling the view function, else redirects user to login page
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
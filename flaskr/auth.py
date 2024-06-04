import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from psycopg import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from .initdb import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
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
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
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

            if error is None:
                session.clear()
                session['user_id'] = user[0]
                return redirect(url_for('menu.home'))

            flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
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
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.home'))

        return view(**kwargs)

    return wrapped_view
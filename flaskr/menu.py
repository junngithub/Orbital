from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from .auth import login_required
from .initdb import get_db

import string
import secrets
import random

bp = Blueprint('menu', __name__, url_prefix='/menu')


@bp.route('/')
@login_required
def home():
    dbconn = get_db()
    with dbconn.cursor() as cur:
        SQL = '''
            SELECT w.website, a.email, a.pw
            FROM website w
            INNER JOIN users u ON w.website_id = %s
            INNER JOIN pw a ON a.pw_id = w.id
            ORDER by w.id
        '''
        table = cur.execute(SQL, (g.user[0],)).fetchall()
        if not table:
            table = "None"
    return render_template('menu/home.html', table = table)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        website = request.form['website'].strip()
        email = request.form['email'].strip()
        pw = request.form['password'].strip()
        error = None

        if not website:
            error = 'website is required.'

        if error is not None:
            flash(error)
        else:
            dbconn = get_db()
            with dbconn.cursor() as cur:
                SQL_select = 'SELECT * FROM website where website = %s'
                web_check = cur.execute(
                    SQL_select, (website,)
                ).fetchone()
                # check if website is present
                if web_check is None:
                    SQL_insert = 'INSERT INTO website(website, website_id) VALUES (%s, %s)'
                    cur.execute(
                        SQL_insert, (website, g.user[0])
                    )
                    web_check = cur.execute(
                        SQL_select, (website,)
                    ).fetchone()
                SQL_select = 'SELECT * FROM pw where pw_id = %s'
                pw_check = cur.execute(
                    SQL_select, (web_check[0],)
                ).fetchone()

                if pw_check is None or pw_check[4] != email:
                    SQL_insert = 'INSERT INTO pw (email, pw, pw_id) VALUES (%s, %s, %s)'
                    cur.execute(
                        SQL_insert, (email, pw, web_check[0])
                    )
                    dbconn.commit()
                    cur.close()
                    dbconn.close()
                    flash("Password Added")
                    return redirect(url_for("menu.home"))
                else:
                    # TODO RESOLVE CLASHES OF PW IN EXISTING EMAIL ACCOUNT
                    session['email'] = email
                    session['pw'] = pw
                    session['pw_id'] = web_check[0]
                    cur.close()
                    dbconn.close()
                    return redirect(url_for("menu.confirm"))
    return render_template('menu/add.html')

@bp.route('/confirm', methods=('GET', 'POST'))
@login_required
def confirm():
    if request.method == 'POST':
        if request.form['answer'] == "Ok":
            email = session.get('email')
            pw = session.get('pw')
            pw_id = session.get('pw_id')
            dbconn = get_db()
            with dbconn.cursor() as cur:
                SQL_delete = 'DELETE FROM pw WHERE email = %s'
                SQL_insert = 'INSERT INTO pw (email, pw, pw_id) VALUES (%s, %s, %s)' 
                cur.execute(
                    SQL_delete, (email,) 
                )
                cur.execute(
                    SQL_insert, (email, pw, pw_id) 
                )
                dbconn.commit()
                cur.close()
                dbconn.close()
            return redirect(url_for("menu.home"))
    return render_template('menu/confirm.html')

@bp.route('/generate', methods=('GET', 'POST'))
@login_required
def generate():
    
    def check(tup, str):
        for p in tup:
            if p == str:
                return False
        return True

    password = None
    if request.method == 'GET':
        dbconn = get_db()
        with dbconn.cursor() as cur:
            tup = cur.execute('SELECT pw FROM pw').fetchall()
        r = random.randint(10, 16)
        alphabet = string.ascii_letters + string.digits + "!#$%^&*+,-.:;<=>?@_~"
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(r))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3
                    and check(tup, password)):
                break
    if request.method == 'POST':
        return add()
    return render_template('menu/generate.html', password = password)


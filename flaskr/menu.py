from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, current_app
)
from werkzeug.exceptions import abort
from .auth import login_required
from .initdb import get_db
from .actions import decrypt, encrypt, get_all
from .analyse import analyse_passwords
import string
import secrets
import random

bp = Blueprint('menu', __name__, url_prefix='/menu')

@bp.route('/')
@login_required
def home():
    # fetches logged in user's data and displays home page accordingly
    table = get_all()
    return render_template('menu/home.html', table = table)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    # handle form submission to add a pw
    if request.method == 'POST':
        website = request.form['website'].strip()
        email = request.form['email'].strip()
        pw_dict = encrypt(request.form['password'].strip(), current_app.config['SECRET_KEY'])
        pw = pw_dict['cipher_text']
        expiry = request.form['expiry'].strip() or None
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
                SQL_select = 'SELECT * FROM pw where pw_id = %s AND email = %s'
                pw_check = cur.execute(
                    SQL_select, (web_check[0], email)
                ).fetchone()

                # validates the pw added, checking db for existing entries
                if pw_check is None:
                    SQL_insert = 'INSERT INTO pw (email, pw, pw_id, salt, iv, expiry) VALUES (%s, %s, %s, %s, %s, %s)'
                    cur.execute(
                        SQL_insert, (email, pw, web_check[0], pw_dict['salt'], pw_dict['iv'], expiry)
                    )
                    dbconn.commit()
                    cur.close()
                    dbconn.close()
                    # display success message then redirects user to home page
                    flash("Password Added")
                    return redirect(url_for("menu.home"))
                else:
                    # there is existing pw for tagged website so redirects user to confirmation page
                    session['email'] = email
                    session['pw_dict'] = pw_dict
                    session['pw_id'] = web_check[0]
                    cur.close()
                    dbconn.close()
                    return redirect(url_for("confirm.add"))
    return render_template('menu/add.html')

@bp.route('/generate', methods=('GET', 'POST'))
@login_required
def generate():
    # handle form submission to generate a new pw
    # inner function to check if generated pw is unique
    def check(table, str):
        for p in table:
            if p == str:
                return False
        return True

    password = ""
    website = request.form.get('website', '').strip()
    email = request.form.get('email', '').strip()

    if request.method == 'POST':
        # generates a new password if either the gen button is clicked or if website and email are provided (replace functionality for pw analysis feature)
        if "gen" in request.form or website and email:
            dbconn = get_db()
            with dbconn.cursor() as cur:
                table = cur.execute('SELECT pw, salt, iv FROM pw').fetchall()
                temp = [None] * len(table)
                i = 0
                
                for row in table:
                    cipher_dict = {
                        'cipher_text' : row[0],
                        'salt' : row[1],
                        'iv' : row[2]    
                    }
                    temp[i] = decrypt(cipher_dict, current_app.config['SECRET_KEY'])
                    i += 1
                table = temp
            
            r = random.randint(10, 16)
            alphabet = string.ascii_letters + string.digits
            
            if not request.form.get("excluded") :
                alphabet += "!#$%^&*+,-.:;<=>?@_~"
            while True:
                password = "".join(secrets.choice(alphabet) for i in range(r))
                # checks if generated pw is unique and meets the complexity requirements
                if (any(c.islower() for c in password)
                        and any(c.isupper() for c in password)
                        and sum(c.isdigit() for c in password) >= 3
                        and check(table, password)):
                    break  
            return render_template('menu/generate.html', password = password, gen_btn = "Generate Again?", txt = "Password Generated", website=website, email=email)      
        else:            
            return add()
    return render_template('menu/generate.html', password="", gen_btn = "Generate", txt = "Your generated password will appear below", website=website, email=email)

@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    # handle form submission to delete selected password(s)
    table = get_all()
    if request.method == 'POST':
        temp = request.form["arr"]
        if len(temp) == 0:
            flash("no passwords selected")
        else:
            # redirects user to confirmation page
            arr = temp.split(",")
            session["arr"] = arr
            return redirect(url_for("confirm.delete"))
    return render_template('menu/delete.html', table = table)

@bp.route('/analyse', methods=('GET', 'POST'))
@login_required
def analyse():
    table = analyse_passwords()
    return render_template('menu/analyse.html', table = table)
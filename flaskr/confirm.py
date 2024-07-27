from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, current_app
)
from werkzeug.exceptions import abort
from .auth import login_required

from .initdb import get_db

bp = Blueprint('confirm', __name__, url_prefix='/confirm')

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    # display confrmation message to user about replacing existing password
    # if user confirms, update pw in db accordingly
    message = "A password is tied to this website and account. Replace existing password?"
    if request.method == 'POST':
        if request.form['answer'] == "Ok":
            email = session.get('email')
            pw_dict = session.get('pw_dict')
            pw = pw_dict['cipher_text']
            pw_id = session.get('pw_id')
            expiry = session.get('expiry')
            dbconn = get_db()
            if expiry == '':
                expiry = None
            with dbconn.cursor() as cur:
                SQL_delete = 'DELETE FROM pw WHERE email = %s AND pw_id = %s'
                SQL_insert = 'INSERT INTO pw (email, pw, pw_id, salt, iv, expiry) VALUES (%s, %s, %s, %s, %s, %s)' 
                
                cur.execute(
                    SQL_delete, (email, pw_id) 
                )
                cur.execute(
                    SQL_insert, (email, pw, pw_id, pw_dict['salt'], pw_dict['iv'], expiry) 
                )
                
                dbconn.commit()
                cur.close()
                dbconn.close()
            
            flash("Password Updated")
            return redirect(url_for("menu.home"))
    return render_template('menu/confirm.html', goto = url_for('menu.home'), message = message)

@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    # display confrmation message to user about deleting selected password(s)
    # if user confirms, delete pw from db accordingly
    arr = session.get("arr")
    message = f"Total of {len(arr)} password(s) to be deleted. Continue?"
    if request.method == 'POST':
        if request.form['answer'] == "Ok":
            dbconn = get_db()
            
            with dbconn.cursor() as cur:
                SQL_delete = 'DELETE FROM pw WHERE id = %s'
                for num in arr:
                    cur.execute(SQL_delete, (int(num),))
                dbconn.commit()
                cur.close()
                dbconn.close()
            
            flash("Password(s) Deleted")
            return redirect(url_for("menu.home"))
    return render_template('menu/confirm.html', goto = url_for('menu.delete'), message = message)
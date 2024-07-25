from flask import (
    Blueprint, render_template, g, redirect, url_for
)

bp = Blueprint('start', __name__)

@bp.route('/')
def start():
    # if user is logged in, take user to home page
    if g.user is not None:
        return(redirect(url_for("menu.home")))
    # else take user to welcome page
    return render_template("start.html")
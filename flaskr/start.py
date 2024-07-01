from flask import (
    Blueprint, render_template, g, redirect, url_for
)

bp = Blueprint('start', __name__)

@bp.route('/')
def start():
    if g.user is not None:
        return(redirect(url_for("menu.home")))
    return render_template("start.html")
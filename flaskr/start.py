from flask import (
    Blueprint, render_template
)

bp = Blueprint('start', __name__)

@bp.route('/')
def start():
    return render_template("start.html")
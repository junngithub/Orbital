from flaskr import create_app
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SESSION_TYPE'] = 'sqlalchemy'
#app.config['SECRET_KEY'] = os.urandom(16).hex()
app.config['SECRET_KEY'] = 'ecfb98e3b133f902160458a049a09064'

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
ses = Session(app)

app.app_context().push()
db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
    #serve(app, host='127.0.0.1', port=5000)
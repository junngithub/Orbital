import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv

def create_app(test_config=None):
    # create and configure the app
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # db and session initialisation
    db = SQLAlchemy(app)
    app.config['SESSION_SQLALCHEMY'] = db
    Session(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import and initialise the db, then register all the blueprints
    from . import initdb
    initdb.init_app(app)

    from . import start
    app.register_blueprint(start.bp)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import menu
    app.register_blueprint(menu.bp)

    from . import confirm
    app.register_blueprint(confirm.bp)

    # set app context and create tables
    app.app_context().push()
    db.create_all()

    return app
import os
import psycopg
import click
from flask import g


def get_db():
    # create and return db connection
    if 'db' not in g:
        g.db = psycopg.connect(os.getenv('DATABASE_URL'))
    return g.db


def close_db(e = None):
    # closes db connection at the end of the request
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    # get gb connection
    dbconn = get_db()
    # create tables if they don't exist
    with dbconn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            );
                    
            CREATE TABLE IF NOT EXISTS website (
            id SERIAL PRIMARY KEY,
            website TEXT NOT NULL,
            website_id INT NOT NULL,
            FOREIGN KEY (website_id) REFERENCES users (id)
            );

            CREATE TABLE IF NOT EXISTS pw (
            id SERIAL PRIMARY KEY,
            pw TEXT NOT NULL,
            pw_id INT NOT NULL,
            email TEXT,
            expiry TIMESTAMP,
            salt TEXT NOT NULL,
            iv TEXT NOT NULL,
            FOREIGN KEY (pw_id) REFERENCES website (id)
            )
        """)

        dbconn.commit()
        cur.close()
        dbconn.close()


def init_app(app):
    # registers the close_db function to be called when the app context is torn down
    app.teardown_appcontext(close_db)
    # registers the init_db_command to initialise the db in the Flask CLI
    app.cli.add_command(init_db_command)
    

@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database.')
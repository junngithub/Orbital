import os
import psycopg
import click
from flask import g


def get_db():
    if 'db' not in g:
        g.db = psycopg.connect("dbname=mydb user=postgres host=localhost password=BBLDrizzy36")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    dbconn = get_db()
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
            created_at TIMESTAMP,
            pw TEXT NOT NULL,
            pw_id INT NOT NULL,
            email TEXT,
            expiry TEXT,
            salt TEXT NOT NULL,
            iv TEXT NOT NULL,
            FOREIGN KEY (pw_id) REFERENCES website (id)
            )
        """)

        dbconn.commit()
        cur.close()
        dbconn.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database.')


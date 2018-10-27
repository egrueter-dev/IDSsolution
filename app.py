import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs;"""
    cur.execute(sql_all)
    all = cur.fetchone()[0]

    # Get # of all successful GET requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\';"""
    cur.execute(sql_success)
    success = cur.fetchone()[0]

    # This could probably be simplified to one query.

    # Get # of all successful local GET requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' and source = 'remote';"""
    cur.execute(sql_success)
    success_remote = cur.fetchone()[0]

    # Get # of all successful local GET requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' and source = 'local';"""
    cur.execute(sql_success)
    success_local = cur.fetchone()[0]

    # Determine rate if there was at least one request
    rate = "No entries yet!"
    if all != 0:
        rate = str(success / all)
        remote_rate = str(success_remote / all)
        local_rate = str(success_local / all)

    return render_template('index.html', rate = rate, remote_rate = remote_rate, local_rate = local_rate )

if __name__ == '__main__':
    app.run(host='0.0.0.0')

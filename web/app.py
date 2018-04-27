import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy import text

app = Flask(__name__)

@app.route('/')
def hello_world():
    engine = createEngine()

    sql = text('select COUNTRYNAME from Country')
    result = engine.execute(sql)
    names = []
    for row in result:
        names.append(row[0])

    return render_template('index.html', title='Home')


@app.route('/search/')
def search():
    input = request.args.get('query')
    engine = createEngine()

    sql = text('select COUNTRYNAME from Country where lower(COUNTRYNAME) like :search')
    result = engine.execute(sql, search="%{}%".format(input).lower())
    names = []
    for row in result:
        print(row[0])
        names.append(row[0])

    return render_template('search.html', countries=names, query=input)


@app.route('/predefined/<query_nr>/')
def query_result(query_nr):

    objects = os.listdir('queries')

    o = objects[int(float(query_nr)) - 1]
    with open(os.path.join('queries', o)) as f:
        query = f.read()

    engine = createEngine()

    sql = text(query)
    result = engine.execute(sql)

    r = []
    for row in result:
        print(row[0])
        r.append(row[0])

    return render_template('predefined.html', queries=(read_queries()), result=r)


@app.route('/predefined/')
def predefiend():
    return render_template('predefined.html', queries=(read_queries()))


def read_queries():
    objects = os.listdir('queries')
    queries = []
    for o in objects:
        with open(os.path.join('queries', o)) as f:
            first_line = f.readline()
        queries.append(first_line.replace("-- Name: ", ""))
    return queries


@app.route('/insert/')
def insert():
    return render_template('insert-delete.html')


def createEngine():
    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'
    engine = create_engine(oracle_connection_string.format(
        username='DB2018_G17',
        password='DB2018_G17',
        hostname='diassrv2.epfl.ch',
        port='1521',
        database='orcldias',
    ))
    engine.connect()
    return engine


if __name__ == '__main__':
    app.run()

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

@app.route('/search/show/<table>/')
def search_result(table):
    input = request.args.get('query')
    engine = createEngine()

    names = []
    return render_template('search-result.html', tables=names, query=input)


@app.route('/search/')
def search():
    input = request.args.get('query')
    engine = createEngine()

    names = []

    search_country(engine, input, names, 'select count(*) from Country where lower(COUNTRYNAME) like :search')
    search_country(engine, input, names, 'select count(*) from Language where lower(language) like :search', "Language")

    return render_template('search.html', tables=names, query=input)


def search_country(engine, input, names, search, country="Country"):
    sql = text(search)
    result = engine.execute(sql, search="%{}%".format(input).lower())
    row = result.fetchone();
    if row[0] > 0:
        names.append(country);


@app.route('/predefined/<query_nr>/')
def query_result(query_nr):

    # objects = os.listdir('queries')
    #
    # o = objects[int(float(query_nr)) - 1]
    # with open(os.path.join('queries', o)) as f:
    #     query = f.read()
    #
    # engine = createEngine()
    #
    # sql = text(query)
    # result = engine.execute(sql)
    #
    # r = []
    # for row in result:
    #     print(row[0])
    #     r.append(row[0])

    return render_template('predefined-result.html')


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


@app.route('/insert/clip/')
def insert_clip():
    return render_template('insert-clip.html')

@app.route('/insert/')
def insert():
    return render_template('insert-delete.html')

def createEngine():
    engine = create_engine('sqlite:///../imported_files/database.db');
    return engine

def createEngineOracle():
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

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
    if table == 'Country':
        column_name = 'countryname'
        search_query(engine, input, names, 'select * from Country where lower(COUNTRYNAME) like :search', column_name)
    elif table == 'Language':
        column_name = 'language'
        search_query(engine, input, names, 'select * from Language where lower(language) like :search', column_name,
                       "Language")

    return render_template('search-result.html', tables=names, query=input, table_name = table)

def search_query(engine, input, names, search, column, country="Country"):
    sql = text(search)
    result = engine.execute(sql, search="%{}%".format(input).lower())
    for row in result:
        names.append(row[column])


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
    engine = create_engine('postgresql://db:db@db.kiru.io/db')
    engine.connect()
    return engine

if __name__ == '__main__':
    app.run(debug=True)

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
        search_query(engine, input, names, 'select * from Country where lower(COUNTRYNAME) like :search limit 200', column_name)
    elif table == 'Language':
        column_name = 'language'
        search_query(engine, input, names, 'select * from Language where lower(language) like :search limit 200', column_name,
                       "Language")
    elif table == 'Person':
        column_name = 'fullname'
        search_query(engine, input, names, 'select * from Person where lower(fullname) like :search limit 200', column_name,
                       "Person")
    elif table == 'Actor':
        column_name = 'fullname'
        search_query(engine, input, names, 'select DISTINCT person.fullname from acts, person where acts.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200', column_name,
                       "Actor")
    elif table == 'Clip':
        column_name = 'clip_title'
        search_query(engine, input, names, 'select * from Clip where lower(clip_title) like :search limit 200', column_name,
                       "Clip")

    elif table == 'Writer':
        column_name = 'fullname'
        search_query(engine, input, names, 'select DISTINCT person.fullname from writes, person where writes.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200', column_name,
                       "Writer")
    elif table == 'Director':
        column_name = 'fullname'
        search_query(engine, input, names, 'select DISTINCT person.fullname from directs, person where directs.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200', column_name,
                       "Director")
    elif table == 'Producer':
        column_name = 'fullname'
        search_query(engine, input, names, 'select DISTINCT person.fullname from produces, person where produces.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200', column_name,
                       "Producer")

    return render_template('search-result.html', tables=names, query=input, table_name = table)

def search_query(engine, input, names, search, column, country="Country"):
    sql = text(search)
    result = engine.execute(sql, search="%{}%".format(input).lower())
    for row in result:
        names.append(row[column])


@app.route('/search/')
def search():
    input = request.args.get('query')
    c = request.args.get('country')
    l = request.args.get('language')
    p = request.args.get('person')
    clip = request.args.get('clips')
    a = request.args.get('actor')
    direct = request.args.get('director')
    write = request.args.get('writer')
    produce = request.args.get('producer')

    engine = createEngine()

    names = []

    if not (c or l or p or clip or a or direct or write or produce):
        search_country(engine, input, names, 'select * from Country where lower(COUNTRYNAME) like :search limit 1')
        search_country(engine, input, names, 'select * from Language where lower(language) like :search limit 1',
                       "Language")
        search_country(engine, input, names, 'select * from Clip where lower(clip_title) like :search limit 1', "Clip")
        search_country(engine, input, names, 'select * from person where lower(fullname) like :search limit 1', "Person")
        search_country(engine, input, names,
                       'select * from acts, person where acts.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                       "Actor")

        search_country(engine, input, names,
                       'select * from directs, person where directs.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                       "Director")
        search_country(engine, input, names,
                       'select * from writes, person where writes.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                       "Writer")
        search_country(engine, input, names,
                       'select * from produces, person where produces.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                       "Producer")

    else:
        if c:
            search_country(engine, input, names, 'select * from Country where lower(COUNTRYNAME) like :search limit 1')
        if l:
            search_country(engine, input, names, 'select * from Language where lower(language) like :search limit 1', "Language")
        if clip:
            search_country(engine, input, names, 'select * from Clip where lower(clip_title) like :search limit 1', "Clip")
        if p:
            search_country(engine, input, names, 'select * from person where lower(fullname) like :search limit 1', "Person")
        if a:
            search_country(engine, input, names, 'select * from acts, person where acts.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1', "Actor")
        if direct:
            search_country(engine, input, names,
                           'select * from directs, person where directs.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                           "Director")
        if write:
            search_country(engine, input, names,
                           'select * from writes, person where writes.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                           "Writer")
        if produce:
            search_country(engine, input, names,
                           'select * from produces, person where produces.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                           "Producer")
    return render_template('search.html', tables=names, query=input)


def search_country(engine, input, names, search, country="Country"):
    sql = text(search)
    result = engine.execute(sql, search="%{}%".format(input).lower())
    row = result.first();
    if row:
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

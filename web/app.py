import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy import text
import sys

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
        search_query(engine, input, names, 'select * from Country where lower(COUNTRYNAME) like :search limit 200',
                     column_name)
    elif table == 'Language':
        column_name = 'language'
        search_query(engine, input, names, 'select * from Language where lower(language) like :search limit 200',
                     column_name,
                     "Language")
    elif table == 'Person':
        column_name = 'fullname'
        search_query(engine, input, names, 'select * from Person where lower(fullname) like :search limit 200',
                     column_name,
                     "Person")
    elif table == 'Actor':
        column_name = 'fullname'
        search_query(engine, input, names,
                     'select DISTINCT person.fullname from acts, person where acts.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200',
                     column_name,
                     "Actor")
    elif table == 'Clip':
        column_name = 'clip_title'
        search_query(engine, input, names, 'select * from Clip where lower(clip_title) like :search limit 200',
                     column_name,
                     "Clip")

    elif table == 'Writer':
        column_name = 'fullname'
        search_query(engine, input, names,
                     'select DISTINCT person.fullname from writes, person where writes.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200',
                     column_name,
                     "Writer")
    elif table == 'Director':
        column_name = 'fullname'
        search_query(engine, input, names,
                     'select DISTINCT person.fullname from directs, person where directs.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200',
                     column_name,
                     "Director")
    elif table == 'Producer':
        column_name = 'fullname'
        search_query(engine, input, names,
                     'select DISTINCT person.fullname from produces, person where produces.person_id = person.person_id AND (lower(person.fullname) like :search) limit 200',
                     column_name,
                     "Producer")

    return render_template('search-result.html', tables=names, query=input, table_name=table)


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

    if not input:
        return render_template('search.html', tables=names, query=input)

    if not (c or l or p or clip or a or direct or write or produce):
        search_country(engine, input, names, 'select * from Country where lower(COUNTRYNAME) like :search limit 1')
        search_country(engine, input, names, 'select * from Language where lower(language) like :search limit 1',
                       "Language")
        search_country(engine, input, names, 'select * from Clip where lower(clip_title) like :search limit 1', "Clip")
        search_country(engine, input, names, 'select * from person where lower(fullname) like :search limit 1',
                       "Person")
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
            search_country(engine, input, names, 'select * from Language where lower(language) like :search limit 1',
                           "Language")
        if clip:
            search_country(engine, input, names, 'select * from Clip where lower(clip_title) like :search limit 1',
                           "Clip")
        if p:
            search_country(engine, input, names, 'select * from person where lower(fullname) like :search limit 1',
                           "Person")
        if a:
            search_country(engine, input, names,
                           'select * from acts, person where acts.person_id = person.person_id AND (lower(person.fullname) like :search) limit 1',
                           "Actor")
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


@app.route('/predefined/1/')
def query_result_1():
    c = request.args.get('country')
    engine = createEngine()

    sql = text("""
        SELECT
          C.CLIP_ID,
          C.CLIP_TITLE,
          max(R.RUNNING_TIME) AS runtime
        FROM CLIP c
          JOIN RUNS R ON c.CLIP_ID = R.CLIP_ID
          JOIN COUNTRY C2 ON r.COUNTRY_ID = C2.COUNTRY_ID
        WHERE lower(C2.COUNTRYNAME) = lower(:country)
        GROUP BY c.CLIP_ID, c.CLIP_TITLE
        ORDER BY runtime DESC, c.CLIP_ID, C.CLIP_TITLE
        FETCH FIRST 10 ROWS ONLY;
    """)

    names = []
    result = engine.execute(sql, country=c)
    for row in result:
        names.append({
            "title": row[1],
            "running": row[2]
        })

    return render_template('predefined_result_1.html', names=names)

@app.route('/predefined/2/')
def query_result_2():
    c = request.args.get('year')
    engine = createEngine()

    sql = text("""
        SELECT
          c2.COUNTRYNAME,
          count(*) AS nb_of_clips
        FROM CLIP c
          JOIN RELEASED R ON c.CLIP_ID = R.CLIP_ID
          JOIN COUNTRY C2 ON R.COUNTRY_ID = C2.COUNTRY_ID
        WHERE extract(YEAR FROM r.RELEASE_DATE) = :yy
        GROUP BY c2.COUNTRYNAME
        ORDER BY c2.COUNTRYNAME
    """)

    names = []
    result = engine.execute(sql, yy=c)
    for row in result:
        names.append({
            "name": row[0],
            "number": row[1]
        })

    return render_template('predefined_result_2.html', names=names)\


@app.route('/predefined/3/')
def query_result_3():
    y = request.args.get('year')
    c = request.args.get('country')

    engine = createEngine()

    sql = text("""
        SELECT
          G.GENRE,
          count(*) AS nb_of_clips
        FROM CLIP c
          JOIN CLIP_GENRE CG ON CG.CLIP_ID = C.CLIP_ID
          JOIN RELEASED R ON c.CLIP_ID = R.CLIP_ID
          JOIN COUNTRY C2 ON R.COUNTRY_ID = C2.COUNTRY_ID
          JOIN GENRE G ON CG.GENRE_ID = G.GENRE_ID
        WHERE extract(YEAR FROM r.RELEASE_DATE) >= :year
              AND lower(C2.COUNTRYNAME) = lower(:country)
        GROUP BY G.GENRE
        ORDER BY g.GENRE;
    """)

    names = []
    result = engine.execute(sql, country=c, year=y)
    for row in result:
        names.append({
            "genre": row[0],
            "count": row[1]
        })

    return render_template('predefined_result_3.html', names=names)


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
    title = request.args.get('title')
    year = request.args.get('year')

    typ = request.args.get('type')
    engine = createEngine()
    result = engine.execute(text('select max(clip_id) from clip'))
    row = result.first()
    id = row[0] + 1
    data = {'clip_id': id, 'clip_type': typ, 'clip_year': year, 'clip_title': title}

    if title and year and type:
        engine.execute(text(
            "INSERT INTO clip (clip_id, clip_type, clip_year, clip_title) VALUES (:clip_id, :clip_type, to_date(:clip_year, 'YYYY'), :clip_title)"),
            data)

    return render_template('insert-clip.html', clip_title=title, clip_year=year, clip_type=typ, clip_id=id)


@app.route('/delete/clip/')
def delete_clip():
    try:
        input = int(request.args.get('id'))
        print(type(input))
    except:
        input = request.args.get('id')
        print(type(input))
    engine = createEngine()
    data = {'clip_id': input}
    if input:
        result = engine.execute(text("Select count(*) from clip where clip_id = :clip_id"), data)
        row = result.first()
        num = row[0]
        engine.execute(text("delete from clip where clip_id = :clip_id"), data)
    else:
        num = False

    return render_template('delete-clip.html', deleted=num, id=input)


@app.route('/insert/')
def insert():
    return render_template('insert-delete.html')


@app.route('/delete/')
def delete():
    return render_template('delete.html')


def createEngine():
    engine = create_engine('postgresql://db:db@db.kiru.io/db')
    engine.connect()
    return engine


if __name__ == '__main__':
    app.run(debug=True)

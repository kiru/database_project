import os
import timeit

from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy import text
import time

import sys
import json


def createEngine():
    engine = create_engine('postgresql://db:db@db.kiru.io/db')
    engine.connect()
    return engine


app = Flask(__name__)
engine = createEngine()


@app.route('/')
def hello_world():
    return redirect('/search')


@app.route('/search/show/<table>/delete/')
def search_result_delete(table):
    clip_id = request.args.get('clip_id')
    person_id = request.args.get('person_id')

    query = request.args.get('query')
    offset = request.args.get('offset')

    if table == 'Actor':
        engine.execute(text("delete from acts where clip_id = :clip_id and person_id = :person_id"), clip_id=clip_id, person_id=person_id)

    if table == 'Writer':
        engine.execute(text("delete from writes where clip_id = :clip_id and person_id = :person_id"), clip_id=clip_id, person_id=person_id)

    if table == 'Producer':
        engine.execute(text("delete from produces where clip_id = :clip_id and person_id = :person_id"), clip_id=clip_id, person_id=person_id)

    if table == 'Director':
        engine.execute(text("delete from directs where clip_id = :clip_id and person_id = :person_id"), clip_id=clip_id, person_id=person_id)

    return redirect('/search/show/' + table + "/?query=" + query + "&offset=" + offset)



@app.route('/search/show/<table>/')
def search_result(table):
    input = request.args.get('query')
    offset = request.args.get('offset')
    if(offset is None):
        offset = 0

    names = []

    if table == 'Country':
        search_query(engine, input, names, 'select countryname as "Country" from Country where COUNTRYNAME ilike :search limit 50',
                     ['Country'])

    elif table == 'Language':
        search_query(engine, input, names, 'select language as "Language" from Language where language ilike :search limit 50',
                     ['Language'],
                     "Language")

    elif table == 'Person':
        search_query(engine, input, names, 'select fullname as "Name" from Person where fullname ilike :search limit 50',
                     ['Name'],
                     "Person")

    elif table == 'Clip':

        search_query(engine,
                     input,
                     names,
                     'select distinct clip_title as "Clip", to_char(clip_year, \'YYYY\') as "Year" from Clip where clip_title ilike :search limit 50 OFFSET :offset',
                     ['Clip', 'Year'],
                     "Clip",
                     offset
                     )


    elif table == 'Actor':
        search_query(engine, input, names,
                     'select DISTINCT person.fullname as "Actor", person.person_id, clip.clip_id, clip.clip_title as "Clip" from acts, person, clip '
                        'where acts.person_id = person.person_id and clip.clip_id = acts.clip_id '
                        'AND (person.fullname ilike :search) limit 50',

                     ['Actor', "Clip", "clip_id", "person_id"],
                     "Actor")

    elif table == 'Writer':
        search_query(engine, input, names,
                     'select DISTINCT person.fullname as "Name", clip_title as "Clip", person.person_id, clip.clip_id from writes, person, clip '
                        'where writes.person_id = person.person_id and clip.clip_id = writes.clip_id '
                        'AND (person.fullname ilike :search) limit 50',
                     ['Name', 'Clip', "clip_id", "person_id"],
                     "Writer")
        
    elif table == 'Director':
        search_query(engine, input, names,
                     'select DISTINCT person.fullname as "Name", clip_title as "Clip",person.person_id, clip.clip_id  from directs, person, clip '
                        'where directs.person_id = person.person_id and clip.clip_id = directs.clip_id '
                        'AND (person.fullname ilike :search) limit 50',
                     ['Name', 'Clip', "clip_id", "person_id"],
                     "Director")
        
    elif table == 'Producer':
        search_query(engine, input, names,
                     'select DISTINCT person.fullname as "Name", clip.clip_title as "Clip", person.person_id, clip.clip_id from produces, person, clip '
                        'where produces.person_id = person.person_id and clip.clip_id = produces.clip_id '
                        'AND (person.fullname ilike :search) limit 50',
                     ['Name', 'Clip', "clip_id", "person_id"],
                     "Producer")

    return render_template('search-result.html', tables=names, query=input,
                           has_delete='True',
                           table_name=table, next=(int(offset) + 50), prev=(int(offset) - 50))


def search_query(engine, input, names, search, column, country="Country", offset=0):
    sql = text(search)
    result = engine.execute(sql, search="%{}%".format(input).lower(), offset=offset)
    for row in result:
        d = {}
        for c in column:
            d[c] = row[c]
        names.append(d)


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

    names = []

    if not input:
        return render_template('search.html', tables=names, query=input)

    if not (c or l or p or clip or a or direct or write or produce):
        search_country(engine, input, names, 'select countryname from Country where COUNTRYNAME ilike :search limit 1')
        search_country(engine, input, names, 'select language from Language where language ilike :search limit 1',
                       "Language")
        search_country(engine, input, names, 'select clip_title from Clip where clip_title ilike :search limit 1',
                       "Clip")
        search_country(engine, input, names, 'select fullname from person where fullname ilike :search limit 1',
                       "Person")
        search_country(engine, input, names,
                       'select person.fullname from acts, person where acts.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                       "Actor")

        search_country(engine, input, names,
                       'select person.fullname from directs, person where directs.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                       "Director")
        search_country(engine, input, names,
                       'select person.fullname from writes, person where writes.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                       "Writer")
        search_country(engine, input, names,
                       'select person.fullname from produces, person where produces.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                       "Producer")

    else:
        if c:
            search_country(engine, input, names,
                           'select countryname from Country where COUNTRYNAME ilike :search limit 1')
        if l:
            search_country(engine, input, names, 'select language from Language where language ilike :search limit 1',
                           "Language")
        if clip:
            search_country(engine, input, names, 'select clip_title from Clip where clip_title ilike :search limit 1',
                           "Clip")
        if p:
            search_country(engine, input, names, 'select fullname from person where fullname ilike :search limit 1',
                           "Person")
        if a:
            search_country(engine, input, names,
                           'select fullname from acts, person where acts.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                           "Actor")
        if direct:
            search_country(engine, input, names,
                           'select fullname from directs, person where directs.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                           "Director")
        if write:
            search_country(engine, input, names,
                           'select fullname from writes, person where writes.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                           "Writer")
        if produce:
            search_country(engine, input, names,
                           'select fullname from produces, person where produces.person_id = person.person_id AND (person.fullname ilike :search) limit 1',
                           "Producer")
    return render_template('search.html',
                           tables=names,
                           query=input, check_country=c, check_langauge=l, check_person=p, check_clip=clip,
                           check_actor=a,
                           check_director=direct, check_write=write, check_produce=produce)


def search_country(engine, input, names, search, country="Country"):
    start = timeit.timeit()

    sql = text(search)
    result = engine.execute(sql, search="%{}%".format(input).lower())

    end = timeit.timeit()

    row = result.first()
    if row:
        names.append(country)

    print("Time taken: {} for {}".format((end - start), search))


@app.route('/predefined/1/')
def query_result_1():
    c = request.args.get('country')
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

    return render_template('predefined_result_2.html', names=names)


@app.route('/predefined/3/')
def query_result_3():
    y = request.args.get('year')
    c = request.args.get('country')

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
    result = engine.execute(text('select max(clip_id) from clip'))
    row = result.first()
    id = row[0] + 1
    data = {'clip_id': id, 'clip_type': typ, 'clip_year': year, 'clip_title': title}

    if title and year and type:
        engine.execute(text(
            "INSERT INTO clip (clip_id, clip_type, clip_year, clip_title) VALUES (:clip_id, :clip_type, to_date(:clip_year, 'YYYY'), :clip_title)"),
            data)

    return render_template('insert-clip.html', clip_title=title, clip_year=year, clip_type=typ, clip_id=id)


@app.route('/insert/actor/autocomplete/person')
def insert_actor_autocomplete_person():
    q = request.args.get('q')
    sql = text('select person_id, fullname from person where fullname ilike :search order by fullname limit 50')
    result = engine.execute(sql, search="%{}%".format(q).lower())

    res = []
    for row in result:
        res.append({
            "id": row[0],
            "value": row[1]
        })

    return json.dumps(res)


@app.route('/insert/actor/autocomplete/clip')
def insert_actor_autocomplete_clip():
    q = request.args.get('q')
    sql = text('select clip_id, clip_title from clip where clip_title ilike :search order by clip_title limit 50')
    result = engine.execute(sql, search="%{}%".format(q).lower())

    res = []
    for row in result:
        res.append({
            "id": row[0],
            "value": row[1]
        })

    return json.dumps(res)


@app.route('/insert/actor/save', methods=['POST'])
def insert_actor_save():
    data = {
        'person_id': (request.form.get('person_id')),
        'clip_id': (request.form.get('clip_id')),
        'c': (request.form.get('character')),
        'a': (request.form.get('additional_info')),
        'o': (request.form.get('orders_credits'))
    }

    print(json.dumps(data, indent=4))

    result = engine.execute(text('select count(*) from acts where acts.clip_id = :c and acts.person_id = :p'),
                            p=(request.form.get('person_id')), c=request.form.get('clip_id'))
    row = result.first()
    if (row[0] > 0):
        return render_template('insert-actor-done.html', data=data, failed='True')
    else:
        engine.execute(text(
        "INSERT INTO acts (person_id, clip_id, additional_info, \"character\", orders_credit)  VALUES (:person_id, :clip_id, :a, :c, :o)"),
        data)
        return render_template('insert-actor-done.html', failed='False')


@app.route('/insert/actor/')
def insert_actor():
    person_id = request.args.get('person_id')
    clip_id = request.args.get('clip_id')
    character = request.args.get('character')
    additional_info = request.args.get('additional_info')
    orders_credits = request.args.get('orders_credits')

    result = engine.execute(text('select max(clip_id) from clip'))
    row = result.first()
    id = row[0] + 1
    typ = "2"
    year = 2000
    title = "2"
    # data = {'clip_id': id, 'clip_type': typ, 'clip_year': year, 'clip_title': title}

    # if title and year and type:
    #     engine.execute(text(
    #         "INSERT INTO clip (clip_id, clip_type, clip_year, clip_title) VALUES (:clip_id, :clip_type, to_date(:clip_year, 'YYYY'), :clip_title)"),
    #         data)

    return render_template('insert-actor.html', clip_title=title, clip_year=year, clip_type=typ, clip_id=id)


@app.route('/delete/clip/')
def delete_clip():
    try:
        input = int(request.args.get('id'))
        print(type(input))
    except:
        input = request.args.get('id')
        print(type(input))
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


if __name__ == '__main__':
    app.run(debug=True)

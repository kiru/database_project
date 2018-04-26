from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import text

app = Flask(__name__)


@app.route('/')
def hello_world():
    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'
    engine = create_engine(oracle_connection_string.format(
        username='DB2018_G17',
        password='DB2018_G17',
        hostname='diassrv2.epfl.ch',
        port='1521',
        database='orcldias',
    ))
    engine.connect()

    sql = text('select COUNTRYNAME from Country')
    result = engine.execute(sql)
    names = []
    for row in result:
        names.append(row[0])

    return 'Hello World!: ' + "<br />".join(str(x) for x in names)


if __name__ == '__main__':
    app.run()

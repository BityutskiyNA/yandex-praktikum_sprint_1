import sqlite3
import uuid
from datetime import datetime

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dataclasses import dataclass, field


@dataclass
class Movie:
    id: uuid.UUID
    title: str
    description: str
    creation_date: str
    rating: str
    type: str = field(default="")
    file_path: str = field(default="")
    created_at: datetime = field(default=datetime.utcnow())
    updated_at: datetime = field(default=datetime.utcnow())
    created: datetime = field(default=datetime.utcnow())
    modified: datetime = field(default=datetime.utcnow())

    def get_list_movies(self):
        if self.description != None:
            description = self.description.replace("'", '"')
        else:
            description = self.description

        title = self.title.replace("'", '"')
        if self.type == None:
            type = 0.0
        else:
            type = self.type
        return (self.id, str(title), str(description), self.creation_date, self.rating, type, str(self.created_at), str(self.updated_at))

    def get_list_no_date(self):
        if self.description != None:
            description = self.description.replace("'", '"')
        else:
            description = self.description

        title = self.title.replace("'", '"')
        if self.type == None:
            type = 0.0
        else:
            type = self.type
        return self.id, str(title), str(description), self.creation_date, self.rating, type


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at:  datetime = field(default=datetime.utcnow())
    updated_at:  datetime = field(default=datetime.utcnow())
    created: datetime = field(default=datetime.utcnow())
    modified: datetime = field(default=datetime.utcnow())

    def get_list_genre(self):
        if self.description != None:
            description = self.description.replace("'", '"')
        else:
            description = self.description
        name = self.name.replace("'", '"')
        return (self.id, name, description, self.created_at, self.updated_at)

    def get_list_no_date(self):
        if self.description != None:
            description = self.description.replace("'", '"')
        else:
            description = self.description
        name = self.name.replace("'", '"')
        return (self.id, name, description)


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created_at:  datetime = field(default=datetime.utcnow())
    updated_at:  datetime = field(default=datetime.utcnow())
    created: datetime = field(default=datetime.utcnow())
    modified: datetime = field(default=datetime.utcnow())

    def get_list_person(self):
        full_name = self.full_name.replace("'", '"')
        return (self.id, full_name, self.created_at, self.updated_at)

    def get_list_no_date(self):
        full_name = self.full_name.replace("'", '"')
        return (self.id, full_name)

@dataclass
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: str
    person_id: str
    created_at: datetime = field(default=datetime.utcnow())
    role: str = field(default="")
    created: datetime = field(default=datetime.utcnow())

    def get_list_person_film_work(self):
        return (self.id, self.person_id, self.film_work_id, self.role, self.created_at)

    def get_list_no_date(self):
        return (self.id, self.person_id, self.film_work_id, self.role)


@dataclass
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: str
    genre_id: str
    created_at: datetime = field(default=datetime.utcnow())
    created: datetime = field(default=datetime.utcnow())


    def get_list_genre_film_work(self):
        return (self.id, self.genre_id, self.film_work_id, self.created_at)

    def get_list_no_date(self):
        return (self.id, self.genre_id, self.film_work_id)


class PostgresSaver:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all(self, table_name, coll, val, record):
        curs = self.pg_conn.cursor()
        sql_qwelle = """INSERT INTO content.{0} {1} 
                     VALUES {2}
                     ON CONFLICT (id) DO NOTHING""".format(table_name, coll, val)
        curs.executemany(sql_qwelle, record)


class SQLiteExtractor:
    def __init__(self, connection = None, curs=None):
        self.connection = connection
        self.curs = curs


    def extract_data(self,coll, table_name, DataCls):
        self.curs.execute("SELECT {0} FROM {1} SORT ORDER BY id;".format(coll, table_name))
        data = self.curs.fetchall()
        return [DataCls(**dict(x)) for x in data]


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    connection.row_factory = sqlite3.Row
    curs = connection.cursor()
    sqlite_extractor = SQLiteExtractor(connection, curs)

    data_person_film_work = sqlite_extractor.extract_data('id, film_work_id, person_id, role', 'person_film_work', PersonFilmWork)
    data_person = sqlite_extractor.extract_data('id, full_name', 'person', Person)
    data_genre = sqlite_extractor.extract_data('id, name, description', 'genre', Genre)
    data_movies = sqlite_extractor.extract_data('id, title, description, creation_date, file_path, rating ,type', 'film_work', Movie)
    data_genre_film_work= sqlite_extractor.extract_data('id, film_work_id, genre_id', 'genre_film_work', GenreFilmWork)

    coll = '(id, title, description, creation_date, rating, type, created, modified)'
    val = '(%s, %s, %s, %s, %s, %s, %s, %s)'
    record = [x.get_list_movies() for x in data_movies]
    postgres_saver.save_all('film_work', coll, val, record)

    coll = '(id, name, description,created, modified)'
    val = '(%s, %s, %s, %s, %s)'
    record = [x.get_list_genre() for x in data_genre]
    postgres_saver.save_all('genre', coll, val, record)

    coll = '(id, full_name, created, modified)'
    val = '(%s, %s, %s, %s)'
    record = [x.get_list_person() for x in data_person]
    postgres_saver.save_all('person', coll, val, record)

    coll = '(id, person_id, film_work_id, role, created)'
    val = '(%s, %s, %s, %s, %s)'
    record = [x.get_list_person_film_work() for x in data_person_film_work]
    postgres_saver.save_all('person_film_work', coll, val, record)

    coll = '(id, genre_id, film_work_id, created)'
    val = '(%s, %s, %s, %s)'
    record = [x.get_list_genre_film_work() for x in data_genre_film_work]
    postgres_saver.save_all('genre_film_work', coll, val, record)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 54320}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

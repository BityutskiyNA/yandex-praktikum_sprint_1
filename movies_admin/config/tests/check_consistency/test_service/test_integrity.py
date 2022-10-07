import pytest
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor
import collections
from load_data import SQLiteExtractor, Movie, Genre, Person, PersonFilmWork, GenreFilmWork


def get_test(data_sl, data_pg):
    for x in data_pg:
        if collections.Counter(x.get_list_no_date()) != collections.Counter(data_sl[data_pg.index(x)].get_list_no_date()):
            return False
    return True


@pytest.fixture()
def sqlite_curs():
    with sqlite3.connect('../../../../db.sqlite') as sqlite_conn:
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_curs = sqlite_conn.cursor()
        return sqlite_curs


@pytest.fixture()
def curs_pg():
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 54320}
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        curs_pg = pg_conn.cursor()
        return curs_pg


class TestSumFunc:

    def test_len_film_work(self, sqlite_curs, curs_pg):
        sql_data = SQLiteExtractor(None, sqlite_curs)
        data_sl = sql_data.extract_data('*','film_work', Movie)

        sql_data = SQLiteExtractor(None, curs_pg)
        data_pg = sql_data.extract_data('*', 'content.film_work', Movie)

        data = get_test(data_sl, data_pg)

        assert len(data_sl) == len(data_pg)
        assert data == True

    def test_len_genre(self, sqlite_curs, curs_pg):
        sql_data = SQLiteExtractor(None, sqlite_curs)
        data_sl = sql_data.extract_data('*', 'genre', Genre)

        sql_data = SQLiteExtractor(None, curs_pg)
        data_pg = sql_data.extract_data('*', 'content.genre', Genre)
        data = get_test(data_sl, data_pg)

        assert len(data_sl) == len(data_pg)
        assert data == True

    def test_len_genre_film_work(self, sqlite_curs, curs_pg):
        sql_data = SQLiteExtractor(None, sqlite_curs)
        data_sl = sql_data.extract_data('*', 'genre_film_work', GenreFilmWork)

        sql_data = SQLiteExtractor(None, curs_pg)
        data_pg = sql_data.extract_data('*', 'content.genre_film_work', GenreFilmWork)

        data = get_test(data_sl, data_pg)

        assert len(data_sl) == len(data_pg)
        assert data == True

    def test_len_person(self, sqlite_curs, curs_pg):
        sql_data = SQLiteExtractor(None, sqlite_curs)
        data_sl = sql_data.extract_data('*', 'person', Person)

        sql_data = SQLiteExtractor(None, curs_pg)
        data_pg = sql_data.extract_data('*', 'content.person', Person)

        data = get_test(data_sl, data_pg)

        assert len(data_sl) == len(data_pg)
        assert data == True

    def test_len_person_film_work(self, sqlite_curs, curs_pg):
        sql_data = SQLiteExtractor(None, sqlite_curs)
        data_sl = sql_data.extract_data('*', 'person_film_work', PersonFilmWork)

        sql_data = SQLiteExtractor(None, curs_pg)
        data_pg = sql_data.extract_data('*', 'content.person_film_work', PersonFilmWork)

        data = get_test(data_sl, data_pg)

        assert len(data_sl) == len(data_pg)
        assert data == True
